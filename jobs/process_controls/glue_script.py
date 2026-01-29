# Write Outputs: Updated to Handle Empty Outputs Gracefully
def write_single_csv(
    df: DataFrame,
    output_bucket: str,
    final_key: str,
    tmp_prefix: str,
    s3_client,
):
    """
    Writes the DataFrame to a single CSV file. Handles empty inputs consistently by generating
    a placeholder file with headers only. Cleans up temporary objects non-fatally.
    """
    tmp_uri = f"s3://{output_bucket}/{tmp_prefix}"
    print(f"[INFO] Writing CSV to temporary prefix: {tmp_uri}")

    if df.rdd.isEmpty():
        print(f"[INFO] Input DataFrame is empty. Generating an empty CSV with headers: {df.columns}")
        schema = df.schema
        empty_df = df.sql_ctx.createDataFrame([], schema=schema)
        empty_df.limit(1).coalesce(1).write.mode("overwrite").option("header", True).csv(tmp_uri)
    else:
        (
            df.coalesce(1)
              .write.mode("overwrite")
              .option("header", True)
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
        except Exception as cleanup_error:
            print(f"[WARNING] Failed to delete temporary file s3://{output_bucket}/{k}. Error: {cleanup_error}")

# Updated try-except block for more granular handling
try:
    # Main Job Logic Here
    pass  # Replace with existing job logic

except RuntimeError as runtime_err:
    print(f"[ERROR] Job Runtime Error: {runtime_err}")
    job.commit()
    raise

except boto3.exceptions.Boto3Error as s3_error:
    print(f"[ERROR] AWS S3 Operation Failed: {s3_error}")
    job.commit()
    raise

except Exception as general_error:
    print(f"[ERROR] Unexpected Error: {general_error}")
    job.commit()
    raise
