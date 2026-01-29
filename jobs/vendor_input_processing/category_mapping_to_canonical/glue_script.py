import sys
import os
import re
from datetime import datetime, timezone
from typing import List, Set

import boto3
from botocore.exceptions import ClientError

from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

from pyspark.sql.functions import (
    col,
    struct,
    collect_list,
    explode_outer,
    first,
    lit,
    when,
    explode,
    size,
)
from pyspark.sql.types import ArrayType, IntegerType, StructType, StructField, StringType
from pyspark.sql.functions import udf

# ---------- Helpers ----------


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9ÄÖÜäöüß]+")
TRIM_PATTERN = re.compile(r"^[^A-Za-z0-9ÄÖÜäöüß]+|[^A-Za-z0-9ÄÖÜäöüß]+$")

MIN_TOKEN_LENGTH = 3
DROP_NUMERIC_ONLY_FIELDS = ["KEYWORD", "DESCRIPTION_SHORT"]
STOPWORDS_DE_V1: List[str] = [
    "und",
    "oder",
    "mit",
    "ohne",
    "für",
    "zum",
    "zur",
    "im",
    "in",
    "am",
    "an",
    "auf",
    "aus",
    "bei",
    "von",
    "vom",
    "der",
    "die",
    "das",
    "den",
    "dem",
    "des",
    "ein",
    "eine",
    "einer",
    "eines",
    "einem",
    "einen",
    "ist",
    "sind",
]

GERMAN_CHAR_MAP = str.maketrans({
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
    "Ä": "ae",
    "Ö": "oe",
    "Ü": "ue",
})


def normalize_german_chars(token: str) -> str:
    return token.translate(GERMAN_CHAR_MAP).lower()


def build_stopword_set() -> Set[str]:
    stopwords: Set[str] = set()
    for stopword in STOPWORDS_DE_V1:
        normalized = normalize_german_chars(stopword)
        stopwords.add(normalized)
    return stopwords


def tokenize_text_value(value, field_name: str, stopwords: Set[str]) -> List[str]:
    if value is None:
        return []
    if not isinstance(value, str):
        value = str(value)
    if not value:
        return []

    normalized_tokens: List[str] = []
    for token in TOKEN_PATTERN.findall(value):
        trimmed = TRIM_PATTERN.sub("", token)
        if not trimmed:
            continue
        normalized = normalize_german_chars(trimmed)
        if not normalized:
            continue
        numeric_only_candidate = re.sub(r"[^0-9]", "", normalized)
        if (
            field_name in DROP_NUMERIC_ONLY_FIELDS
            and numeric_only_candidate
            and len(numeric_only_candidate) == len(normalized)
        ):
            continue
        if len(normalized) < MIN_TOKEN_LENGTH:
            continue
        if normalized in stopwords:
            continue
        normalized_tokens.append(normalized)
    return normalized_tokens


def tokenize_keywords(keywords, stopwords: Set[str]) -> List[str]:
    tokens: List[str] = []
    if isinstance(keywords, list):
        for keyword in keywords:
            if isinstance(keyword, str):
                tokens.extend(tokenize_text_value(keyword, "KEYWORD", stopwords))
    return tokens


def tokenize_description(description_short, stopwords: Set[str]) -> List[str]:
    if isinstance(description_short, str):
        return tokenize_text_value(description_short, "DESCRIPTION_SHORT", stopwords)
    return []


def normalize_class_code_system(system: str) -> str:
    normalized_system = normalize_german_chars(str(system)).lower()
    if normalized_system.startswith("eclass"):
        return "eclass-5.1"
    if normalized_system.startswith("etim-"):
        return normalized_system
    if normalized_system.startswith("etim"):
        return "etim"
    return normalized_system


def tokenize_class_codes(class_codes) -> List[str]:
    tokens: List[str] = []
    if isinstance(class_codes, list):
        for entry in class_codes:
            if entry is None:
                continue
            entry_dict = None
            if isinstance(entry, dict):
                entry_dict = entry
            elif hasattr(entry, "asDict"):
                try:
                    entry_dict = entry.asDict(recursive=True)
                except Exception:
                    entry_dict = None
            else:
                try:
                    entry_dict = {
                        "system": entry["system"],
                        "code": entry["code"],
                    }
                except Exception:
                    entry_dict = None

            if not entry_dict:
                continue

            system = entry_dict.get("system")
            code = entry_dict.get("code")
            if system is None or code is None:
                continue
            normalized_system = normalize_class_code_system(system)
            code_str = str(code).strip()
            if not code_str:
                continue
            tokens.append(f"{normalized_system}:{code_str}")
    return tokens


def normalize_rule_tokens(values, field_name: str, stopwords: Set[str]) -> List[str]:
    """
    Turn mapping_method values into normalized tokens using the SAME tokenization rules.
    This intentionally supports older/manual rule values like 'Akku-Bohrer' by splitting it.
    """
    tokens: List[str] = []
    if not values:
        return tokens
    for v in values:
        tokens.extend(tokenize_text_value(v, field_name, stopwords))
    return tokens


def normalize_class_code_rule_tokens(values) -> List[str]:
    tokens: List[str] = []
    if not values:
        return tokens
    for v in values:
        if v is None:
            continue
        value_str = str(v).strip()
        if not value_str:
            continue
        if ":" in value_str:
            system_part, code_part = value_str.split(":", 1)
            system_norm = normalize_class_code_system(system_part)
            code_norm = code_part.strip()
            if not code_norm:
                continue
            tokens.append(f"{system_norm}:{code_norm}")
        else:
            tokens.append(normalize_class_code_system(value_str))
    return tokens


def ensure_prefix_uri(uri: str) -> str:
    """
    Ensure that an S3 URI prefix ends with a slash.
    Example: "path/to/prefix" -> "path/to/prefix/".
    """
    if uri.endswith("/"):
        return uri
    return uri + "/"


def list_s3_objects(bucket: str, prefix: str):
    """
    List all S3 object keys under a given prefix.
    """
    s3_client = boto3.client("s3")
    keys = []
    continuation_token = None

    print(f"[INFO] Listing S3 objects in bucket='{bucket}', prefix='{prefix}'")

    while True:
        list_kwargs = {
            "Bucket": bucket,
            "Prefix": prefix,
        }
        if continuation_token:
            list_kwargs["ContinuationToken"] = continuation_token

        response = s3_client.list_objects_v2(**list_kwargs)
        for item in response.get("Contents", []):
            keys.append(item["Key"])

        if response.get("IsTruncated"):
            continuation_token = response.get("NextContinuationToken")
        else:
            break

    print(f"[INFO] Found {len(keys)} object(s) under prefix '{prefix}'")
    return keys


def select_latest_category_mapping_key(bucket: str) -> str:
    """
    Find the newest Category_Mapping_Reference_<timestamp>.json in
    INPUT_BUCKET/canonical_mappings/, based on the timestamp in the filename.

    Returns the S3 key (without bucket). Raises RuntimeError if none found.
    """
    prefix = "canonical_mappings/"
    all_keys = list_s3_objects(bucket, prefix)

    candidates = []
    for k in all_keys:
        fname = k.split("/")[-1]
        if not fname.startswith("Category_Mapping_Reference_"):
            continue
        if not fname.endswith(".json"):
            continue
        # Extract the <timestamp> between prefix and ".json"
        base = fname[len("Category_Mapping_Reference_"):]
        ts_str, ext = os.path.splitext(base)
        if ts_str:
            candidates.append((ts_str, k))

    if not candidates:
        raise RuntimeError(
            f"No Category_Mapping_Reference_<timestamp>.json found under "
            f"s3://{bucket}/{prefix}"
        )

    # Sort by timestamp string (YYYYMMDD[...]) – lexical order matches time order
    candidates.sort(key=lambda x: x[0])
    latest_ts, latest_key = candidates[-1]

    print(
        f"[INFO] Selected latest Category_Mapping_Reference file: "
        f"s3://{bucket}/{latest_key} (timestamp={latest_ts})"
    )
    return latest_key


# ---------- Glue entry point ----------

# EXACTLY the arguments described:
# - from job configuration: JOB_NAME, INPUT_BUCKET, OUTPUT_BUCKET
# - from Lambda/Make: vendor_name, preprocessed_input_key, prepared_output_prefix
args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "INPUT_BUCKET",
        "OUTPUT_BUCKET",
        "vendor_name",
        "preprocessed_input_key",
        "prepared_output_prefix",
    ],
)

job_name = args["JOB_NAME"]
input_bucket = args["INPUT_BUCKET"]
output_bucket = args["OUTPUT_BUCKET"]

vendor_name = args["vendor_name"]
preprocessed_input_prefix = ensure_prefix_uri(args["preprocessed_input_key"])
prepared_output_prefix = ensure_prefix_uri(args["prepared_output_prefix"])

print(f"[INFO] Job name: {job_name}")
print(f"[INFO] INPUT_BUCKET: {input_bucket}")
print(f"[INFO] OUTPUT_BUCKET: {output_bucket}")
print(f"[INFO] vendor_name: {vendor_name}")
print(f"[INFO] preprocessed_input_prefix: {preprocessed_input_prefix}")
print(f"[INFO] prepared_output_prefix: {prepared_output_prefix}")

sc = SparkContext()
glue_context = GlueContext(sc)
spark = glue_context.spark_session

job = Job(glue_context)
job.init(job_name, args)

s3_client = boto3.client("s3")
stopwords_for_filtering = build_stopword_set()

try:
    # =========================================================
    # PART-1 (unchanged): build <VENDOR_NAME>_forMapping_products
    # =========================================================
    print("[INFO] ===== PART-1: Building vendor_mappings on products =====")

    # -------------------------
    # 1) Locate and load input files
    # -------------------------
    all_keys = list_s3_objects(input_bucket, preprocessed_input_prefix)

    # Expected file names (suffixes) under preprocessed_input_prefix
    vendor_products_suffix = f"{vendor_name}_vendor_products.json"
    product_links_suffix = f"{vendor_name}_product_category_links.json"
    vendor_categories_suffix = f"{vendor_name}_vendor_categories.json"

    vendor_products_keys = [
        k for k in all_keys if k.endswith(vendor_products_suffix)
    ]
    product_links_keys = [
        k for k in all_keys if k.endswith(product_links_suffix)
    ]
    vendor_categories_keys = [
        k for k in all_keys if k.endswith(vendor_categories_suffix)
    ]

    if not vendor_products_keys:
        raise RuntimeError(
            f"No '{vendor_products_suffix}' file found under "
            f"s3://{input_bucket}/{preprocessed_input_prefix}"
        )
    if not product_links_keys:
        raise RuntimeError(
            f"No '{product_links_suffix}' file found under "
            f"s3://{input_bucket}/{preprocessed_input_prefix}"
        )
    if not vendor_categories_keys:
        raise RuntimeError(
            f"No '{vendor_categories_suffix}' file found under "
            f"s3://{input_bucket}/{preprocessed_input_prefix}"
        )

    # If multiple files match, pick the first sorted one (deterministic)
    vendor_products_keys.sort()
    product_links_keys.sort()
    vendor_categories_keys.sort()

    vendor_products_key = vendor_products_keys[0]
    product_links_key = product_links_keys[0]
    vendor_categories_key = vendor_categories_keys[0]

    vendor_products_uri = f"s3://{input_bucket}/{vendor_products_key}"
    product_links_uri = f"s3://{input_bucket}/{product_links_key}"
    vendor_categories_uri = f"s3://{input_bucket}/{vendor_categories_key}"

    print(f"[INFO] Using vendor products file: {vendor_products_uri}")
    print(f"[INFO] Using product-category links file: {product_links_uri}")
    print(f"[INFO] Using vendor categories file: {vendor_categories_uri}")

    vendor_products_df = spark.read.json(vendor_products_uri)
    print(f"[INFO] Loaded vendor_products_df with {vendor_products_df.count()} rows")

    product_links_df = spark.read.json(product_links_uri)
    print(f"[INFO] Loaded product_category_links_df with {product_links_df.count()} rows")

    vendor_categories_df = spark.read.json(vendor_categories_uri)
    print(f"[INFO] Loaded vendor_categories_df with {vendor_categories_df.count()} rows")

    # -------------------------
    # 2) Build mappings: article_id + category_id + category metadata
    # -------------------------
    # Join product_category_links with vendor_categories on vendor_name + category_id
    # so that for each (article_id, vendor_category_id) we get category_name/path/type.
    links_with_cat_df = (
        product_links_df.alias("l")
        .join(
            vendor_categories_df.alias("c"),
            (col("l.vendor_name") == col("c.vendor_name"))
            & (col("l.vendor_category_id") == col("c.category_id")),
            how="left",
        )
    )

    print(
        "[INFO] links_with_cat_df rows after join: "
        f"{links_with_cat_df.count()}"
    )

    # Build the mapping struct in the exact format requested:
    # "vendor_mappings": [
    #   {
    #     "vendor_short_name": vendor_products.vendor_name,
    #     "vendor_category_id": product_category_links.vendor_category_id,
    #     "vendor_category_name": vendor_categories.category_name,
    #     "vendor_category_path": vendor_categories.category_path,
    #     "vendor_category_type": vendor_categories.type
    #   }
    # ]
    mapping_struct_col = struct(
        col("l.vendor_name").alias("vendor_short_name"),
        col("l.vendor_category_id").alias("vendor_category_id"),
        col("c.category_name").alias("vendor_category_name"),
        col("c.category_path").alias("vendor_category_path"),
        col("c.type").alias("vendor_category_type"),
    ).alias("mapping")

    # Only keep combinations where we actually have a vendor_category_id
    mappings_df = (
        links_with_cat_df.where(col("l.vendor_category_id").isNotNull())
        .select(
            col("l.vendor_name").alias("vendor_name"),
            col("l.article_id").alias("article_id"),
            mapping_struct_col,
        )
    )

    print(
        f"[INFO] mappings_df rows (article/category combinations): "
        f"{mappings_df.count()}"
    )

    # Aggregate mappings per (vendor_name, article_id) into vendor_mappings array
    aggregated_mappings_df = (
        mappings_df.groupBy("vendor_name", "article_id")
        .agg(collect_list("mapping").alias("vendor_mappings"))
    )

    print(
        "[INFO] aggregated_mappings_df rows (distinct vendor_name/article_id): "
        f"{aggregated_mappings_df.count()}"
    )

    # -------------------------
    # 3) Extend vendor_products with vendor_mappings
    # -------------------------
    # "rest of the product record is taken over from vendor_products as is"
    extended_products_df = (
        vendor_products_df.alias("p")
        .join(
            aggregated_mappings_df.alias("m"),
            on=["vendor_name", "article_id"],
            how="left",
        )
    )

    print(f"[INFO] extended_products_df rows: {extended_products_df.count()}")

    # -------------------------
    # 4) Write NDJSON output to prepared_output_prefix
    # -------------------------
    timestamp_part1 = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    # Temporary prefix in OUTPUT_BUCKET to handle coalesce(1)
    tmp_key_prefix_part1 = (
        f"{prepared_output_prefix.rstrip('/')}/"
        f"_tmp_{vendor_name}_forMapping_products_{timestamp_part1}/"
    )
    tmp_uri_part1 = f"s3://{output_bucket}/{tmp_key_prefix_part1}"

    print(f"[INFO] Writing PART-1 NDJSON to temporary prefix: {tmp_uri_part1}")

    (
        extended_products_df.toJSON()  # 1 JSON object per line
        .coalesce(1)  # single output part file
        .saveAsTextFile(tmp_uri_part1)
    )

    # Locate the part file
    tmp_keys_part1 = list_s3_objects(output_bucket, tmp_key_prefix_part1)
    part_keys_part1 = [k for k in tmp_keys_part1 if "/part-" in k]

    if not part_keys_part1:
        raise RuntimeError(
            f"No part files found in temporary output prefix '{tmp_key_prefix_part1}'"
        )

    part_keys_part1.sort()
    part_key_part1 = part_keys_part1[0]
    print(
        f"[INFO] Selected PART-1 part file: s3://{output_bucket}/{part_key_part1}"
    )

    # Final keys: primary uses explicit .ndjson extension; legacy kept for backward compatibility
    final_key_primary = (
        f"{prepared_output_prefix.rstrip('/')}/{vendor_name}_forMapping_products.ndjson"
    )
    final_key_legacy = (
        f"{prepared_output_prefix.rstrip('/')}/{vendor_name}_forMapping_products"
    )
    print(
        "[INFO] Copying PART-1 result to final output (primary): "
        f"s3://{output_bucket}/{final_key_primary}"
    )

    # Copy part file to final primary key
    s3_client.copy_object(
        Bucket=output_bucket,
        CopySource={"Bucket": output_bucket, "Key": part_key_part1},
        Key=final_key_primary,
    )

    # Also copy to legacy key if different
    if final_key_legacy != final_key_primary:
        print(
            "[INFO] Copying PART-1 result to final output (legacy): "
            f"s3://{output_bucket}/{final_key_legacy}"
        )
        s3_client.copy_object(
            Bucket=output_bucket,
            CopySource={"Bucket": output_bucket, "Key": part_key_part1},
            Key=final_key_legacy,
        )

    # Cleanup temporary folder (non-fatal)
    print(f"[INFO] Cleaning up PART-1 temporary prefix: {tmp_key_prefix_part1}")
    for k in tmp_keys_part1:
        try:
            s3_client.delete_object(Bucket=output_bucket, Key=k)
        except Exception as cleanup_err:
            print(f"[WARN] Failed to delete temporary file s3://{output_bucket}/{k}: {cleanup_err}")

    # =========================================================
    # PART-2: enrich with existing canonical mappings
    # =========================================================
    print("[INFO] ===== PART-2: Enriching with existing category mappings =====")

    for_mapping_uri = f"s3://{output_bucket}/{final_key_primary}"
    print(f"[INFO] Reading for-mapping products from: {for_mapping_uri}")

    # This is NDJSON (one JSON per line), so standard read.json works
    for_mapping_df = spark.read.json(for_mapping_uri)
    print(f"[INFO] Loaded for_mapping_df with {for_mapping_df.count()} rows")

    mapping_ref_df = None  # will stay None if no mapping reference exists

    # Try to find latest Category_Mapping_Reference_<timestamp>.json.
    # If none exists, we still add empty columns but do NOT fail the job.
    try:
        mapping_ref_key = select_latest_category_mapping_key(input_bucket)
        mapping_ref_uri = f"s3://{input_bucket}/{mapping_ref_key}"
        print(f"[INFO] Reading Category Mapping Reference from: {mapping_ref_uri}")

        # The reference file is a normal JSON file with objects containing:
        # pim_category_id, pim_category_name, vendor_mappings[], mapping_methods[]
        # We enable multiLine to be robust against pretty-printed JSON.
        mapping_ref_df = (
            spark.read.option("multiLine", True).json(mapping_ref_uri)
        )

        print(
            "[INFO] Loaded mapping_ref_df with "
            f"{mapping_ref_df.count()} rows (PIM categories)"
        )

        # Flatten vendor_mappings array so we have one row per (vendor_short_name, vendor_category_id)
        mapping_flat_df = (
            mapping_ref_df.select(
                explode_outer("vendor_mappings").alias("vm"),
                col("pim_category_id"),
                col("pim_category_name"),
            )
            .where(col("vm").isNotNull())
            .select(
                col("vm.vendor_short_name").alias("vendor_short_name"),
                col("vm.vendor_category_id").alias("vendor_category_id"),
                col("pim_category_id"),
                col("pim_category_name"),
            )
        )

        print(
            "[INFO] mapping_flat_df rows (vendor-category to PIM mappings): "
            f"{mapping_flat_df.count()}"
        )

        # If there are no rows for this vendor, mapping_flat_df may be empty;
        # we handle that gracefully.
        if mapping_flat_df.rdd.isEmpty():
            print(
                "[WARN] mapping_flat_df is empty (no vendor/category mappings found "
                "in reference); products will get empty PIM fields."
            )
            enriched_df = (
                for_mapping_df.withColumn("pim_category_id", lit(None).cast("string"))
                .withColumn("pim_category_name", lit(None).cast("string"))
                .withColumn("assignment_source", lit(None).cast("string"))
                .withColumn("assignment_confidence", lit(None).cast("string"))
            )
        else:
            # Explode vendor_mappings in products to (vendor_name, article_id, vendor_short_name, vendor_category_id)
            products_exploded_df = (
                for_mapping_df.select(
                    col("vendor_name"),
                    col("article_id"),
                    col("vendor_mappings"),
                    explode_outer("vendor_mappings").alias("vm"),
                )
            )

            print(
                "[INFO] products_exploded_df rows (vendor-mapping combinations): "
                f"{products_exploded_df.count()}"
            )

            # Join exploded products with mapping_flat_df on vendor_short_name + vendor_category_id
            joined_df = (
                products_exploded_df.join(
                    mapping_flat_df,
                    (
                        col("vm.vendor_short_name")
                        == col("vendor_short_name")
                    )
                    & (
                        col("vm.vendor_category_id")
                        == col("vendor_category_id")
                    ),
                    how="left",
                )
            )

            print(
                "[INFO] joined_df rows after join to mapping_flat_df: "
                f"{joined_df.count()}"
            )

            # For each product (vendor_name, article_id), pick first matching PIM category
            product_pim_df = (
                joined_df.groupBy("vendor_name", "article_id")
                .agg(
                    first("pim_category_id", ignorenulls=True).alias(
                        "pim_category_id"
                    ),
                    first("pim_category_name", ignorenulls=True).alias(
                        "pim_category_name"
                    ),
                )
            )

            print(
                "[INFO] product_pim_df rows (products with possible PIM mapping): "
                f"{product_pim_df.count()}"
            )

            # Join back to full product records, keep vendor_mappings as in Part-1
            enriched_df = (
                for_mapping_df.alias("p")
                .join(
                    product_pim_df.alias("pm"),
                    on=["vendor_name", "article_id"],
                    how="left",
                )
            )

            # Add assignment_source and assignment_confidence only if we have a PIM mapping
            enriched_df = (
                enriched_df
                .withColumn(
                    "assignment_source",
                    when(
                        col("pim_category_id").isNotNull(),
                        lit("existing_category_match")
                    ).otherwise(lit(None).cast("string"))
                )
                .withColumn(
                    "assignment_confidence",
                    when(
                        col("pim_category_id").isNotNull(),
                        lit("full")
                    ).otherwise(lit(None).cast("string"))
                )
            )

    except RuntimeError as e:
        # No Category_Mapping_Reference file found – do NOT fail the job, just add empty columns
        print(
            "[WARN] No Category_Mapping_Reference file found; "
            "products will get empty PIM fields. Details: "
            f"{e}"
        )
        enriched_df = (
            for_mapping_df.withColumn("pim_category_id", lit(None).cast("string"))
            .withColumn("pim_category_name", lit(None).cast("string"))
            .withColumn("assignment_source", lit(None).cast("string"))
            .withColumn("assignment_confidence", lit(None).cast("string"))
        )

    print(f"[INFO] enriched_df rows (post PART-2 products): {enriched_df.count()}")

    # =========================================================
    # PART-3: Rule-based matching for unmapped products
    # =========================================================
    print("[INFO] ===== PART-3: Rule-based matching across DESCRIPTION_SHORT, KEYWORD, CLASS_CODES =====")

    if mapping_ref_df is None:
        print("[WARN] mapping_ref_df is None; skipping PART-3 (no mapping_methods available).")
        final_df = enriched_df
    else:
        mapping_records = (
            mapping_ref_df
            .select("pim_category_id", "pim_category_name", "mapping_methods")
            .collect()
        )

        mapping_methods_lookup_ds = []
        mapping_methods_lookup_kw = []
        mapping_methods_lookup_cc = []

        for row in mapping_records:
            pim_id = row["pim_category_id"]
            pim_name = row["pim_category_name"]
            methods = row["mapping_methods"] or []

            ds_methods = []
            kw_methods = []
            cc_methods = []

            for m in methods:
                if m is None:
                    continue
                if hasattr(m, "asDict"):
                    try:
                        m = m.asDict(recursive=True)
                    except Exception:
                        pass
                m_dict = m if isinstance(m, dict) else {
                    "field_name": m["field_name"],
                    "operator": m["operator"],
                    "values_include": m.get("values_include"),
                    "values_exclude": m.get("values_exclude"),
                }
                field_name = m_dict.get("field_name")
                operator = m_dict.get("operator")
                values_include = m_dict.get("values_include")
                values_exclude = m_dict.get("values_exclude")

                if field_name == "DESCRIPTION_SHORT":
                    ds_methods.append({
                        "operator": operator,
                        "include_tokens": normalize_rule_tokens(
                            values_include or [],
                            "DESCRIPTION_SHORT",
                            stopwords_for_filtering,
                        ),
                        "exclude_tokens": normalize_rule_tokens(
                            values_exclude or [],
                            "DESCRIPTION_SHORT",
                            stopwords_for_filtering,
                        ),
                    })
                elif field_name == "KEYWORD":
                    kw_methods.append({
                        "operator": operator,
                        "include_tokens": normalize_rule_tokens(
                            values_include or [],
                            "KEYWORD",
                            stopwords_for_filtering,
                        ),
                        "exclude_tokens": normalize_rule_tokens(
                            values_exclude or [],
                            "KEYWORD",
                            stopwords_for_filtering,
                        ),
                    })
                elif field_name == "CLASS_CODES":
                    cc_methods.append({
                        "operator": operator,
                        "include_tokens": normalize_class_code_rule_tokens(values_include or []),
                        "exclude_tokens": normalize_class_code_rule_tokens(values_exclude or []),
                    })

            if ds_methods:
                mapping_methods_lookup_ds.append({
                    "pim_category_id": pim_id,
                    "pim_category_name": pim_name,
                    "methods": ds_methods,
                })

            if kw_methods:
                mapping_methods_lookup_kw.append({
                    "pim_category_id": pim_id,
                    "pim_category_name": pim_name,
                    "methods": kw_methods,
                })

            if cc_methods:
                mapping_methods_lookup_cc.append({
                    "pim_category_id": pim_id,
                    "pim_category_name": pim_name,
                    "methods": cc_methods,
                })

        if not (mapping_methods_lookup_ds or mapping_methods_lookup_kw or mapping_methods_lookup_cc):
            print("[WARN] No mapping_methods found for DESCRIPTION_SHORT, KEYWORD, or CLASS_CODES; skipping PART-3.")
            final_df = enriched_df
        else:
            print(f"[INFO] Found DESCRIPTION_SHORT mapping_methods for {len(mapping_methods_lookup_ds)} PIM categories.")
            print(f"[INFO] Found KEYWORD mapping_methods for {len(mapping_methods_lookup_kw)} PIM categories.")
            print(f"[INFO] Found CLASS_CODES mapping_methods for {len(mapping_methods_lookup_cc)} PIM categories.")

            signal_result_schema = StructType([
                StructField("pim_ids", ArrayType(StringType()), True),
                StructField("pim_names", ArrayType(StringType()), True),
                StructField("counts", ArrayType(IntegerType()), True),
            ])

            def method_matches_description_tokens(text_tokens: Set[str], raw_text, method: dict) -> bool:
                op = (method.get("operator") or "").lower()
                inc_tokens = method.get("include_tokens") or []
                exc_tokens = method.get("exclude_tokens") or []

                def contains_any(tokens):
                    return bool(tokens) and any(t in text_tokens for t in tokens)

                def contains_all(tokens):
                    return bool(tokens) and all(t in text_tokens for t in tokens)

                def has_any(tokens):
                    return bool(tokens) and any(t in text_tokens for t in tokens)

                def has_all(tokens):
                    return bool(tokens) and all(t in text_tokens for t in tokens)

                if op == "contains_any":
                    return contains_any(inc_tokens)

                if op == "contains_all":
                    return contains_all(inc_tokens)

                if op == "contains_any_exclude_any":
                    if not contains_any(inc_tokens):
                        return False
                    return not has_any(exc_tokens)

                if op == "contains_any_exclude_all":
                    if not contains_any(inc_tokens):
                        return False
                    if not exc_tokens:
                        return True
                    return not has_all(exc_tokens)

                if op == "contains_all_exclude_any":
                    if not contains_all(inc_tokens):
                        return False
                    return not has_any(exc_tokens)

                if op == "contains_all_exclude_all":
                    if not contains_all(inc_tokens):
                        return False
                    if not exc_tokens:
                        return True
                    return not has_all(exc_tokens)

                if op == "starts_with":
                    if not inc_tokens:
                        return False
                    normalized_text = normalize_german_chars(str(raw_text))
                    return any(normalized_text.startswith(t) for t in inc_tokens)

                return False

            def method_matches_keywords_tokens(keyword_tokens: Set[str], keywords_raw, method: dict) -> bool:
                op = (method.get("operator") or "").lower()
                inc_tokens = method.get("include_tokens") or []
                exc_tokens = method.get("exclude_tokens") or []

                def contains_any(tokens):
                    return bool(tokens) and any(t in keyword_tokens for t in tokens)

                def contains_all(tokens):
                    return bool(tokens) and all(t in keyword_tokens for t in tokens)

                def has_any(tokens):
                    return bool(tokens) and any(t in keyword_tokens for t in tokens)

                def has_all(tokens):
                    return bool(tokens) and all(t in keyword_tokens for t in tokens)

                if op == "contains_any":
                    return contains_any(inc_tokens)

                if op == "contains_all":
                    return contains_all(inc_tokens)

                if op == "contains_any_exclude_any":
                    if not contains_any(inc_tokens):
                        return False
                    return not has_any(exc_tokens)

                if op == "contains_any_exclude_all":
                    if not contains_any(inc_tokens):
                        return False
                    if not exc_tokens:
                        return True
                    return not has_all(exc_tokens)

                if op == "contains_all_exclude_any":
                    if not contains_all(inc_tokens):
                        return False
                    return not has_any(exc_tokens)

                if op == "contains_all_exclude_all":
                    if not contains_all(inc_tokens):
                        return False
                    if not exc_tokens:
                        return True
                    return not has_all(exc_tokens)

                if op == "starts_with":
                    if not inc_tokens:
                        return False
                    normalized_keywords = [
                        normalize_german_chars(str(k))
                        for k in (keywords_raw or [])
                        if k is not None
                    ]
                    return any(
                        any(n_kw.startswith(t) for n_kw in normalized_keywords)
                        for t in inc_tokens
                    )

                return False

            def method_matches_class_codes_tokens(cc_tokens: Set[str], method: dict) -> bool:
                op = (method.get("operator") or "").lower()
                inc_tokens = method.get("include_tokens") or []
                exc_tokens = method.get("exclude_tokens") or []

                def contains_any(tokens):
                    return bool(tokens) and any(t in cc_tokens for t in tokens)

                def contains_all(tokens):
                    return bool(tokens) and all(t in cc_tokens for t in tokens)

                def has_any(tokens):
                    return bool(tokens) and any(t in cc_tokens for t in tokens)

                def has_all(tokens):
                    return bool(tokens) and all(t in cc_tokens for t in tokens)

                if op == "contains_any":
                    return contains_any(inc_tokens)

                if op == "contains_all":
                    return contains_all(inc_tokens)

                if op == "contains_any_exclude_any":
                    if not contains_any(inc_tokens):
                        return False
                    return not has_any(exc_tokens)

                if op == "contains_any_exclude_all":
                    if not contains_any(inc_tokens):
                        return False
                    if not exc_tokens:
                        return True
                    return not has_all(exc_tokens)

                if op == "contains_all_exclude_any":
                    if not contains_all(inc_tokens):
                        return False
                    return not has_any(exc_tokens)

                if op == "contains_all_exclude_all":
                    if not contains_all(inc_tokens):
                        return False
                    if not exc_tokens:
                        return True
                    return not has_all(exc_tokens)

                return False

            def dict_to_sorted_lists(cat_counts):
                if not cat_counts:
                    return ([], [], [])
                pim_ids_sorted = sorted(cat_counts.keys())
                pim_names_sorted = [cat_counts[p][1] for p in pim_ids_sorted]
                counts_sorted = [cat_counts[p][0] for p in pim_ids_sorted]
                return (pim_ids_sorted, pim_names_sorted, counts_sorted)

            def evaluate_description_short(description_short: str, assignment_source: str):
                if assignment_source == "existing_category_match":
                    return ([], [], [])

                text_tokens = set(tokenize_description(description_short, stopwords_for_filtering))
                if not text_tokens:
                    return ([], [], [])

                cat_counts = {}
                for entry in mapping_methods_lookup_ds:
                    pim_id = entry["pim_category_id"]
                    pim_name = entry["pim_category_name"]
                    methods = entry["methods"]

                    count = 0
                    for m in methods:
                        if method_matches_description_tokens(text_tokens, description_short, m):
                            count += 1

                    if count > 0:
                        cat_counts[pim_id] = (count, pim_name)

                return dict_to_sorted_lists(cat_counts)

            def evaluate_keywords(keywords, assignment_source: str):
                if assignment_source == "existing_category_match":
                    return ([], [], [])

                kw_tokens = set(tokenize_keywords(keywords, stopwords_for_filtering))
                if not kw_tokens:
                    return ([], [], [])

                cat_counts = {}
                for entry in mapping_methods_lookup_kw:
                    pim_id = entry["pim_category_id"]
                    pim_name = entry["pim_category_name"]
                    methods = entry["methods"]

                    count = 0
                    for m in methods:
                        if method_matches_keywords_tokens(kw_tokens, keywords, m):
                            count += 1

                    if count > 0:
                        cat_counts[pim_id] = (count, pim_name)

                return dict_to_sorted_lists(cat_counts)

            def evaluate_class_codes(class_codes, assignment_source: str):
                if assignment_source == "existing_category_match":
                    return ([], [], [])

                cc_tokens = set(tokenize_class_codes(class_codes))
                if not cc_tokens:
                    return ([], [], [])

                cat_counts = {}
                for entry in mapping_methods_lookup_cc:
                    pim_id = entry["pim_category_id"]
                    pim_name = entry["pim_category_name"]
                    methods = entry["methods"]

                    count = 0
                    for m in methods:
                        if method_matches_class_codes_tokens(cc_tokens, m):
                            count += 1

                    if count > 0:
                        cat_counts[pim_id] = (count, pim_name)

                return dict_to_sorted_lists(cat_counts)

            def count_class_code_tokens(class_codes):
                return len(tokenize_class_codes(class_codes))

            ds_udf = udf(evaluate_description_short, signal_result_schema)
            kw_udf = udf(evaluate_keywords, signal_result_schema)
            cc_udf = udf(evaluate_class_codes, signal_result_schema)
            cc_token_count_udf = udf(count_class_code_tokens, IntegerType())

            if "keywords" not in enriched_df.columns:
                enriched_df = enriched_df.withColumn(
                    "keywords",
                    lit([]).cast(ArrayType(StringType()))
                )

            with_signals_df = (
                enriched_df
                .withColumn(
                    "ds_result",
                    ds_udf(col("description_short"), col("assignment_source"))
                )
                .withColumn(
                    "kw_result",
                    kw_udf(col("keywords"), col("assignment_source"))
                )
                .withColumn(
                    "cc_result",
                    cc_udf(col("class_codes"), col("assignment_source"))
                )
                .withColumn(
                    "cc_tokens_count",
                    cc_token_count_udf(col("class_codes"))
                )
            )

            final_result_schema = StructType([
                StructField("pim_category_id_final", StringType(), True),
                StructField("pim_category_name_final", StringType(), True),
                StructField("assignment_source_final", StringType(), True),
                StructField("assignment_confidence_final", StringType(), True),
            ])

            source_map = {
                frozenset({"code_class"}): "code_class_match",
                frozenset({"description_short"}): "description_short_match",
                frozenset({"keyword"}): "keyword_match",
                frozenset({"code_class", "description_short"}): "code_class_and_description_short_match",
                frozenset({"code_class", "keyword"}): "code_class_and_keyword_match",
                frozenset({"description_short", "keyword"}): "description_short_and_keyword_match",
                frozenset({"code_class", "description_short", "keyword"}): "code_class_and_description_short_and_keyword_match",
            }

            def build_count_lookup(ids, names, counts):
                lookup = {}
                if ids is None:
                    return lookup
                for pid, name, cnt in zip(ids, names or [], counts or []):
                    lookup[pid] = (cnt, name)
                return lookup

            def pick_name_for_id(target_id, lookups):
                for lookup in lookups:
                    if target_id in lookup and lookup[target_id][1]:
                        return lookup[target_id][1]
                return target_id

            def finalize_assignment(
                pim_category_id,
                pim_category_name,
                assignment_source,
                assignment_confidence,
                ds_result,
                kw_result,
                cc_result,
            ):
                if assignment_source == "existing_category_match":
                    return (
                        pim_category_id,
                        pim_category_name,
                        assignment_source,
                        assignment_confidence,
                    )

                ds_ids = (ds_result["pim_ids"] if ds_result else []) or []
                kw_ids = (kw_result["pim_ids"] if kw_result else []) or []
                cc_ids = (cc_result["pim_ids"] if cc_result else []) or []

                ds_names = (ds_result["pim_names"] if ds_result else []) or []
                kw_names = (kw_result["pim_names"] if kw_result else []) or []
                cc_names = (cc_result["pim_names"] if cc_result else []) or []

                ds_counts = (ds_result["counts"] if ds_result else []) or []
                kw_counts = (kw_result["counts"] if kw_result else []) or []
                cc_counts = (cc_result["counts"] if cc_result else []) or []

                ds_lookup = build_count_lookup(ds_ids, ds_names, ds_counts)
                kw_lookup = build_count_lookup(kw_ids, kw_names, kw_counts)
                cc_lookup = build_count_lookup(cc_ids, cc_names, cc_counts)

                ds_set = set(ds_lookup.keys())
                kw_set = set(kw_lookup.keys())
                cc_set = set(cc_lookup.keys())

                hits = set()
                if cc_set:
                    hits.add("code_class")
                if ds_set:
                    hits.add("description_short")
                if kw_set:
                    hits.add("keyword")

                if not hits:
                    return (pim_category_id, pim_category_name, assignment_source, assignment_confidence)

                non_empty_sets = [s for s in [cc_set, ds_set, kw_set] if s]
                intersection = set.intersection(*non_empty_sets) if non_empty_sets else set()

                if len(intersection) == 1:
                    target_id = next(iter(intersection))
                    total_count = (
                        ds_lookup.get(target_id, (0, None))[0]
                        + kw_lookup.get(target_id, (0, None))[0]
                        + cc_lookup.get(target_id, (0, None))[0]
                    )
                    target_name = pick_name_for_id(
                        target_id,
                        [cc_lookup, ds_lookup, kw_lookup],
                    )
                    source_val = source_map.get(frozenset(hits))
                    return (
                        target_id,
                        target_name,
                        source_val,
                        str(total_count),
                    )

                all_ids = sorted(ds_set | kw_set | cc_set)
                name_lookup = {}
                for pid, (_, name) in ds_lookup.items():
                    name_lookup[pid] = name or pid
                for pid, (_, name) in kw_lookup.items():
                    if pid not in name_lookup:
                        name_lookup[pid] = name or pid
                for pid, (_, name) in cc_lookup.items():
                    if pid not in name_lookup:
                        name_lookup[pid] = name or pid

                pim_id_str = "|".join(all_ids) if all_ids else None
                pim_name_str = "|".join([name_lookup.get(pid, pid) for pid in all_ids]) if all_ids else None
                source_val = source_map.get(frozenset(hits))

                return (
                    pim_id_str,
                    pim_name_str,
                    source_val,
                    "mixed",
                )

            finalize_udf = udf(
                finalize_assignment,
                final_result_schema,
            )

            with_final_df = (
                with_signals_df
                .withColumn(
                    "final_result",
                    finalize_udf(
                        col("pim_category_id"),
                        col("pim_category_name"),
                        col("assignment_source"),
                        col("assignment_confidence"),
                        col("ds_result"),
                        col("kw_result"),
                        col("cc_result"),
                    ),
                )
                .withColumn(
                    "pim_category_id",
                    col("final_result.pim_category_id_final")
                )
                .withColumn(
                    "pim_category_name",
                    col("final_result.pim_category_name_final")
                )
                .withColumn(
                    "assignment_source",
                    col("final_result.assignment_source_final")
                )
                .withColumn(
                    "assignment_confidence",
                    col("final_result.assignment_confidence_final")
                )
            )

            stats_df = (
                with_final_df
                .withColumn("ds_hit", size(col("ds_result.pim_ids")) > 0)
                .withColumn("kw_hit", size(col("kw_result.pim_ids")) > 0)
                .withColumn("cc_hit", size(col("cc_result.pim_ids")) > 0)
                .withColumn(
                    "hits_count",
                    col("ds_hit").cast("int") + col("kw_hit").cast("int") + col("cc_hit").cast("int"),
                )
            )

            cc_non_empty = stats_df.filter(col("cc_hit")).count()
            ds_non_empty = stats_df.filter(col("ds_hit")).count()
            kw_non_empty = stats_df.filter(col("kw_hit")).count()
            class_codes_present = with_signals_df.filter(size(col("class_codes")) > 0).count()
            cc_tokens_present = with_signals_df.filter(col("cc_tokens_count") > 0).count()

            unique_counts = {
                "code_class_match": stats_df.filter(
                    (col("assignment_confidence") != "mixed") & (col("assignment_source") == "code_class_match")
                ).count(),
                "description_short_match": stats_df.filter(
                    (col("assignment_confidence") != "mixed") & (col("assignment_source") == "description_short_match")
                ).count(),
                "keyword_match": stats_df.filter(
                    (col("assignment_confidence") != "mixed") & (col("assignment_source") == "keyword_match")
                ).count(),
                "code_class_and_description_short_match": stats_df.filter(
                    (col("assignment_confidence") != "mixed") & (col("assignment_source") == "code_class_and_description_short_match")
                ).count(),
                "code_class_and_keyword_match": stats_df.filter(
                    (col("assignment_confidence") != "mixed") & (col("assignment_source") == "code_class_and_keyword_match")
                ).count(),
                "description_short_and_keyword_match": stats_df.filter(
                    (col("assignment_confidence") != "mixed") & (col("assignment_source") == "description_short_and_keyword_match")
                ).count(),
                "code_class_and_description_short_and_keyword_match": stats_df.filter(
                    (col("assignment_confidence") != "mixed") & (col("assignment_source") == "code_class_and_description_short_and_keyword_match")
                ).count(),
            }

            mixed_multi_signal = stats_df.filter(
                (col("assignment_confidence") == "mixed")
                & (col("hits_count") >= 2)
            ).count()

            print(f"[INFO] PRODUCTS with CLASS_CODES hits: {cc_non_empty}")
            print(f"[INFO] PRODUCTS with DESCRIPTION_SHORT hits: {ds_non_empty}")
            print(f"[INFO] PRODUCTS with KEYWORD hits: {kw_non_empty}")
            print(f"[INFO] PRODUCTS with non-empty class_codes array: {class_codes_present}")
            print(f"[INFO] PRODUCTS with non-empty cc_tokens: {cc_tokens_present}")
            print("[INFO] UNIQUE assignment counts by signal combination:")
            for source_key, count_val in unique_counts.items():
                print(f"[INFO]   {source_key}: {count_val}")
            print(
                "[INFO] MIXED (>=2 signal hits, no unique intersection): "
                f"{mixed_multi_signal}"
            )
            code_class_assignments = with_final_df.filter(
                col("assignment_source").contains("code_class")
            ).count()
            print(
                "[INFO] PRODUCTS with assignment_source containing 'code_class': "
                f"{code_class_assignments}"
            )

            final_df = with_final_df.drop("ds_result", "kw_result", "cc_result", "final_result", "cc_tokens_count")

    print(f"[INFO] final_df rows (after PART-3): {final_df.count()}")

    # -------------------------
    # Write FINAL result back to SAME final_key (overwrite)
    # -------------------------
    timestamp_part4 = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    tmp_key_prefix_part4 = (
        f"{prepared_output_prefix.rstrip('/')}/"
        f"_tmp_{vendor_name}_forMapping_products_enriched_part4_{timestamp_part4}/"
    )
    tmp_uri_part4 = f"s3://{output_bucket}/{tmp_key_prefix_part4}"

    print(f"[INFO] Writing FINAL NDJSON (after PART-4) to temporary prefix: {tmp_uri_part4}")

    (
        final_df.toJSON()  # 1 JSON object per line
        .coalesce(1)  # single output part file
        .saveAsTextFile(tmp_uri_part4)
    )

    tmp_keys_part4 = list_s3_objects(output_bucket, tmp_key_prefix_part4)
    part_keys_part4 = [k for k in tmp_keys_part4 if "/part-" in k]

    if not part_keys_part4:
        raise RuntimeError(
            f"No part files found in PART-4 temporary output prefix '{tmp_key_prefix_part4}'"
        )

    part_keys_part4.sort()
    part_key_part4 = part_keys_part4[0]
    print(
        f"[INFO] Selected PART-4 part file: s3://{output_bucket}/{part_key_part4}"
    )

    print(
        f"[INFO] Copying FINAL result (overwriting) to final output: "
        f"s3://{output_bucket}/{final_key_primary}"
    )

    s3_client.copy_object(
        Bucket=output_bucket,
        CopySource={"Bucket": output_bucket, "Key": part_key_part4},
        Key=final_key_primary,
    )

    if final_key_legacy != final_key_primary:
        print(
            "[INFO] Copying FINAL result (overwriting) to legacy output: "
            f"s3://{output_bucket}/{final_key_legacy}"
        )
        s3_client.copy_object(
            Bucket=output_bucket,
            CopySource={"Bucket": output_bucket, "Key": part_key_part4},
            Key=final_key_legacy,
        )

    print(f"[INFO] Cleaning up PART-4 temporary prefix: {tmp_key_prefix_part4}")
    for k in tmp_keys_part4:
        try:
            s3_client.delete_object(Bucket=output_bucket, Key=k)
        except Exception as cleanup_err:
            print(f"[WARN] Failed to delete temporary file s3://{output_bucket}/{k}: {cleanup_err}")

    print("[INFO] Job completed successfully (Part-1 + Part-2 + Part-3 + Part-4).")
    job.commit()

except Exception as e:
    import traceback
    error_type = type(e).__name__
    error_msg = str(e)
    
    # Categorize error types for better debugging
    aws_error_types = ['ClientError', 'BotoCoreError', 'NoCredentialsError', 'PartialCredentialsError']
    is_aws_error = any(aws_err in error_type for aws_err in aws_error_types) or 'boto' in error_type.lower()
    
    if is_aws_error:
        print(f"[ERROR] AWS Service Error ({error_type}): {error_msg}")
    else:
        print(f"[ERROR] Runtime Error ({error_type}): {error_msg}")
    
    print("[ERROR] Full traceback:")
    traceback.print_exc()
    
    job.commit()
    raise
