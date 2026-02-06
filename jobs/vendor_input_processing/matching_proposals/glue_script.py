#!/usr/bin/env python3
# Glue 5.0 / Spark / Python 3 script

import sys
import json
import traceback

import boto3
from botocore.exceptions import ClientError

from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql import types as T


def main():
    # ---------- Very-early debug: raw argv + safe arg parsing ----------
    print("DEBUG: sys.argv received by Glue script:", sys.argv)

    try:
        args = getResolvedOptions(
            sys.argv,
            [
                "JOB_NAME",
                "INPUT_BUCKET",
                "OUTPUT_BUCKET",
                "vendor_name",
                "prepared_input_key",
                "prepared_output_prefix",
            ],
        )
    except Exception as e:
        # If we fail here, Glue logger isn't ready yet – so we print directly.
        print("FATAL: Error while resolving Glue arguments with getResolvedOptions.")
        print("Exception:", repr(e))
        traceback.print_exc()
        # Re-raise so Glue marks the job as failed with a visible trace
        raise

    job_name = args["JOB_NAME"]
    input_bucket = args["INPUT_BUCKET"]
    output_bucket = args["OUTPUT_BUCKET"]
    vendor_name = args["vendor_name"]
    prepared_input_key = args["prepared_input_key"]
    prepared_output_prefix = args["prepared_output_prefix"]

    # ---------- Glue / Spark setup ----------
    sc = SparkContext.getOrCreate()
    glue_context = GlueContext(sc)
    spark = glue_context.spark_session
    logger = glue_context.get_logger()

    job = Job(glue_context)
    job.init(job_name, args)

    logger.info("========== JOB START ==========")
    logger.info(f"JOB_NAME={job_name}")
    logger.info(f"INPUT_BUCKET={input_bucket}")
    logger.info(f"OUTPUT_BUCKET={output_bucket}")
    logger.info(f"vendor_name={vendor_name}")
    logger.info(f"prepared_input_key={prepared_input_key}")
    logger.info(f"prepared_output_prefix={prepared_output_prefix}")

    # Normalize prefixes (do not add or remove anything else)
    input_prefix = prepared_input_key.rstrip("/")
    output_prefix = prepared_output_prefix.rstrip("/")

    # ---------- Input discovery (extension-agnostic) ----------
    # We expect the file to be located under:
    #   <prepared_input_key>/canonicalCategoryMapping/
    # with a base name <vendor_name>_forMapping_products, but the upstream job
    # may or may not include a ".json" extension. Therefore we:
    #  1) Try "<base>.json"
    #  2) Try "<base>"
    #  3) If still not found, list objects with prefix "<base" and use it
    s3_client = boto3.client("s3")

    mapping_prefix = f"{input_prefix}/canonicalCategoryMapping".rstrip("/") + "/"
    base_filename = f"{vendor_name}_forMapping_products"

    candidate_keys = [
        mapping_prefix + base_filename + ".json",
        mapping_prefix + base_filename,
    ]

    resolved_input_key = None

    logger.info(f"Input discovery: mapping_prefix={mapping_prefix}")
    logger.info(f"Input discovery: base_filename={base_filename}")
    logger.info(f"Input discovery: candidate_keys={candidate_keys}")

    # Try explicit candidates first
    for key in candidate_keys:
        try:
            logger.info(
                f"Checking existence of candidate input file: s3://{input_bucket}/{key}"
            )
            s3_client.head_object(Bucket=input_bucket, Key=key)
            logger.info(f"Input file found using candidate key: {key}")
            resolved_input_key = key
            break
        except ClientError as ce:
            if ce.response.get("Error", {}).get("Code") in ("404", "NoSuchKey"):
                logger.info(f"Candidate key not found: {key}")
            else:
                logger.error(
                    f"Unexpected error when checking candidate input key {key}: {repr(ce)}"
                )
                raise

    # If still not resolved, try list_objects_v2 with the base prefix
    if resolved_input_key is None:
        prefix_for_listing = mapping_prefix + base_filename
        logger.info(
            "No candidate key found. Listing S3 objects with prefix "
            f"{prefix_for_listing!r} to handle unknown extensions."
        )
        try:
            resp = s3_client.list_objects_v2(
                Bucket=input_bucket,
                Prefix=prefix_for_listing,
                MaxKeys=10,
            )
            contents = resp.get("Contents", [])
            if len(contents) == 0:
                logger.warn(
                    "Input discovery via list_objects_v2 returned no objects. "
                    "We will treat this as 'no input file'."
                )
            elif len(contents) == 1:
                resolved_input_key = contents[0]["Key"]
                logger.info(
                    "Input discovery via list_objects_v2 succeeded with a single "
                    f"object: {resolved_input_key}"
                )
            else:
                # Multiple candidates – pick the first, but log a warning.
                resolved_input_key = contents[0]["Key"]
                logger.warn(
                    "Input discovery via list_objects_v2 returned multiple objects. "
                    f"Picking the first one: {resolved_input_key}. Please verify "
                    "upstream naming if this is not desired."
                )
        except ClientError as ce:
            logger.error(
                "Unexpected error while listing objects for input discovery: "
                f"{repr(ce)}"
            )
            raise

    # If we still have no resolved key, write {} and exit
    if resolved_input_key is None:
        msg = (
            "Input file not found under expected prefix. Checked candidates "
            f"{candidate_keys} and list_objects_v2 with prefix "
            f"{mapping_prefix + base_filename!r}. Writing empty mapping {{}} and exiting."
        )
        logger.error(msg)
        print("DEBUG:", msg)
        output_key = f"{output_prefix}/{vendor_name}_category_matching_proposals.json"
        write_json_dict_to_s3(output_bucket, output_key, {}, logger)
        job.commit()
        logger.info("========== JOB END (NO INPUT FILE) ==========")
        return

    input_key = resolved_input_key
    input_uri = f"s3://{input_bucket}/{input_key}"
    output_key = f"{output_prefix}/{vendor_name}_category_matching_proposals.json"

    logger.info(f"Resolved input S3 key: {input_key}")
    logger.info(f"Input URI: {input_uri}")
    logger.info(f"Computed output S3 key: {output_key}")

    try:
        # ---------- Read input JSON ----------
        try:
            logger.info(
                "Step 1: Reading input as standard JSON (line-delimited or normal)..."
            )
            df_products = spark.read.json(input_uri)
        except Exception as e1:
            logger.warn(
                "Standard JSON read failed; trying multiLine=true. "
                f"Error was: {repr(e1)}"
            )
            df_products = spark.read.option("multiLine", True).json(input_uri)

        logger.info(f"Step 1: Input schema: {df_products.schema.simpleString()}")
        print("DEBUG: Step 1 schema:", df_products.schema.simpleString())

        total_records = df_products.count()
        logger.info(
            f"Step 1: Total records in input (before any filtering): {total_records}"
        )
        print("DEBUG: Step 1 total_records:", total_records)

        if df_products.limit(1).count() == 0:
            msg = (
                "Step 1: No products found in input DataFrame. "
                "Writing empty mapping {}."
            )
            logger.warn(msg)
            print("DEBUG:", msg)
            write_json_dict_to_s3(output_bucket, output_key, {}, logger)
            job.commit()
            logger.info("========== JOB END (NO PRODUCTS) ==========")
            return

        # Check presence of vendor_mappings
        if "vendor_mappings" not in df_products.columns:
            msg = (
                "Input data does not contain 'vendor_mappings' field, "
                "which is required for category aggregation. Writing {}."
            )
            logger.error(msg)
            print("DEBUG:", msg)
            write_json_dict_to_s3(output_bucket, output_key, {}, logger)
            job.commit()
            logger.info("========== JOB END (NO VENDOR_MAPPINGS COLUMN) ==========")
            return

        # ---------- Step 2: Explode vendor_mappings ----------
        logger.info("Step 2: Exploding 'vendor_mappings' array...")
        df_exp = df_products.withColumn("vm", F.explode_outer(F.col("vendor_mappings")))

        total_after_explode = df_exp.count()
        logger.info(
            f"Step 2: Records after explode_outer(vendor_mappings): "
            f"{total_after_explode}"
        )
        print("DEBUG: Step 2 total_after_explode:", total_after_explode)

        non_null_vm = df_exp.filter(F.col("vm").isNotNull()).limit(1).count()
        logger.info(f"Step 2: Non-null 'vm' sample count (limit 1): {non_null_vm}")
        print("DEBUG: Step 2 non_null_vm (limit 1 count):", non_null_vm)

        if non_null_vm == 0:
            msg = (
                "Step 2: No non-null 'vendor_mappings' entries found. "
                "Writing empty mapping {}."
            )
            logger.warn(msg)
            print("DEBUG:", msg)
            write_json_dict_to_s3(output_bucket, output_key, {}, logger)
            job.commit()
            logger.info(
                "========== JOB END (NO VENDOR_MAPPINGS ENTRIES) =========="
            )
            return

        # ---------- Step 3: Exception rule per product (vm_count > 1) ----------
        logger.info(
            "Step 3: Applying exception rule based on products with "
            "more than one vendor_mappings entry (vm_count > 1)..."
        )

        # vm_count = size of vendor_mappings array per product
        df_with_vm_count = df_products.withColumn(
            "vm_count",
            F.when(F.col("vendor_mappings").isNull(), F.lit(0)).otherwise(
                F.size(F.col("vendor_mappings"))
            ),
        )

        # For products where vm_count > 1, explode their vendor_mappings
        # to collect all vendor_category_id that are affected by this exception
        df_multimapping = (
            df_with_vm_count.filter(F.col("vm_count") > 1)
            .withColumn("vm_multi", F.explode(F.col("vendor_mappings")))
            .select(F.col("vm_multi.vendor_category_id").alias("vendor_category_id"))
            .filter(F.col("vendor_category_id").isNotNull())
            .distinct()
        )

        invalid_categories = [r["vendor_category_id"] for r in df_multimapping.collect()]
        logger.info(
            "Step 3: Number of vendor_category_id with products having vm_count > 1: "
            f"{len(invalid_categories)}"
        )
        print(
            "DEBUG: Step 3 invalid vendor_category_id from vm_count>1:",
            invalid_categories,
        )

        if invalid_categories:
            logger.warn(
                "Step 3: Found vendor_category_id values associated with products "
                "that have more than one vendor_mappings entry. These categories "
                f"will be excluded from further processing: {invalid_categories}"
            )

        # Build vm_struct for later aggregation
        vm_struct = F.struct(
            F.col("vm.vendor_short_name").alias("vendor_short_name"),
            F.col("vm.vendor_category_id").alias("vendor_category_id"),
            F.col("vm.vendor_category_name").alias("vendor_category_name"),
            F.col("vm.vendor_category_path").alias("vendor_category_path"),
            F.col("vm.vendor_category_type").alias("vendor_category_type"),
        )

        df_vm_struct = df_exp.withColumn("vm_struct", vm_struct)

        distinct_vm_records = df_vm_struct.count()
        logger.info(
            f"Step 3: Records in df_vm_struct (after adding vm_struct): "
            f"{distinct_vm_records}"
        )
        print("DEBUG: Step 3 df_vm_struct count:", distinct_vm_records)

        # Exclude all rows whose vendor_category_id is in the invalid list
        if invalid_categories:
            logger.info("Step 3: Excluding rows with invalid vendor_category_id...")
            invalid_cats_df = spark.createDataFrame(
                [(vc_id,) for vc_id in invalid_categories],
                schema=T.StructType(
                    [T.StructField("vendor_category_id", T.StringType(), True)]
                ),
            )

            df_vm_valid = df_vm_struct.join(
                invalid_cats_df,
                on=df_vm_struct["vm.vendor_category_id"]
                == invalid_cats_df["vendor_category_id"],
                how="left_anti",
            )
        else:
            logger.info("Step 3: No invalid vendor_category_id found; keeping all rows.")
            df_vm_valid = df_vm_struct

        # Filter out rows without vendor_category_id
        df_vm_valid = df_vm_valid.filter(F.col("vm.vendor_category_id").isNotNull())

        valid_rows_count = df_vm_valid.count()
        logger.info(
            f"Step 3: Records after filtering to valid vendor_category_id: "
            f"{valid_rows_count}"
        )
        print("DEBUG: Step 3 valid_rows_count:", valid_rows_count)

        if valid_rows_count == 0:
            msg = (
                "Step 3: No valid vendor_category_id entries remain after applying the "
                "exception rule. Writing empty mapping {}."
            )
            logger.warn(msg)
            print("DEBUG:", msg)
            write_json_dict_to_s3(output_bucket, output_key, {}, logger)
            job.commit()
            logger.info("========== JOB END (NO VALID CATEGORIES) ==========")
            return

        # ---------- Step 4: Normalize pim_category_id (UNMATCHED) ----------
        logger.info("Step 4: Normalizing pim_category_id into pim_category_id_norm...")

        if "pim_category_id" in df_vm_valid.columns:
            df_vm_valid = df_vm_valid.withColumn(
                "pim_category_id_norm",
                F.when(
                    F.col("pim_category_id").isNull()
                    | (F.trim(F.col("pim_category_id")) == ""),
                    F.lit("UNMATCHED"),
                ).otherwise(F.col("pim_category_id")),
            )
            logger.info("Step 4: pim_category_id column found and normalized.")
        else:
            df_vm_valid = df_vm_valid.withColumn(
                "pim_category_id_norm", F.lit("UNMATCHED")
            )
            logger.info(
                "Step 4: pim_category_id column not present; all rows set to UNMATCHED."
            )

        # Ensure assignment_source and assignment_confidence columns exist
        if "assignment_source" not in df_vm_valid.columns:
            df_vm_valid = df_vm_valid.withColumn(
                "assignment_source", F.lit(None).cast(T.StringType())
            )
            logger.info(
                "Step 4: assignment_source column missing; added as nullable string."
            )
        if "assignment_confidence" not in df_vm_valid.columns:
            df_vm_valid = df_vm_valid.withColumn(
                "assignment_confidence", F.lit(None).cast(T.StringType())
            )
            logger.info(
                "Step 4: assignment_confidence column missing; added as nullable string."
            )

        # Ensure pim_category_name exists so we can propagate it downstream
        if "pim_category_name" not in df_vm_valid.columns:
            df_vm_valid = df_vm_valid.withColumn(
                "pim_category_name", F.lit(None).cast(T.StringType())
            )
            logger.info(
                "Step 4: pim_category_name column missing; added as nullable string."
            )

        # Ensure product-level detail columns exist for later aggregation
        for col_name in ["article_id", "description_short", "keywords", "class_codes"]:
            if col_name not in df_vm_valid.columns:
                df_vm_valid = df_vm_valid.withColumn(col_name, F.lit(None))
        logger.info(
            "Step 4: Ensured presence of article-level columns: "
            "article_id, description_short, keywords, class_codes."
        )

        # ---------- Step 5: Aggregate pim_matches, split by method ----------
        logger.info(
            "Step 5: Aggregating pim_matches by "
            "(vendor_category_id, pim_category_id_norm, assignment_source, "
            "assignment_confidence) and collecting product details..."
        )

        pim_group = (
            df_vm_valid.groupBy(
                F.col("vm.vendor_category_id").alias("vendor_category_id"),
                F.col("pim_category_id_norm").alias("pim_category_id_norm"),
                F.col("assignment_source").alias("assignment_source"),
                F.col("assignment_confidence").alias("assignment_confidence"),
            )
            .agg(
                F.count(F.lit(1)).alias("products_in_pim_category"),
                F.first("pim_category_name", ignorenulls=True).alias(
                    "pim_category_name"
                ),
                F.collect_list(
                    F.struct(
                        F.col("article_id").alias("article_id"),
                        F.col("description_short").alias("description_short"),
                        F.col("keywords").alias("keywords"),
                        F.col("class_codes").alias("class_codes"),
                    )
                ).alias("products"),
            )
        )

        pim_group_count = pim_group.count()
        logger.info(f"Step 5: Number of grouped rows in pim_group: {pim_group_count}")
        print("DEBUG: Step 5 pim_group count:", pim_group_count)

        pim_group_with_struct = pim_group.withColumn(
            "pim_match",
            F.struct(
                F.col("pim_category_id_norm").alias("pim_category_id"),
                F.col("pim_category_name").alias("pim_category_name"),
                F.col("assignment_source").alias("assignment_source"),
                F.col("assignment_confidence").alias("assignment_confidence"),
                F.col("products_in_pim_category").alias("products_in_pim_category"),
                F.col("products").alias("products"),
            ),
        )

        pim_matches_df = (
            pim_group_with_struct.groupBy("vendor_category_id")
            .agg(F.collect_list("pim_match").alias("pim_matches"))
        )

        pim_matches_count = pim_matches_df.count()
        logger.info(
            "Step 5: Number of rows in pim_matches_df "
            f"(distinct vendor_category_id): {pim_matches_count}"
        )
        print("DEBUG: Step 5 pim_matches_df count:", pim_matches_count)

        # ---------- Step 6: Aggregate vendor_mappings and totals ----------
        logger.info(
            "Step 6: Aggregating vendor metadata and "
            "total_products_in_vendor_category..."
        )

        vendor_meta_df = (
            df_vm_valid.groupBy(F.col("vm.vendor_category_id").alias("vendor_category_id"))
            .agg(
                F.first("vm.vendor_short_name", ignorenulls=True).alias(
                    "vendor_short_name"
                ),
                F.first("vm.vendor_category_id", ignorenulls=True).alias(
                    "vendor_category_id_dup"
                ),
                F.first("vm.vendor_category_name", ignorenulls=True).alias(
                    "vendor_category_name"
                ),
                F.first("vm.vendor_category_path", ignorenulls=True).alias(
                    "vendor_category_path"
                ),
                F.first("vm.vendor_category_type", ignorenulls=True).alias(
                    "vendor_category_type"
                ),
                F.count(F.lit(1)).alias("total_products_in_vendor_category"),
            )
        )

        vendor_meta_count = vendor_meta_df.count()
        logger.info(
            "Step 6: Number of rows in vendor_meta_df "
            f"(distinct vendor_category_id): {vendor_meta_count}"
        )
        print("DEBUG: Step 6 vendor_meta_df count:", vendor_meta_count)

        # ---------- Step 7: Join vendor_meta with pim_matches ----------
        logger.info("Step 7: Joining vendor_meta_df with pim_matches_df...")
        result_df = vendor_meta_df.join(
            pim_matches_df, on="vendor_category_id", how="left"
        )

        result_count = result_df.count()
        logger.info(f"Step 7: Number of vendor categories in result_df: {result_count}")
        print("DEBUG: Step 7 result_df count:", result_count)

        # ---------- Step 8: Convert to dictionary keyed by vendor_category_id ----------
        logger.info("Step 8: Collecting result_df to driver and building result_dict...")

        rows = result_df.collect()
        result_dict = {}

        for row in rows:
            vcat_id = row["vendor_category_id"]

            vendor_mappings = {
                "vendor_short_name": row["vendor_short_name"],
                "vendor_category_id": row["vendor_category_id"],
                "vendor_category_name": row["vendor_category_name"],
                "vendor_category_path": row["vendor_category_path"],
                "vendor_category_type": row["vendor_category_type"],
            }

            total_products = row["total_products_in_vendor_category"] or 0

            pim_matches_py = []
            pim_matches_val = row["pim_matches"]
            if pim_matches_val is not None:
                for m in pim_matches_val:
                    # Safely extract products_in_pim_category
                    products_in_pim_cat = m["products_in_pim_category"]

                    # Build product-level details list
                    products_py = []
                    raw_products = m["products"] if "products" in m else None
                    if raw_products is not None:
                        for p in raw_products:
                            article_id = p["article_id"] if p["article_id"] is not None else ""
                            desc = p["description_short"] or ""
                            raw_keywords = p["keywords"]
                            if raw_keywords is None:
                                keywords = []
                            elif isinstance(raw_keywords, (list, tuple)):
                                keywords = [str(k) for k in raw_keywords if k is not None]
                            else:
                                keywords = [str(raw_keywords)]

                            raw_class_codes = p["class_codes"]
                            class_codes = []
                            if raw_class_codes is not None:
                                if not isinstance(raw_class_codes, (list, tuple)):
                                    raw_class_codes = [raw_class_codes]
                                for cc in raw_class_codes:
                                    if cc is None:
                                        continue
                                    if isinstance(cc, dict):
                                        code = cc.get("code") or ""
                                        system = cc.get("system") or ""
                                    else:
                                        code = getattr(cc, "code", None) or ""
                                        system = getattr(cc, "system", None) or ""
                                    class_codes.append(
                                        {
                                            "code": code,
                                            "system": system,
                                        }
                                    )

                            products_py.append(
                                {
                                    "article_id": article_id,
                                    "description_short": desc,
                                    "keywords": keywords,
                                    "class_codes": class_codes,
                                }
                            )

                    pim_matches_py.append(
                        {
                            "pim_category_id": m["pim_category_id"],
                            "pim_category_name": (
                                m.asDict().get("pim_category_name")
                                if hasattr(m, "asDict")
                                else m["pim_category_name"]
                                if "pim_category_name" in m
                                else None
                            ),
                            "assignment_source": m["assignment_source"],
                            "assignment_confidence": m["assignment_confidence"],
                            "products_in_pim_category": int(products_in_pim_cat)
                            if products_in_pim_cat is not None
                            else 0,
                            "products": products_py,
                        }
                    )

            result_dict[vcat_id] = {
                "vendor_category_id": vcat_id,
                "vendor_mappings": vendor_mappings,
                "total_products_in_vendor_category": int(total_products),
                "pim_matches": pim_matches_py,
            }

        logger.info(
            f"Step 8: Built result_dict with {len(result_dict)} "
            "vendor_category_id entries."
        )
        print("DEBUG: Step 8 result_dict size:", len(result_dict))

        # ---------- Step 9: Write pretty-printed JSON to S3 ----------
        logger.info("Step 9: Writing pretty-printed JSON to S3...")
        write_json_dict_to_s3(output_bucket, output_key, result_dict, logger)

        # ---------- Step 10 (Part-2): Build oneVendor_to_onePim subset ----------
        logger.info(
            "Step 10 (Part-2): Deriving oneVendor_to_onePim subset from result_dict..."
        )

        one_to_one_dict = {}
        for vcat_id, rec in result_dict.items():
            # Check vendor_mappings cardinality:
            vm = rec.get("vendor_mappings")
            # In the current structure this is a single dict; treat that as 'one entry'.
            # If it ever becomes a list, enforce exactly one element.
            if vm is None:
                continue
            if isinstance(vm, (list, tuple)) and len(vm) != 1:
                continue

            pim_matches = rec.get("pim_matches") or []
            # Only one pim_matches entry
            if len(pim_matches) != 1:
                continue

            pm = pim_matches[0]
            conf = pm.get("assignment_confidence")

            # Exclude null / empty
            if conf is None:
                continue
            conf_str = str(conf)
            if conf_str == "":
                continue

            # Case-sensitive comparison, per requirement
            if conf_str == "mixed" or conf_str == "null":
                continue

            # All conditions satisfied => include full record unchanged
            one_to_one_dict[vcat_id] = rec

        logger.info(
            "Step 10 (Part-2): oneVendor_to_onePim subset contains "
            f"{len(one_to_one_dict)} vendor_category_id entries."
        )
        print(
            "DEBUG: Step 10 one_to_one_dict size:",
            len(one_to_one_dict),
        )

        output_key_one_to_one = (
            f"{output_prefix}/{vendor_name}_category_matching_proposals_one_vendor_to_one_pim_match.json"
        )
        logger.info(
            "Step 10 (Part-2): Writing oneVendor_to_onePim JSON to S3: "
            f"s3://{output_bucket}/{output_key_one_to_one}"
        )
        write_json_dict_to_s3(output_bucket, output_key_one_to_one, one_to_one_dict, logger)

        job.commit()
        logger.info("========== JOB END (SUCCESS) ==========")

    except Exception as e:
        logger.error("Job failed with exception.")
        logger.error(repr(e))
        logger.error(traceback.format_exc())
        print("FATAL: Job failed with exception:", repr(e))
        traceback.print_exc()
        # Let Glue mark the job as failed
        raise


def write_json_dict_to_s3(bucket: str, key: str, data_dict: dict, logger):
    """
    Write a Python dict as pretty-printed JSON to S3.
    """
    s3 = boto3.client("s3")
    body = json.dumps(data_dict, indent=2, ensure_ascii=False)
    logger.info(f"Writing output JSON to s3://{bucket}/{key}")
    print(
        f"DEBUG: Writing output JSON to s3://{bucket}/{key}, "
        f"{len(body)} bytes."
    )
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=body.encode("utf-8"))
    except ClientError as ce:
        logger.error(f"Failed to write output to s3://{bucket}/{key}: {repr(ce)}")
        print("DEBUG: Failed to write output:", repr(ce))
        raise


if __name__ == "__main__":
    main()
