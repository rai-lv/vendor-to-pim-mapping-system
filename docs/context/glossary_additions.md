### Normalized placeholder
A manifest placeholder convention (e.g., `${X_norm}`) indicating that parameter `X` has been normalized by the script to ensure a trailing slash for S3 prefix operations.
Example: `${prepared_output_prefix_norm}` means the `prepared_output_prefix` parameter value with exactly one trailing `/`.
Definition: Section 6.4 of `docs/standards/job_manifest_spec.md`.

---

## P

### Placeholder (manifest)
A template variable in a job manifest's `bucket` or `key_pattern` field, represented as `${NAME}`.
Placeholders are substituted at job invocation time with actual parameter values or runtime-generated values.
Types: parameter placeholders (match parameter names exactly) and runtime-generated placeholders (computed by the job).

### PySpark
The Python API for Apache Spark, enabling large-scale data processing using Spark's distributed computing engine.
In this system, PySpark jobs run on AWS Glue with access to `SparkContext`, `GlueContext`, and Spark DataFrames.
Runtime type in job manifests: `pyspark`.

### Python Shell (AWS Glue)
A lightweight Glue job type that runs standard Python code without Spark overhead.
Used for tasks that process smaller datasets or orchestrate S3 operations using boto3.
Runtime type in job manifests: `python_shell`.
Distinguished from `pyspark` by absence of SparkContext/GlueContext Spark features.

---

## R

### Run receipt
A structured JSON artifact written by a job to S3 that records execution metadata: run ID, timestamp, input/output locations, record counts, validation status, and notes.
Run receipts serve as audit trails and enable downstream jobs to verify upstream completion.
Declared in job manifests under `logging_and_receipt.writes_run_receipt`.

---

## S

### Side effect (job)
A job behavior that modifies S3 state beyond its declared outputs.
Types:
- `deletes_inputs`: Job deletes input objects after successful processing
- `overwrites_outputs`: Job overwrites existing output objects (vs. fail-on-exists)
Declared in job manifests under `side_effects` to inform orchestration and recovery logic.
