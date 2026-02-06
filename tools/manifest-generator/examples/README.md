# Manifest Generator Examples

This directory contains example outputs from the manifest generator tool to demonstrate its capabilities.

## Example 1: preprocess_incoming_bmecat (python_shell runtime)

A Python Shell Glue job that processes BMEcat XML files.

**Command:**
```bash
python tools/manifest-generator/generate.py \
  --script jobs/vendor_input_processing/preprocess_incoming_bmecat/glue_script.py \
  --output tools/manifest-generator/examples/preprocess_incoming_bmecat_generated.yaml
```

**What the tool detected:**
- Runtime: python_shell (from awsglue.utils import without Spark)
- Parameters: 5 parameters from getResolvedOptions
- Inputs: 2 (XML input file + config file)
- Outputs: 15 different NDJSON outputs
- Helper functions: Recognized read_text_from_s3 and write_ndjson_to_s3 patterns
- F-string patterns: Extracted ${BMECAT_OUTPUT_PREFIX}${VENDOR_NAME}_* patterns

## Example 2: category_mapping_to_canonical (pyspark runtime)

A PySpark Glue job that maps vendor categories to canonical taxonomy.

**Command:**
```bash
python tools/manifest-generator/generate.py \
  --script jobs/vendor_input_processing/category_mapping_to_canonical/glue_script.py \
  --output tools/manifest-generator/examples/category_mapping_generated.yaml
```

**What the tool detected:**
- Runtime: pyspark (from SparkContext/GlueContext imports)
- Parameters: 5 parameters
- Spark operations: spark.read.json() calls
- Different pattern recognition for Spark-based I/O

## Comparison with Manual Manifests

Compare generated manifests with manually created ones to see:
1. What the tool gets right automatically
2. What needs manual review/enhancement
3. Evidence notes that explain the extraction

The tool is designed to provide a ~80% complete draft that humans review and finalize, not a 100% perfect output.

## How to Use These Examples

1. Run the generator commands above
2. Compare output with actual manifests in jobs/ directories
3. Identify patterns the tool handles well
4. Identify areas for improvement
5. Provide feedback for tool enhancements
