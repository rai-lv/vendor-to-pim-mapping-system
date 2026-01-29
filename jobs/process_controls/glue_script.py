import sys
import json
import re
import traceback
from datetime import datetime, timezone
from typing import Dict, List, Tuple, Optional
import csv
from io import StringIO
from os.path import basename

import boto3
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, expr, trim
from pyspark.sql.types import StringType

# =========================
# Configuration Constants
# =========================

SAMPLE_BUFFER_SIZE = 65536  # 64KB for CSV dialect detection
MAX_DIALECT_SAMPLE_LINES = 200
CSV_SEPARATORS = [";", ",", "\t", "|"]
MAX_DUPLICATE_SAMPLE_COUNT = 20

# Fact (user-provided): delimiter is tabstop
FORCED_INPUT_SEPARATOR = "\t"
FORCED_OUTPUT_SEPARATOR = "\t"

# =========================
# Helpers (aligned pattern)
# =========================

def validate_s3_key(key: str) -> None:
    """
    Validate S3 key format for basic security checks.
    Raises ValueError if key is invalid.
    """
    if not key:
        raise ValueError("S3 key cannot be empty")

    # Check for invalid null characters
    if "\0" in key:
        raise ValueError("Invalid S3 key format (contains null character)")

def ensure_prefix_uri(uri: str) -> str:
    if uri.endswith("/"):
        return uri
    return uri + "/"

def list_s3_objects(bucket: str, prefix: str) -> List[str]:
    s3_client = boto3.client("s3")
    keys: List[str] = []
    continuation_token = None

    print(f"[INFO] Listing S3 objects in bucket='{bucket}', prefix='{prefix}'")
    while True:
        list_kwargs = {"Bucket": bucket, "Prefix": prefix}
        if continuation_token:
            list_kwargs["ContinuationToken"] = continuation_token

        resp = s3_client.list_objects_v2(**list_kwargs)
        for item in resp.get("Contents", []):
            keys.append(item["Key"])

        if resp.get("IsTruncated"):
            continuation_token = resp.get("NextContinuationToken")
        else:
            break

    print(f"[INFO] Found {len(keys)} object(s) under prefix '{prefix}'")
    return keys

def _read_s3_head(bucket: str, key: str, max_bytes: int = SAMPLE_BUFFER_SIZE) -> bytes:
    s3 = boto3.client("s3")
    resp = s3.get_object(Bucket=bucket, Key=key, Range=f"bytes=0-{max_bytes-1}")
    return resp["Body"].read()

def detect_csv_dialect(bucket: str, key: str) -> Tuple[str, str]:
    """
    Detect encoding using a small head sample.
    Separator is forced to TAB (\t) as per user input.
    Returns (sep, encoding_name_for_spark).
    """
    raw = _read_s3_head(bucket, key, SAMPLE_BUFFER_SIZE)

    # --- UTF-16 BOM detection (critical for Excel/Windows exports) ---
    # FF FE => UTF-16LE BOM, FE FF => UTF-16BE BOM
    if raw.startswith(b"\xff\xfe"):
        # Validate decode works (debug safety); Spark should read with UTF-16LE
        _ = raw.decode("utf-16", errors="strict")
        return FORCED_INPUT_SEPARATOR, "UTF-16LE"

    if raw.startswith(b"\xfe\xff"):
        _ = raw.decode("utf-16", errors="strict")
        return FORCED_INPUT_SEPARATOR, "UTF-16BE"

    decode_attempts = [
        ("utf-8-sig", "UTF-8"),
        ("utf-8", "UTF-8"),
        ("cp1252", "CP1252"),
        ("latin1", "ISO-8859-1"),
    ]

    text: Optional[str] = None
    chosen_encoding_for_spark: Optional[str] = None
    last_err: Optional[Exception] = None

    for py_enc, spark_enc in decode_attempts:
        try:
            text = raw.decode(py_enc, errors="strict")
            chosen_encoding_for_spark = spark_enc
            break
        except Exception as e:
            last_err = e

    if text is None or chosen_encoding_for_spark is None:
        raise RuntimeError(f"Could not decode head sample of s3://{bucket}/{key}. Last error: {last_err}")

    # Separator is forced by requirement; still return encoding discovered above
    return FORCED_INPUT_SEPARATOR, chosen_encoding_for_spark

def normalize_header(h: str) -> str:
    s = str(h)
    # Remove NULs from mis-decoded UTF-16 and remove BOM if present
    s = s.replace("\x00", "")
    s = s.replace("\ufeff", "")
    return re.sub(r"\s+", " ", s.strip().lower())

def find_column_by_normalized_name(columns: List[str], target_norm: str) -> Optional[str]:
    for c in columns:
        if normalize_header(c) == target_norm:
            return c
    return None

def make_safe_name_map(columns: List[str]) -> Dict[str, str]:
    """
    Make Spark-safe unique column names (internal only).
    """
    seen = set()
    mapping: Dict[str, str] = {}
    for c in columns:
        base = re.sub(r"[^A-Za-z0-9_]", "_", str(c).strip())
        if not base:
            base = "col"
        if base[0].isdigit():
            base = "c_" + base
        safe = base
        i = 1
        while safe in seen:
            safe = f"{base}_{i}"
            i += 1
        seen.add(safe)
        mapping[c] = safe
    return mapping

def apply_safe_columns(df: DataFrame, mapping: Dict[str, str]) -> DataFrame:
    return df.select([col(orig).alias(safe) for orig, safe in mapping.items()])

def write_single_csv(
    df: DataFrame,
    output_bucket: str,
    final_key: str,
    tmp_prefix: str,
    s3_client,
):
    """
    Spark writes CSV as a folder; this writes to tmp_prefix, copies the single part file to final_key,
    and deletes tmp objects. Output is a single TSV object (sep=TAB).
    Handles empty DataFrames by ensuring headers are written.
    """
    try:
        is_empty = df.isEmpty()
    except AttributeError:
        is_empty = df.limit(1).count() == 0

    if is_empty:
        print(f"[INFO] DataFrame is empty. Writing headers-only TSV to: s3://{output_bucket}/{final_key}")

        if not df.columns:
            print("[WARN] DataFrame has no columns. Writing empty file.")
            s3_client.put_object(
                Bucket=output_bucket,
                Key=final_key,
                Body=b"",
                ContentType="text/tab-separated-values",
            )
            return

        output = StringIO()
        writer = csv.writer(output, delimiter=FORCED_OUTPUT_SEPARATOR)
        writer.writerow(df.columns)
        header_tsv = output.getvalue()

        s3_client.put_object(
            Bucket=output_bucket,
            Key=final_key,
            Body=header_tsv.encode("utf-8"),
            ContentType="text/tab-separated-values",
        )
        return

    tmp_uri = f"s3://{output_bucket}/{tmp_prefix}"
    print(f"[INFO] Writing TSV to temporary prefix: {tmp_uri}")

    (
        df.coalesce(1)
          .write.mode("overwrite")
          .option("header", True)
          .option("sep", FORCED_OUTPUT_SEPARATOR)
          .csv(tmp_uri)
    )

    tmp_keys = list_s3_objects(output_bucket, tmp_prefix)
    part_keys = [k for k in tmp_keys if "/part-" in k and k.endswith(".csv")]

    if not part_keys:
        raise RuntimeError(f"No CSV part file found under tmp prefix '{tmp_prefix}'")

    part_keys.sort()
    part_key = part_keys[0]
    print(f"[INFO] Selected part file: s3://{output_bucket}/{part_key}")

    print(f"[INFO] Copying result to final key: s3://{output_bucket}/{final_key}")
    s3_client.copy_object(
        Bucket=output_bucket,
        CopySource={"Bucket": output_bucket, "Key": part_key},
        Key=final_key,
    )

    print(f"[INFO] Cleaning up tmp prefix: {tmp_prefix}")
    for k in tmp_keys:
        try:
            s3_client.delete_object(Bucket=output_bucket, Key=k)
        except Exception as cleanup_err:
            print(f"[WARN] Failed to delete temporary file s3://{output_bucket}/{k}: {type(cleanup_err).__name__}: {cleanup_err}")

# =========================
# Glue entry point (args)
# =========================

args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "INPUT_BUCKET",
        "OUTPUT_BUCKET",
        "process_control_type",
        "preprocessed_input_key",
        "prepared_output_prefix",
    ],
)

job_name = args["JOB_NAME"]
input_bucket = args["INPUT_BUCKET"]
output_bucket = args["OUTPUT_BUCKET"]

process_control_type = args["process_control_type"]

incoming_prefix = ensure_prefix_uri(args["preprocessed_input_key"])
result_prefix = ensure_prefix_uri(args["prepared_output_prefix"])

print(f"[INFO] Job name: {job_name}")
print(f"[INFO] INPUT_BUCKET: {input_bucket}")
print(f"[INFO] OUTPUT_BUCKET: {output_bucket}")
print(f"[INFO] process_control_type: {process_control_type}")
print(f"[INFO] incoming_prefix: {incoming_prefix}")
print(f"[INFO] result_prefix: {result_prefix}")
print(f"[INFO] Forced input separator: TAB")
print(f"[INFO] Forced output separator: TAB")

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(job_name, args)

s3_client = boto3.client("s3")

RUN_TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

try:
    # -------------------------
    # 1) Locate exactly 2 CSV files in incoming
    # -------------------------
    all_keys = list_s3_objects(input_bucket, incoming_prefix)
    csv_keys = [
        k for k in all_keys
        if k.lower().endswith(".csv") and not k.endswith("/")
    ]

    if len(csv_keys) != 2:
        raise RuntimeError(
            f"Expected exactly 2 CSV files under s3://{input_bucket}/{incoming_prefix} "
            f"but found {len(csv_keys)}. Found CSV keys: {csv_keys}"
        )

    csv_keys.sort()
    key_a, key_b = csv_keys[0], csv_keys[1]

    # Validate S3 keys before use
    validate_s3_key(key_a)
    validate_s3_key(key_b)

    base_a = basename(key_a)
    base_b = basename(key_b)

    def tag_from_name(name: str) -> str:
        n = name.lower()
        if "x1" in n:
            return "X1"
        if "x2" in n:
            return "X2"
        return "A"

    tag_a = tag_from_name(base_a)
    tag_b = tag_from_name(base_b)
    if tag_a == tag_b:
        tag_a, tag_b = "A", "B"

    print(f"[INFO] Using input A: s3://{input_bucket}/{key_a} (tag={tag_a})")
    print(f"[INFO] Using input B: s3://{input_bucket}/{key_b} (tag={tag_b})")

    # -------------------------
    # 2) Detect encoding + read CSVs (separator forced to TAB)
    # -------------------------
    sep_a, enc_a = detect_csv_dialect(input_bucket, key_a)
    sep_b, enc_b = detect_csv_dialect(input_bucket, key_b)

    print(f"[INFO] Detected A sep='TAB' encoding='{enc_a}'")
    print(f"[INFO] Detected B sep='TAB' encoding='{enc_b}'")

    uri_a = f"s3://{input_bucket}/{key_a}"
    uri_b = f"s3://{input_bucket}/{key_b}"

    df_a_raw = (
        spark.read.format("csv")
        .option("header", True)
        .option("sep", sep_a)
        .option("encoding", enc_a)
        .option("multiLine", True)
        .option("escape", "\"")
        .option("quote", "\"")
        .option("mode", "PERMISSIVE")
        .load(uri_a)
    )

    df_b_raw = (
        spark.read.format("csv")
        .option("header", True)
        .option("sep", sep_b)
        .option("encoding", enc_b)
        .option("multiLine", True)
        .option("escape", "\"")
        .option("quote", "\"")
        .option("mode", "PERMISSIVE")
        .load(uri_b)
    )

    df_a_raw = df_a_raw.toDF(*[str(c).strip() for c in df_a_raw.columns])
    df_b_raw = df_b_raw.toDF(*[str(c).strip() for c in df_b_raw.columns])

    # -------------------------
    # 3) Identify key and excluded columns by normalized header name
    # -------------------------
    KEY_NORM = "xmedia id"
    PATH_NORM = "path"

    key_col_a = find_column_by_normalized_name(df_a_raw.columns, KEY_NORM)
    key_col_b = find_column_by_normalized_name(df_b_raw.columns, KEY_NORM)
    if not key_col_a:
        raise RuntimeError(f"Key column 'xmedia ID' not found in A. Columns: {df_a_raw.columns}")
    if not key_col_b:
        raise RuntimeError(f"Key column 'xmedia ID' not found in B. Columns: {df_b_raw.columns}")

    path_col_a = find_column_by_normalized_name(df_a_raw.columns, PATH_NORM)
    path_col_b = find_column_by_normalized_name(df_b_raw.columns, PATH_NORM)

    print(f"[INFO] Key column A: '{key_col_a}', Key column B: '{key_col_b}'")
    print(f"[INFO] Path column A: '{path_col_a}', Path column B: '{path_col_b}'")

    # -------------------------
    # 4) Internal safe columns
    # -------------------------
    map_a = make_safe_name_map(df_a_raw.columns)
    map_b = make_safe_name_map(df_b_raw.columns)

    df_a = apply_safe_columns(df_a_raw, map_a)
    df_b = apply_safe_columns(df_b_raw, map_b)

    key_safe_a = map_a[key_col_a]
    key_safe_b = map_b[key_col_b]

    df_a = df_a.withColumn(key_safe_a, trim(col(key_safe_a)).cast(StringType()))
    df_b = df_b.withColumn(key_safe_b, trim(col(key_safe_b)).cast(StringType()))

    null_key_a = df_a.filter(col(key_safe_a).isNull() | (col(key_safe_a) == "")).limit(1).count()
    null_key_b = df_b.filter(col(key_safe_b).isNull() | (col(key_safe_b) == "")).limit(1).count()
    if null_key_a > 0:
        raise RuntimeError("Found null/empty 'xmedia ID' values in input A.")
    if null_key_b > 0:
        raise RuntimeError("Found null/empty 'xmedia ID' values in input B.")

    dup_a = df_a.groupBy(key_safe_a).count().filter(col("count") > 1)
    dup_b = df_b.groupBy(key_safe_b).count().filter(col("count") > 1)

    dup_a_exists = dup_a.limit(1).count() > 0
    dup_b_exists = dup_b.limit(1).count() > 0
    if dup_a_exists or dup_b_exists:
        sample_a = [r[key_safe_a] for r in dup_a.select(key_safe_a).limit(MAX_DUPLICATE_SAMPLE_COUNT).collect()] if dup_a_exists else []
        sample_b = [r[key_safe_b] for r in dup_b.select(key_safe_b).limit(MAX_DUPLICATE_SAMPLE_COUNT).collect()] if dup_b_exists else []
        raise RuntimeError(
            f"Duplicate xmedia IDs detected. "
            f"A sample={sample_a} | B sample={sample_b}. "
            f"Fix duplicates before diff (comparison requires 1 row per xmedia ID)."
        )

    KEY_SAFE = "xmedia_id"
    df_a = df_a.withColumnRenamed(key_safe_a, KEY_SAFE)
    df_b = df_b.withColumnRenamed(key_safe_b, KEY_SAFE)

    path_safe_a = map_a[path_col_a] if path_col_a else None
    path_safe_b = map_b[path_col_b] if path_col_b else None

    cols_a_safe = set(df_a.columns)
    cols_b_safe = set(df_b.columns)

    excluded = {KEY_SAFE}
    if path_safe_a and path_safe_a in cols_a_safe and path_safe_b and path_safe_b in cols_b_safe:
        df_a = df_a.withColumnRenamed(path_safe_a, "path__tmp")
        df_b = df_b.withColumnRenamed(path_safe_b, "path__tmp")
        excluded.add("path__tmp")

    comparable_cols = sorted(list((cols_a_safe & cols_b_safe) - excluded))

    cols_only_in_a = sorted(list(cols_a_safe - cols_b_safe))
    cols_only_in_b = sorted(list(cols_b_safe - cols_a_safe))

    print(f"[INFO] Comparable column count (intersection, excluding key/path): {len(comparable_cols)}")
    print(f"[INFO] Columns only in A (safe): {cols_only_in_a}")
    print(f"[INFO] Columns only in B (safe): {cols_only_in_b}")

    # -------------------------
    # 5) Missing IDs
    # -------------------------
    ids_a = df_a.select(KEY_SAFE).distinct()
    ids_b = df_b.select(KEY_SAFE).distinct()

    missing_in_a = ids_b.subtract(ids_a).withColumnRenamed(KEY_SAFE, "xmedia ID")
    missing_in_b = ids_a.subtract(ids_b).withColumnRenamed(KEY_SAFE, "xmedia ID")

    # -------------------------
    # 6) Field differences (long format)
    # -------------------------
    a_pref = "a__"
    b_pref = "b__"

    proj_a = [col(KEY_SAFE)] + [col(c).alias(a_pref + c) for c in comparable_cols]
    proj_b = [col(KEY_SAFE)] + [col(c).alias(b_pref + c) for c in comparable_cols]

    ja = df_a.select(*proj_a)
    jb = df_b.select(*proj_b)

    joined = ja.join(jb, on=KEY_SAFE, how="inner")

    NULL_MARK = "<NULL>"

    stack_parts = []
    for c in comparable_cols:
        a_expr = f"coalesce(trim(`{a_pref + c}`), '{NULL_MARK}')"
        b_expr = f"coalesce(trim(`{b_pref + c}`), '{NULL_MARK}')"
        stack_parts.append(f"'{c}', {a_expr}, {b_expr}")

    if stack_parts:
        stack_expr = f"stack({len(comparable_cols)}, {', '.join(stack_parts)}) as (field, value_a, value_b)"
        diffs_long = (
            joined
            .select(
                col(KEY_SAFE).alias("xmedia ID"),
                expr(stack_expr)
            )
            .filter(col("value_a") != col("value_b"))
        )
    else:
        diffs_long = spark.createDataFrame([], schema="`xmedia ID` string, field string, value_a string, value_b string")

    # -------------------------
    # 7) Write outputs as single TSV objects (still .csv extension)
    # -------------------------
    out_missing_in_a_key = f"{result_prefix.rstrip('/')}/missing_in_{tag_a}.csv"
    out_missing_in_b_key = f"{result_prefix.rstrip('/')}/missing_in_{tag_b}.csv"
    out_diffs_key = f"{result_prefix.rstrip('/')}/field_differences.csv"

    tmp_missing_in_a = f"{result_prefix.rstrip('/')}/_tmp_missing_in_{tag_a}_{RUN_TS}/"
    tmp_missing_in_b = f"{result_prefix.rstrip('/')}/_tmp_missing_in_{tag_b}_{RUN_TS}/"
    tmp_diffs = f"{result_prefix.rstrip('/')}/_tmp_field_differences_{RUN_TS}/"

    write_single_csv(missing_in_a, output_bucket, out_missing_in_a_key, tmp_missing_in_a, s3_client)
    write_single_csv(missing_in_b, output_bucket, out_missing_in_b_key, tmp_missing_in_b, s3_client)
    write_single_csv(diffs_long, output_bucket, out_diffs_key, tmp_diffs, s3_client)

    # -------------------------
    # 8) Run receipt (JSON)
    # -------------------------
    receipt = {
        "job_name": job_name,
        "process_control_type": process_control_type,
        "run_ts": RUN_TS,
        "input": {
            "bucket": input_bucket,
            "incoming_prefix": incoming_prefix,
            "file_a_key": key_a,
            "file_a_tag": tag_a,
            "file_a_sep": "\\t",
            "file_a_encoding": enc_a,
            "file_b_key": key_b,
            "file_b_tag": tag_b,
            "file_b_sep": "\\t",
            "file_b_encoding": enc_b,
        },
        "output": {
            "bucket": output_bucket,
            "result_prefix": result_prefix,
            "missing_in_a_key": out_missing_in_a_key,
            "missing_in_b_key": out_missing_in_b_key,
            "field_differences_key": out_diffs_key,
        },
        "schema": {
            "comparable_columns_count": len(comparable_cols),
            "columns_only_in_a_safe": cols_only_in_a,
            "columns_only_in_b_safe": cols_only_in_b,
        },
        "notes": {
            "comparison_key_header_normalized": KEY_NORM,
            "excluded_header_normalized": PATH_NORM,
            "diff_compares_intersection_only": True,
            "null_marker_in_diff": NULL_MARK,
            "forced_input_separator": "\\t",
            "forced_output_separator": "\\t",
        },
    }

    safe_pctype = re.sub(r"[^A-Za-z0-9_-]", "_", process_control_type.strip() or "process_control")
    receipt_key = f"{result_prefix.rstrip('/')}/run_receipt_{safe_pctype}_{RUN_TS}.json"

    s3_client.put_object(
        Bucket=output_bucket,
        Key=receipt_key,
        Body=json.dumps(receipt, indent=2, ensure_ascii=False).encode("utf-8"),
        ContentType="application/json",
    )
    print(f"[INFO] Wrote run receipt: s3://{output_bucket}/{receipt_key}")

    print("[INFO] Job completed successfully.")
    job.commit()

except Exception as e:
    error_type = type(e).__name__
    error_msg = str(e)

    aws_error_types = ["ClientError", "BotoCoreError", "NoCredentialsError", "PartialCredentialsError"]
    is_aws_error = error_type in aws_error_types or "boto" in error_type.lower()

    if is_aws_error:
        print(f"[ERROR] AWS Service Error ({error_type}): {error_msg}")
    else:
        print(f"[ERROR] Runtime Error ({error_type}): {error_msg}")

    print("[ERROR] Full traceback:")
    traceback.print_exc()

    job.commit()
    raise
