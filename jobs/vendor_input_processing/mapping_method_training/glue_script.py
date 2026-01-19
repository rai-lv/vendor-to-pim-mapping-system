"""
AWS Glue script for vendorInputProcessing_VENDOR_mappingMethodTraining.
Section 1 bootstrapping: argument parsing, key resolution, existence checks, and run receipt writing.
"""

import hashlib
import io
import json
import sys
from collections import defaultdict
from datetime import datetime
from itertools import combinations
from copy import deepcopy
import re
from typing import Dict, List, Set, Tuple

import boto3
from botocore.exceptions import ClientError
try:
    from awsglue.utils import getResolvedOptions
except ImportError as exc:  # pragma: no cover - Glue runtime should provide this
    raise ImportError("awsglue package is required when running this script in AWS Glue") from exc

TOKEN_PATTERN = re.compile(r"[A-Za-z0-9ÄÖÜäöüß]+")
TRIM_PATTERN = re.compile(r"^[^A-Za-z0-9ÄÖÜäöüß]+|[^A-Za-z0-9ÄÖÜäöüß]+$")

THRESHOLD_POLICY = {
    "products_total_min": 8,
    "support_ratio_min": 0.60,
    "support_count_min": 5,
    "support_logic": "ratio_or_count",
}


def evaluate_threshold(
    products_in_category: int | None,
    matched_products_in_category: int | None,
    threshold_policy: dict,
) -> dict:
    products_total = products_in_category or 0
    matched_total = matched_products_in_category or 0
    support_ratio = matched_total / products_total if products_total else 0.0

    support_logic = threshold_policy.get("support_logic", "ratio_or_count")
    if support_logic != "ratio_or_count":
        raise ValueError(f"Unsupported support_logic '{support_logic}' in threshold_policy")

    pass_threshold = bool(
        products_total >= threshold_policy.get("products_total_min", 0)
        and (
            support_ratio >= threshold_policy.get("support_ratio_min", 0)
            or matched_total >= threshold_policy.get("support_count_min", 0)
        )
    )

    return {
        "pass_threshold": pass_threshold,
        "support_ratio": support_ratio,
    }


# === Section 1: LOCKED – DO NOT TOUCH (Bootstrapping / Arg parsing / Key resolution / Run receipt) ===

def s3_key_exists(s3_client, bucket: str, key: str) -> bool:
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as error:
        error_code = error.response.get("Error", {}).get("Code")
        http_status = error.response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        if error_code in {"404", "NotFound"} or http_status == 404:
            return False
        raise

def select_latest_category_mapping_reference(s3_client, bucket: str) -> str:
    prefix = "canonical_mappings/"
    paginator = s3_client.get_paginator("list_objects_v2")
    keys: List[str] = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj.get("Key", "")
            if re.search(r"Category_Mapping_Reference_.*\.json$", key):
                keys.append(key)
    if not keys:
        raise RuntimeError("No Category_Mapping_Reference_*.json files found in canonical_mappings/")
    return max(keys)


def main():
    required_args = [
        "JOB_NAME",
        "vendor_name",
        "prepared_input_key",
        "prepared_output_prefix",
        "INPUT_BUCKET",
        "OUTPUT_BUCKET",
    ]
    args = getResolvedOptions(sys.argv, required_args)
    print(f"Received args: {args}")

    job_name = args["JOB_NAME"]
    vendor_name = args["vendor_name"]
    prepared_input_key = args["prepared_input_key"]
    prepared_output_prefix_raw = args["prepared_output_prefix"]
    input_bucket = args["INPUT_BUCKET"]
    output_bucket = args["OUTPUT_BUCKET"]

    prepared_output_prefix = prepared_output_prefix_raw.rstrip("/")
    run_id = datetime.utcnow().strftime("%Y%m%d-T%H%M%SZ")

    s3_client = boto3.client("s3")

    step2_prefix = f"{prepared_output_prefix}/"
    step2_full_key = f"{step2_prefix}{vendor_name}_categoryMatchingProposals.json"
    step2_1to1_key = f"{step2_prefix}{vendor_name}_categoryMatchingProposals_oneVendor_to_onePim_match.json"

    category_mapping_reference_key = select_latest_category_mapping_reference(s3_client, input_bucket)
    stable_training_set_key = "canonical_mappings/stable_training_sets/StableTrainingSet.json"

    print(f"Resolved step2_full_key: s3://{input_bucket}/{step2_full_key}")
    print(f"Resolved step2_1to1_key: s3://{input_bucket}/{step2_1to1_key}")
    print(f"Selected category mapping reference key: s3://{input_bucket}/{category_mapping_reference_key}")
    print(f"Stable training set key: s3://{input_bucket}/{stable_training_set_key}")

    step2_full_exists = s3_key_exists(s3_client, input_bucket, step2_full_key)
    step2_1to1_exists = s3_key_exists(s3_client, input_bucket, step2_1to1_key)
    category_mapping_reference_exists = s3_key_exists(
        s3_client, input_bucket, category_mapping_reference_key
    )
    stable_training_set_exists = s3_key_exists(s3_client, input_bucket, stable_training_set_key)

    print(f"step2_full_exists: {step2_full_exists}")
    print(f"step2_1to1_exists: {step2_1to1_exists}")
    print(f"category_mapping_reference_exists: {category_mapping_reference_exists}")
    print(f"stable_training_set_exists: {stable_training_set_exists}")

    if not step2_full_exists:
        raise FileNotFoundError(
            f"Missing Step2 full proposals file at s3://{input_bucket}/{step2_full_key}"
        )
    if not step2_1to1_exists:
        raise FileNotFoundError(
            f"Missing Step2 1:1 proposals file at s3://{input_bucket}/{step2_1to1_key}"
        )
    if not category_mapping_reference_exists:
        raise FileNotFoundError(
            f"Missing selected category mapping reference file at s3://{input_bucket}/{category_mapping_reference_key}"
        )

    receipt = {
        "job_name": job_name,
        "script_version": "v0.10_section8_reference_update_no_internal_state",
        "run_id": run_id,
        "vendor_name": vendor_name,
        "prepared_input_key": prepared_input_key,
        "prepared_output_prefix": prepared_output_prefix,
        "input_bucket": input_bucket,
        "output_bucket": output_bucket,
        "step2_full_key": step2_full_key,
        "step2_1to1_key": step2_1to1_key,
        "category_mapping_reference_key_selected": category_mapping_reference_key,
        "stable_training_set_key": stable_training_set_key,
        "stable_training_set_exists": stable_training_set_exists,
        "counts": {},
        "outputs_written": {},
        "notes": [],
        "threshold_policy": THRESHOLD_POLICY,
    }

    run_receipt = run_pipeline_layers(receipt)
    run_receipt.pop("internal_state", None)

    if isinstance(run_receipt.get("notes"), str) and "CISTEM not used" in run_receipt["notes"]:
        run_receipt.pop("notes", None)
    elif isinstance(run_receipt.get("notes"), list):
        run_receipt["notes"] = [
            n for n in run_receipt["notes"] if not (isinstance(n, str) and "CISTEM not used" in n)
        ]
        if not run_receipt["notes"]:
            run_receipt.pop("notes", None)

    receipt_body = json.dumps(run_receipt, indent=2)
    receipt_key = (
        f"{prepared_output_prefix}/mappingMethodTraining/run_receipts/"
        f"run_receipt_{vendor_name}_{run_id}.json"
    )

    s3_client.put_object(Bucket=output_bucket, Key=receipt_key, Body=receipt_body)
    print(
        f"Run receipt written to s3://{output_bucket}/{receipt_key} with run_id {run_id}"
    )


# === Section 2: ACTIVE (Placeholder for next steps) ===


def section2_placeholder(run_receipt: dict) -> dict:
    input_bucket = run_receipt["input_bucket"]
    s3_client = boto3.client("s3")

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    def validate_step2_data(step2_data, context: str):
        if not isinstance(step2_data, dict):
            raise ValueError(f"{context}: top-level data must be a dict keyed by vendor_category_id")

        for vendor_category_id, vendor_category_data in step2_data.items():
            if not isinstance(vendor_category_data, dict):
                raise ValueError(
                    f"{context}: vendor category '{vendor_category_id}' must be a dict, got {type(vendor_category_data).__name__}"
                )

            for required_key in ["vendor_mappings", "total_products_in_vendor_category", "pim_matches"]:
                if required_key not in vendor_category_data:
                    raise ValueError(
                        f"{context}: vendor category '{vendor_category_id}' missing required key '{required_key}'"
                    )

            pim_matches = vendor_category_data["pim_matches"]
            if not isinstance(pim_matches, list):
                raise ValueError(
                    f"{context}: vendor category '{vendor_category_id}' pim_matches must be a list"
                )

            for pim_match in pim_matches:
                for required_key in ["pim_category_id", "assignment_source", "assignment_confidence", "products"]:
                    if required_key not in pim_match:
                        raise ValueError(
                            f"{context}: vendor category '{vendor_category_id}' pim_match missing required key '{required_key}'"
                        )

                products = pim_match["products"]
                if not isinstance(products, list):
                    raise ValueError(
                        f"{context}: vendor category '{vendor_category_id}' pim_match products must be a list"
                    )

                for product in products:
                    if "article_id" not in product:
                        raise ValueError(
                            f"{context}: vendor category '{vendor_category_id}' product missing required key 'article_id'"
                        )

    def validate_category_mapping_reference(reference_data):
        if not isinstance(reference_data, (dict, list)):
            raise ValueError("Category_Mapping_Reference must be a dict or list")

        entries = reference_data.values() if isinstance(reference_data, dict) else reference_data
        for entry in entries:
            if not isinstance(entry, dict):
                raise ValueError("Category_Mapping_Reference entries must be dicts")
            if "pim_category_id" not in entry:
                raise ValueError("Category_Mapping_Reference entry missing required key 'pim_category_id'")

    def validate_stable_training_set(training_set):
        if training_set is None:
            return
        if not isinstance(training_set, (dict, list)):
            raise ValueError("StableTrainingSet must be a dict or list when present")

    step2_full = load_json_from_s3(input_bucket, run_receipt["step2_full_key"])
    step2_1to1 = load_json_from_s3(input_bucket, run_receipt["step2_1to1_key"])
    category_mapping_reference = load_json_from_s3(
        input_bucket, run_receipt["category_mapping_reference_key_selected"]
    )

    stable_training_set = None
    if run_receipt.get("stable_training_set_exists"):
        stable_training_set = load_json_from_s3(input_bucket, run_receipt["stable_training_set_key"])

    validate_step2_data(step2_full, "Step2 full proposals")
    validate_step2_data(step2_1to1, "Step2 1:1 proposals")
    validate_category_mapping_reference(category_mapping_reference)
    validate_stable_training_set(stable_training_set)

    run_receipt.setdefault("counts", {})
    run_receipt.setdefault("notes", [])

    step2_full_vendor_category_count = len(step2_full)
    step2_1to1_vendor_category_count = len(step2_1to1)
    existing_category_match_vendor_category_count = 0
    total_products_1to1 = 0
    missing_keywords_products = 0
    missing_description_products = 0

    for vendor_category_data in step2_1to1.values():
        pim_matches = vendor_category_data.get("pim_matches", [])
        if len(pim_matches) == 1:
            only_match = pim_matches[0]
            if (
                only_match.get("assignment_source") == "existing_category_match"
                and only_match.get("pim_category_id") != "UNMATCHED"
            ):
                existing_category_match_vendor_category_count += 1

        for pim_match in pim_matches:
            products = pim_match.get("products", [])
            for product in products:
                total_products_1to1 += 1
                keywords = product.get("keywords")
                description_short = product.get("description_short")

                if not keywords:
                    missing_keywords_products += 1
                if not description_short:
                    missing_description_products += 1

    if isinstance(category_mapping_reference, dict):
        pim_category_entry_count = len(category_mapping_reference)
    else:
        pim_category_entry_count = len(category_mapping_reference)

    stable_training_set_exists = bool(run_receipt.get("stable_training_set_exists"))
    if stable_training_set_exists:
        if isinstance(stable_training_set, dict):
            stable_training_set_record_count = len(stable_training_set)
        else:
            stable_training_set_record_count = len(stable_training_set)
    else:
        stable_training_set_record_count = 0

    run_receipt["counts"]["step2_full"] = {
        "vendor_category_count": step2_full_vendor_category_count,
    }
    run_receipt["counts"]["step2_1to1"] = {
        "vendor_category_count": step2_1to1_vendor_category_count,
        "existing_category_match_vendor_category_count": existing_category_match_vendor_category_count,
    }
    run_receipt["counts"]["category_mapping_reference"] = {
        "pim_category_entry_count": pim_category_entry_count,
    }
    run_receipt["counts"]["stable_training_set"] = {
        "exists": stable_training_set_exists,
        "record_count": stable_training_set_record_count,
    }

    if total_products_1to1 > 0:
        if missing_keywords_products / total_products_1to1 > 0.5:
            run_receipt["notes"].append(
                "High share (>50%) of 1:1 products missing or empty keywords"
            )
        if missing_description_products / total_products_1to1 > 0.5:
            run_receipt["notes"].append(
                "High share (>50%) of 1:1 products missing or empty description_short"
            )

    return run_receipt


def layer_a_truth_training_base(run_receipt: dict) -> dict:
    run_receipt = section2_placeholder(run_receipt)
    run_receipt = section3_extract_stable_training_delta(run_receipt)
    run_receipt = section4_upsert_stable_training_set(run_receipt)
    return run_receipt


def layer_b_evidence_build(run_receipt: dict) -> dict:
    run_receipt = section5_build_unigram_evidence(run_receipt)
    run_receipt = section6_6_build_pair_evidence(run_receipt)
    return run_receipt


def layer_c_rule_build(run_receipt: dict) -> dict:
    run_receipt, field_globals = section6_1_load_field_globals(run_receipt)
    run_receipt, rules_by_pim_category, rules_summary = section6_2_generate_contains_any_rules(
        run_receipt, field_globals
    )
    run_receipt, rules_by_pim_category, rules_summary = section6_7_generate_contains_all_rules(
        run_receipt, rules_by_pim_category, rules_summary
    )
    run_receipt, rules_by_pim_category, rules_summary = (
        section6_8_generate_contains_any_exclude_any_rules(
            run_receipt, field_globals, rules_by_pim_category, rules_summary
        )
    )
    run_receipt = section6_3_write_rules_snapshot(
        run_receipt,
        field_globals=field_globals,
        rules_by_pim_category=rules_by_pim_category,
        rules_summary=rules_summary,
    )
    run_receipt = section6_9_write_product_rule_hits(
        run_receipt,
        rules_by_pim_category=rules_by_pim_category,
        field_globals=field_globals,
    )
    run_receipt = section7_1_write_vendor_category_product_rule_hits(run_receipt)
    run_receipt = section7_2_write_rule_validation_status(run_receipt)
    run_receipt = section7_3_write_vendor_category_mapping_status(run_receipt)
    run_receipt = section8_update_category_mapping_reference(run_receipt)
    return run_receipt


def run_pipeline_layers(run_receipt: dict) -> dict:
    run_receipt = layer_a_truth_training_base(run_receipt)
    run_receipt = layer_b_evidence_build(run_receipt)
    run_receipt = layer_c_rule_build(run_receipt)
    return run_receipt


# === Section 3: ACTIVE (Extract StableTrainingSet delta from Step2 1:1 existing_category_match only) ===


def section3_extract_stable_training_delta(run_receipt: dict) -> dict:
    input_bucket = run_receipt["input_bucket"]
    output_bucket = run_receipt["output_bucket"]
    vendor_name = run_receipt["vendor_name"]
    prepared_output_prefix = run_receipt["prepared_output_prefix"]
    run_id = run_receipt["run_id"]

    s3_client = boto3.client("s3")

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    def filter_product_fields(product: dict) -> dict:
        return {
            "article_id": product.get("article_id"),
            "description_short": product.get("description_short"),
            "keywords": product.get("keywords"),
            "class_codes": product.get("class_codes"),
        }

    step2_1to1 = load_json_from_s3(input_bucket, run_receipt["step2_1to1_key"])

    delta_records = []
    total_product_count = 0

    for vendor_category_id, vendor_category_data in step2_1to1.items():
        pim_matches = vendor_category_data.get("pim_matches", [])
        if len(pim_matches) != 1:
            continue

        only_match = pim_matches[0]
        if (
            only_match.get("assignment_source") != "existing_category_match"
            or only_match.get("pim_category_id") == "UNMATCHED"
        ):
            continue

        vendor_mappings = vendor_category_data.get("vendor_mappings", {})
        vendor_short_name = vendor_mappings.get("vendor_short_name") or vendor_name

        products = only_match.get("products", [])
        filtered_products = [filter_product_fields(product) for product in products]

        delta_record = {
            "vendor_short_name": vendor_short_name,
            "vendor_category_id": vendor_category_id,
            "vendor_category_name": vendor_mappings.get("vendor_category_name"),
            "vendor_category_path": vendor_mappings.get("vendor_category_path"),
            "vendor_category_type": vendor_mappings.get("vendor_category_type"),
            "pim_category_id": only_match.get("pim_category_id"),
            "assignment_source": only_match.get("assignment_source"),
            "assignment_confidence": only_match.get("assignment_confidence"),
            "run_id": run_id,
            "total_products_in_vendor_category": vendor_category_data.get(
                "total_products_in_vendor_category"
            ),
            "products": filtered_products,
        }

        delta_records.append(delta_record)
        total_product_count += len(filtered_products)

    delta_body = json.dumps(delta_records, indent=2)

    stable_training_delta_key = (
        f"{prepared_output_prefix}/mappingMethodTraining/stable_training_deltas/"
        f"stable_training_delta_{vendor_name}_{run_id}.json"
    )

    s3_client.put_object(
        Bucket=output_bucket,
        Key=stable_training_delta_key,
        Body=delta_body,
    )

    run_receipt.setdefault("outputs_written", {})[
        "stable_training_delta_key"
    ] = stable_training_delta_key

    run_receipt.setdefault("counts", {}).setdefault("stable_training_delta", {})[
        "vendor_category_count"
    ] = len(delta_records)
    run_receipt["counts"]["stable_training_delta"]["product_count"] = total_product_count

    if not delta_records:
        run_receipt.setdefault("notes", []).append(
            "No existing_category_match categories in Step2 1:1 input; delta is empty."
        )

    return run_receipt


# === Section 4: ACTIVE (Upsert global StableTrainingSet using delta + lineage) ===


def section4_upsert_stable_training_set(run_receipt: dict) -> dict:
    input_bucket = run_receipt["input_bucket"]
    output_bucket = run_receipt["output_bucket"]
    vendor_name = run_receipt["vendor_name"]
    run_id = run_receipt["run_id"]
    stable_training_set_key = run_receipt["stable_training_set_key"]
    stable_training_set_exists = run_receipt.get("stable_training_set_exists", False)
    delta_key = run_receipt.get("outputs_written", {}).get("stable_training_delta_key")

    if not delta_key:
        raise ValueError("stable_training_delta_key missing from run_receipt outputs")

    s3_client = boto3.client("s3")

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    if stable_training_set_exists:
        stable_training_set = load_json_from_s3(input_bucket, stable_training_set_key)
        if not isinstance(stable_training_set, dict):
            raise ValueError("StableTrainingSet must be a JSON object keyed by vendor::category")
    else:
        stable_training_set = {}

    delta_records = load_json_from_s3(output_bucket, delta_key)
    if not isinstance(delta_records, list):
        raise ValueError("StableTrainingSet delta must be a JSON list")

    created_key_count = 0
    updated_key_count = 0

    for record in delta_records:
        if not isinstance(record, dict):
            raise ValueError("Each delta record must be a JSON object")
        vendor_category_id = record.get("vendor_category_id")
        if vendor_category_id is None:
            raise ValueError("Delta record missing required field 'vendor_category_id'")

        upsert_key = f"{vendor_name}::{vendor_category_id}"
        existing_record = stable_training_set.get(upsert_key) or {}

        first_seen_run_id = existing_record.get("first_seen_run_id") or run_id

        new_record = dict(record)
        new_record["first_seen_run_id"] = first_seen_run_id
        new_record["last_seen_run_id"] = run_id

        if upsert_key in stable_training_set:
            updated_key_count += 1
        else:
            created_key_count += 1

        stable_training_set[upsert_key] = new_record

    stable_training_body = json.dumps(stable_training_set, indent=2)

    s3_client.put_object(
        Bucket=input_bucket,
        Key=stable_training_set_key,
        Body=stable_training_body,
    )

    outputs_written = run_receipt.setdefault("outputs_written", {})
    outputs_written["stable_training_set_key"] = stable_training_set_key

    stable_training_set_upsert_counts = run_receipt.setdefault("counts", {}).setdefault(
        "stable_training_set_upsert", {}
    )
    stable_training_set_upsert_counts.update(
        {
            "delta_record_count": len(delta_records),
            "created_key_count": created_key_count,
            "updated_key_count": updated_key_count,
            "final_total_key_count": len(stable_training_set),
        }
    )

    if not delta_records:
        run_receipt.setdefault("notes", []).append(
            "StableTrainingSet delta was empty; wrote existing dataset unchanged."
        )

    return run_receipt


# === Section 5: ACTIVE (Build StableTrainingEvidence_Unigrams_v1) ===


NORMALIZATION_VERSION = "v1.2_ae_stopwords_len3_plural_vocab"
MIN_TOKEN_LENGTH = 3
DROP_NUMERIC_ONLY_FIELDS = ["KEYWORD", "DESCRIPTION_SHORT"]
DENYLIST_CONFIG_KEY_DEFAULT = (
    "configuration-files/vendorInputProcessing_configs/categoryMapping_DenylistConfig.json"
)
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


def tokenize_text_value(value: str, field_name: str, stopwords: Set[str]) -> List[str]:
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


def tokenize_class_codes(class_codes) -> List[str]:
    tokens: List[str] = []
    if isinstance(class_codes, list):
        for entry in class_codes:
            if not isinstance(entry, dict):
                continue
            system = entry.get("system")
            code = entry.get("code")
            if system is None or code is None:
                continue
            normalized_system = normalize_german_chars(str(system))
            tokens.append(f"{normalized_system}:{code}")
    return tokens


def build_token_set_for_product(product: dict, stopwords: Set[str]) -> Dict[str, Set[str]]:
    keyword_tokens = set(tokenize_keywords(product.get("keywords"), stopwords))
    description_tokens = set(tokenize_description(product.get("description_short"), stopwords))
    class_code_tokens = set(tokenize_class_codes(product.get("class_codes")))
    return {
        "KEYWORD": keyword_tokens,
        "DESCRIPTION_SHORT": description_tokens,
        "CLASS_CODES": class_code_tokens,
    }


def canonicalize_plural(token: str, vocab: Set[str]) -> str:
    if len(token) < MIN_TOKEN_LENGTH:
        return token
    if token.endswith("en"):
        candidate_drop_n = token[:-1]
        if len(candidate_drop_n) >= MIN_TOKEN_LENGTH and candidate_drop_n.endswith("e"):
            return candidate_drop_n
        candidate2 = token[:-2]
        if len(candidate2) >= MIN_TOKEN_LENGTH and candidate2 in vocab:
            return candidate2
    if token.endswith("n"):
        candidate = token[:-1]
        if len(candidate) >= MIN_TOKEN_LENGTH and candidate in vocab:
            return candidate
    if token.endswith("e"):
        candidate = token[:-1]
        if len(candidate) >= MIN_TOKEN_LENGTH and candidate in vocab:
            return candidate
    if token.endswith("er"):
        candidate = token[:-2]
        if len(candidate) >= MIN_TOKEN_LENGTH and candidate in vocab:
            return candidate
    if token.endswith("s"):
        candidate = token[:-1]
        if len(candidate) >= MIN_TOKEN_LENGTH and candidate in vocab:
            return candidate
    return token


def build_plural_map(vocab: Set[str]) -> Dict[str, str]:
    return {token: canonicalize_plural(token, vocab) for token in vocab}


def build_plural_maps_from_training_set(
    stable_training_set: dict, stopwords: Set[str]
) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, Set[str]]]:
    vocab_by_field: Dict[str, Set[str]] = {
        "KEYWORD": set(),
        "DESCRIPTION_SHORT": set(),
        "CLASS_CODES": set(),
    }

    for record in stable_training_set.values():
        if not isinstance(record, dict):
            continue
        pim_category_id = record.get("pim_category_id")
        if pim_category_id is None:
            continue
        products = record.get("products") or []
        if not isinstance(products, list):
            continue
        for product in products:
            if not isinstance(product, dict):
                continue
            product_token_sets = build_token_set_for_product(product, stopwords=stopwords)
            for field_name, tokens in product_token_sets.items():
                vocab_by_field[field_name].update(tokens)

    plural_map_keyword = build_plural_map(vocab_by_field["KEYWORD"])
    plural_map_description = build_plural_map(vocab_by_field["DESCRIPTION_SHORT"])
    return plural_map_keyword, plural_map_description, vocab_by_field


def load_denylist_config(s3_client, input_bucket: str, key: str) -> dict:
    response = s3_client.get_object(Bucket=input_bucket, Key=key)
    body = response["Body"].read().decode("utf-8")
    denylist_raw = json.loads(body)
    if not isinstance(denylist_raw, dict):
        raise ValueError("Denylist config must be a JSON object")
    schema_version = denylist_raw.get("schema_version")
    denylist_section = denylist_raw.get("denylist")
    if not schema_version or not isinstance(denylist_section, dict):
        raise ValueError("Denylist config missing schema_version or denylist section")

    global_raw = denylist_section.get("global")
    by_field_raw = denylist_section.get("by_field")
    if not isinstance(global_raw, list) or not isinstance(by_field_raw, dict):
        raise ValueError("Denylist config requires denylist.global list and denylist.by_field dict")

    def normalize_entries(values: list) -> Set[str]:
        normalized_values: Set[str] = set()
        for entry in values:
            if isinstance(entry, str) and entry:
                normalized_values.add(normalize_german_chars(entry))
        return normalized_values

    global_set = normalize_entries(global_raw)
    by_field_sets = {
        "KEYWORD": normalize_entries(by_field_raw.get("KEYWORD", [])),
        "DESCRIPTION_SHORT": normalize_entries(by_field_raw.get("DESCRIPTION_SHORT", [])),
    }

    return {
        "global": global_set,
        "by_field": by_field_sets,
    }


def is_denylisted_token(token: str, field_name: str, denylist_config: dict) -> bool:
    if not token:
        return False
    normalized = normalize_german_chars(token)
    field_denylist = denylist_config.get("by_field", {}).get(field_name, set())
    return normalized in denylist_config.get("global", set()) or normalized in field_denylist


def section5_build_unigram_evidence(run_receipt: dict) -> dict:
    input_bucket = run_receipt["input_bucket"]
    run_id = run_receipt["run_id"]
    stable_training_set_key = run_receipt["stable_training_set_key"]

    s3_client = boto3.client("s3")
    denylist_config = load_denylist_config(
        s3_client, input_bucket, DENYLIST_CONFIG_KEY_DEFAULT
    )
    print(
        "Loaded denylist config for unigram evidence from "
        f"s3://{input_bucket}/{DENYLIST_CONFIG_KEY_DEFAULT}"
    )

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    stable_training_set = load_json_from_s3(input_bucket, stable_training_set_key)
    if not isinstance(stable_training_set, dict):
        raise ValueError("StableTrainingSet must be a JSON object keyed by vendor::category")

    stopwords_for_filtering = build_stopword_set()
    plural_map_keyword, plural_map_description, vocab_by_field = build_plural_maps_from_training_set(
        stable_training_set, stopwords_for_filtering
    )

    field_aggregates: Dict[str, Dict[str, dict]] = {
        "KEYWORD": {"by_pim_category": defaultdict(lambda: {"products_total": 0, "token_product_counts": defaultdict(int)})},
        "DESCRIPTION_SHORT": {"by_pim_category": defaultdict(lambda: {"products_total": 0, "token_product_counts": defaultdict(int)})},
        "CLASS_CODES": {"by_pim_category": defaultdict(lambda: {"products_total": 0, "token_product_counts": defaultdict(int)})},
    }
    field_unique_tokens: Dict[str, Set[str]] = {
        "KEYWORD": set(),
        "DESCRIPTION_SHORT": set(),
        "CLASS_CODES": set(),
    }
    plural_changed_counts = {"KEYWORD": 0, "DESCRIPTION_SHORT": 0}
    denylist_removed_counts = {"KEYWORD": 0, "DESCRIPTION_SHORT": 0}

    pim_categories_seen: Set[str] = set()
    product_count_total = 0
    missing_pim_categories = 0
    invalid_product_collections = 0

    for record in stable_training_set.values():
        if not isinstance(record, dict):
            continue
        pim_category_id = record.get("pim_category_id")
        if pim_category_id is None:
            missing_pim_categories += 1
            continue

        pim_categories_seen.add(str(pim_category_id))
        products = record.get("products") or []
        if not isinstance(products, list):
            invalid_product_collections += 1
            continue

        for product in products:
            if not isinstance(product, dict):
                continue
            product_count_total += 1
            product_token_sets = build_token_set_for_product(
                product, stopwords=stopwords_for_filtering
            )

            product_token_sets["KEYWORD"] = {
                plural_map_keyword.get(token, token) for token in product_token_sets["KEYWORD"]
            }
            product_token_sets["DESCRIPTION_SHORT"] = {
                plural_map_description.get(token, token)
                for token in product_token_sets["DESCRIPTION_SHORT"]
            }

            plural_changed_counts["KEYWORD"] += sum(
                1 for token in product_token_sets["KEYWORD"] if token not in vocab_by_field["KEYWORD"]
            )
            plural_changed_counts["DESCRIPTION_SHORT"] += sum(
                1
                for token in product_token_sets["DESCRIPTION_SHORT"]
                if token not in vocab_by_field["DESCRIPTION_SHORT"]
            )

            for field_name in ("KEYWORD", "DESCRIPTION_SHORT"):
                denylist_tokens = denylist_config["global"] | denylist_config["by_field"][field_name]
                if not denylist_tokens:
                    continue
                filtered = {token for token in product_token_sets[field_name] if token not in denylist_tokens}
                denylist_removed_counts[field_name] += (
                    len(product_token_sets[field_name]) - len(filtered)
                )
                product_token_sets[field_name] = filtered

            for field_name, tokens in product_token_sets.items():
                field_entry = field_aggregates[field_name]["by_pim_category"][str(pim_category_id)]
                field_entry["products_total"] += 1
                for token in tokens:
                    field_entry["token_product_counts"][token] += 1
                field_unique_tokens[field_name].update(tokens)

    for field_name, field_data in field_aggregates.items():
        token_category_occurrence_count: Dict[str, int] = defaultdict(int)
        for pim_category_id, pim_data in field_data["by_pim_category"].items():
            for token in pim_data["token_product_counts"].keys():
                token_category_occurrence_count[token] += 1
        field_data["token_category_occurrence_count"] = dict(token_category_occurrence_count)
        # Convert defaultdicts to normal dicts for serialization
        field_data["by_pim_category"] = {
            pim_category_id: {
                "products_total": pim_data["products_total"],
                "token_product_counts": dict(pim_data["token_product_counts"]),
            }
            for pim_category_id, pim_data in field_data["by_pim_category"].items()
        }

    evidence_body = {
        "schema_version": "StableTrainingEvidence_Unigrams_v1",
        "built_at_run_id": run_id,
        "built_from": {"stable_training_set_key": stable_training_set_key},
        "normalization_profile": {
            "normalization_version": NORMALIZATION_VERSION,
            "tokenizer": "[A-Za-z0-9ÄÖÜäöüß]+",
            "normalization": {
                "lowercase": True,
                "strip_leading_trailing_non_alnum": True,
                "german_char_substitution": {
                    "ä": "ae",
                    "ö": "oe",
                    "ü": "ue",
                    "ß": "ss",
                },
            },
            "filtering": {
                "min_token_length": MIN_TOKEN_LENGTH,
                "drop_numeric_only_tokens_in_fields": DROP_NUMERIC_ONLY_FIELDS,
                "stopwords_de_v1_count": len(STOPWORDS_DE_V1),
                "stopwords_de_v1": STOPWORDS_DE_V1,
                "drop_empty_tokens": True,
                "stopwords_applied_after_stemming": False,
            },
            "stemming": {
                "mode": "none",
                "mode_used": "none",
            },
            "plural_normalization": {
                "mode": "en_drop_n_unconditional_plus_vocab_backed_others",
                "rules": [
                    "en->drop n (no vocab) then drop en (vocab-backed)",
                    "n->drop n",
                    "e->drop e",
                    "er->drop er",
                    "s->drop s",
                ],
                "min_candidate_length": MIN_TOKEN_LENGTH,
            },
        },
        "fields": field_aggregates,
    }

    evidence_key = "canonical_mappings/stable_training_sets/StableTrainingEvidence_Unigrams_v1.json"
    s3_client.put_object(Bucket=input_bucket, Key=evidence_key, Body=json.dumps(evidence_body, indent=2))

    outputs_written = run_receipt.setdefault("outputs_written", {})
    outputs_written["stable_training_evidence_unigrams_key"] = evidence_key

    run_receipt.setdefault("counts", {})["stable_training_evidence_unigrams"] = {
        "pim_category_count": len(pim_categories_seen),
        "product_count_total": product_count_total,
        "unique_token_count_by_field": {
            field_name: len(tokens) for field_name, tokens in field_unique_tokens.items()
        },
        "plural_map_size_by_field": {
            "KEYWORD": len(plural_map_keyword),
            "DESCRIPTION_SHORT": len(plural_map_description),
        },
        "plural_normalization_changed_tokens_keyword": plural_changed_counts["KEYWORD"],
        "plural_normalization_changed_tokens_description": plural_changed_counts["DESCRIPTION_SHORT"],
        "denylist_removed_tokens_by_field": denylist_removed_counts,
    }

    if missing_pim_categories:
        run_receipt.setdefault("notes", []).append(
            f"Skipped {missing_pim_categories} StableTrainingSet records without pim_category_id"
        )
    if invalid_product_collections:
        run_receipt.setdefault("notes", []).append(
            f"Skipped {invalid_product_collections} StableTrainingSet records with non-list products"
        )

    return run_receipt


# === Section 6.6: ACTIVE (Build StableTrainingEvidence_Pairs_v1) ===


def section6_6_build_pair_evidence(run_receipt: dict) -> dict:
    input_bucket = run_receipt["input_bucket"]
    run_id = run_receipt["run_id"]
    stable_training_set_key = run_receipt["stable_training_set_key"]
    stable_training_evidence_unigrams_key = run_receipt.get("outputs_written", {}).get(
        "stable_training_evidence_unigrams_key"
    )

    if not stable_training_evidence_unigrams_key:
        raise ValueError("stable_training_evidence_unigrams_key missing from run_receipt outputs")

    s3_client = boto3.client("s3")

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    stable_training_set = load_json_from_s3(input_bucket, stable_training_set_key)
    if not isinstance(stable_training_set, dict):
        raise ValueError("StableTrainingSet must be a JSON object keyed by vendor::category")

    unigram_evidence = load_json_from_s3(input_bucket, stable_training_evidence_unigrams_key)
    normalization_profile = unigram_evidence.get("normalization_profile")
    if not isinstance(normalization_profile, dict):
        raise ValueError("StableTrainingEvidence normalization_profile must be a dict")

    fields = unigram_evidence.get("fields")
    if not isinstance(fields, dict):
        raise ValueError("StableTrainingEvidence fields must be a dict")

    stopwords_for_filtering = build_stopword_set()
    plural_map_keyword, plural_map_description, _ = build_plural_maps_from_training_set(
        stable_training_set, stopwords_for_filtering
    )

    products_total_min = 8
    eligible_token_support_min = 5
    stored_pair_count_min = 5

    eligible_tokens_by_field: Dict[str, Dict[str, Set[str]]] = {
        "KEYWORD": {},
        "DESCRIPTION_SHORT": {},
        "CLASS_CODES": {},
    }

    for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]:
        field_data = fields.get(field_name)
        if not isinstance(field_data, dict):
            raise ValueError(f"StableTrainingEvidence {field_name} section missing or invalid")

        by_pim_category = field_data.get("by_pim_category")
        if not isinstance(by_pim_category, dict):
            raise ValueError(f"StableTrainingEvidence {field_name}.by_pim_category must be a dict")

        for pim_category_id, pim_data in by_pim_category.items():
            if not isinstance(pim_data, dict):
                raise ValueError(
                    f"StableTrainingEvidence {field_name}.by_pim_category entry '{pim_category_id}' must be a dict"
                )

            products_total = pim_data.get("products_total")
            token_product_counts = pim_data.get("token_product_counts")

            if not isinstance(products_total, int):
                raise ValueError(
                    f"StableTrainingEvidence {field_name}.by_pim_category['{pim_category_id}'].products_total must be an int"
                )
            if not isinstance(token_product_counts, dict):
                raise ValueError(
                    f"StableTrainingEvidence {field_name}.by_pim_category['{pim_category_id}'].token_product_counts must be a dict"
                )

            eligible_tokens: Set[str] = set()
            if products_total >= products_total_min:
                for token, count in token_product_counts.items():
                    if not isinstance(count, int):
                        raise ValueError(
                            f"StableTrainingEvidence token_product_counts values must be ints for {field_name}"
                        )
                    if count >= eligible_token_support_min:
                        eligible_tokens.add(token)
            eligible_tokens_by_field[field_name][str(pim_category_id)] = eligible_tokens

    field_pair_aggregates: Dict[str, Dict[str, dict]] = {
        "KEYWORD": {
            "by_pim_category": defaultdict(
                lambda: {"products_total": 0, "pair_counts": defaultdict(int)}
            )
        },
        "DESCRIPTION_SHORT": {
            "by_pim_category": defaultdict(
                lambda: {"products_total": 0, "pair_counts": defaultdict(int)}
            )
        },
        "CLASS_CODES": {
            "by_pim_category": defaultdict(
                lambda: {"products_total": 0, "pair_counts": defaultdict(int)}
            )
        },
    }

    stored_pairs_by_field: Dict[str, Set[str]] = {
        "KEYWORD": set(),
        "DESCRIPTION_SHORT": set(),
        "CLASS_CODES": set(),
    }

    for record in stable_training_set.values():
        if not isinstance(record, dict):
            continue
        pim_category_id = record.get("pim_category_id")
        if pim_category_id is None:
            continue

        products = record.get("products") or []
        if not isinstance(products, list):
            continue

        pim_category_key = str(pim_category_id)

        for product in products:
            if not isinstance(product, dict):
                continue

            product_token_sets = build_token_set_for_product(product, stopwords=stopwords_for_filtering)
            product_token_sets["KEYWORD"] = {
                plural_map_keyword.get(token, token) for token in product_token_sets["KEYWORD"]
            }
            product_token_sets["DESCRIPTION_SHORT"] = {
                plural_map_description.get(token, token)
                for token in product_token_sets["DESCRIPTION_SHORT"]
            }

            for field_name, tokens in product_token_sets.items():
                field_entry = field_pair_aggregates[field_name]["by_pim_category"][
                    pim_category_key
                ]
                field_entry["products_total"] += 1

                eligible_tokens = eligible_tokens_by_field[field_name].get(pim_category_key, set())
                eligible_product_tokens = set(tokens) & eligible_tokens
                if len(eligible_product_tokens) < 2:
                    continue

                sorted_tokens = sorted(eligible_product_tokens)
                for left, right in combinations(sorted_tokens, 2):
                    pair_key = f"{left}||{right}"
                    field_entry["pair_counts"][pair_key] += 1

    fields_output: Dict[str, dict] = {}
    pim_categories_total_by_field: Dict[str, int] = {}
    pim_categories_with_any_pair_by_field: Dict[str, int] = {}
    pairs_total_by_field: Dict[str, int] = {}
    pair_category_occurrence_any_by_field: Dict[str, Dict[str, int]] = {
        "KEYWORD": {},
        "DESCRIPTION_SHORT": {},
        "CLASS_CODES": {},
    }

    for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]:
        by_pim_category_output: Dict[str, dict] = {}
        pair_category_occurrence_count: Dict[str, int] = defaultdict(int)

        for pim_category_id, pim_data in field_pair_aggregates[field_name]["by_pim_category"].items():
            products_total = pim_data["products_total"]
            pair_counts_pruned = {
                pair_key: count
                for pair_key, count in pim_data["pair_counts"].items()
                if count >= stored_pair_count_min
            }
            stored_pairs_by_field[field_name].update(pair_counts_pruned.keys())
            for pair_key in pair_counts_pruned.keys():
                pair_category_occurrence_count[pair_key] += 1

            by_pim_category_output[pim_category_id] = {
                "products_total": products_total,
                "pair_counts": pair_counts_pruned,
            }

        fields_output[field_name] = {
            "by_pim_category": by_pim_category_output,
            "pair_category_occurrence_count": dict(pair_category_occurrence_count),
        }

        pim_categories_total_by_field[field_name] = len(by_pim_category_output)
        pim_categories_with_any_pair_by_field[field_name] = sum(
            1 for entry in by_pim_category_output.values() if entry["pair_counts"]
        )
        pairs_total_by_field[field_name] = sum(
            len(entry["pair_counts"]) for entry in by_pim_category_output.values()
        )

    # Pass 2: compute occurrence_any for stored pairs only
    pair_seen_categories_by_field: Dict[str, Dict[str, Set[str]]] = {
        "KEYWORD": defaultdict(set),
        "DESCRIPTION_SHORT": defaultdict(set),
        "CLASS_CODES": defaultdict(set),
    }
    pair_counts_any_by_field: Dict[str, Dict[str, Dict[str, int]]] = {
        "KEYWORD": defaultdict(lambda: defaultdict(int)),
        "DESCRIPTION_SHORT": defaultdict(lambda: defaultdict(int)),
        "CLASS_CODES": defaultdict(lambda: defaultdict(int)),
    }

    tokens_in_stored_pairs: Dict[str, Set[str]] = {
        field_name: set() for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]
    }
    for field_name, stored_pairs in stored_pairs_by_field.items():
        for pair_key in stored_pairs:
            parts = pair_key.split("||")
            if len(parts) != 2:
                continue
            tokens_in_stored_pairs[field_name].update(parts)

    for record in stable_training_set.values():
        if not isinstance(record, dict):
            continue
        pim_category_id = record.get("pim_category_id")
        if pim_category_id is None:
            continue

        products = record.get("products") or []
        if not isinstance(products, list):
            continue

        pim_category_key = str(pim_category_id)

        for product in products:
            if not isinstance(product, dict):
                continue

            product_token_sets = build_token_set_for_product(product, stopwords=stopwords_for_filtering)
            product_token_sets["KEYWORD"] = {
                plural_map_keyword.get(token, token) for token in product_token_sets["KEYWORD"]
            }
            product_token_sets["DESCRIPTION_SHORT"] = {
                plural_map_description.get(token, token)
                for token in product_token_sets["DESCRIPTION_SHORT"]
            }

            for field_name, tokens in product_token_sets.items():
                candidate_tokens = set(tokens) & tokens_in_stored_pairs[field_name]
                if len(candidate_tokens) < 2:
                    continue

                sorted_tokens = sorted(candidate_tokens)
                for left, right in combinations(sorted_tokens, 2):
                    pair_key = f"{left}||{right}"
                    if pair_key not in stored_pairs_by_field[field_name]:
                        continue
                    pair_counts_any_by_field[field_name][pim_category_key][pair_key] += 1
                    pair_seen_categories_by_field[field_name][pair_key].add(pim_category_key)

    for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]:
        pair_category_occurrence_any_by_field[field_name] = {
            pair_key: len(categories)
            for pair_key, categories in pair_seen_categories_by_field[field_name].items()
        }
        for pim_category_id, pim_entry in fields_output[field_name]["by_pim_category"].items():
            pair_counts_any = pair_counts_any_by_field[field_name].get(pim_category_id, {})
            pim_entry["pair_counts_any"] = dict(pair_counts_any)

    evidence_body = {
        "schema_version": "StableTrainingEvidence_Pairs_v1",
        "built_at_run_id": run_id,
        "built_from": {
            "stable_training_set_key": stable_training_set_key,
            "stable_training_evidence_unigrams_key": stable_training_evidence_unigrams_key,
        },
        "normalization_profile": normalization_profile,
        "pair_policy": {
            "products_total_min": products_total_min,
            "eligible_token_support_min": eligible_token_support_min,
            "stored_pair_count_min": stored_pair_count_min,
            "pair_key_format": "token||token",
            "pair_sort_order": "lexicographic_a_lt_b",
            "counting": "presence_based_per_product",
            "pair_category_occurrence_any": "stored pairs only; categories with >=1 occurrence (supports contains_all outside==0)",
        },
        "fields": fields_output,
    }

    for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]:
        evidence_body["fields"][field_name]["pair_category_occurrence_any"] = (
            pair_category_occurrence_any_by_field[field_name]
        )

    evidence_key = "canonical_mappings/stable_training_sets/StableTrainingEvidence_Pairs_v1.json"
    s3_client.put_object(Bucket=input_bucket, Key=evidence_key, Body=json.dumps(evidence_body, indent=2))

    outputs_written = run_receipt.setdefault("outputs_written", {})
    outputs_written["stable_training_evidence_pairs_key"] = evidence_key

    run_receipt.setdefault("counts", {})["stable_training_evidence_pairs"] = {
        "pim_categories_total_by_field": pim_categories_total_by_field,
        "pim_categories_with_any_pair_by_field": pim_categories_with_any_pair_by_field,
        "pairs_total_by_field": pairs_total_by_field,
        "pairs_any_occurrence_indexed_by_field": {
            field_name: len(pair_category_occurrence_any_by_field[field_name])
            for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]
        },
    }

    return run_receipt


# === Section 6.1: ACTIVE (Load StableTrainingEvidence + field global aggregates) ===


def _compute_field_globals(evidence: dict, field_name: str) -> Tuple[dict, Dict[str, int]]:
    fields = evidence.get("fields")
    if not isinstance(fields, dict):
        raise ValueError("StableTrainingEvidence fields must be a dict")

    field_data = fields.get(field_name)
    if not isinstance(field_data, dict):
        raise ValueError(f"StableTrainingEvidence {field_name} section missing or invalid")

    by_pim_category = field_data.get("by_pim_category")
    if not isinstance(by_pim_category, dict):
        raise ValueError(f"StableTrainingEvidence {field_name}.by_pim_category must be a dict")

    global_products_total = 0
    global_token_support_count: Dict[str, int] = defaultdict(int)

    for pim_category_id, pim_data in by_pim_category.items():
        if not isinstance(pim_data, dict):
            raise ValueError(
                f"StableTrainingEvidence {field_name}.by_pim_category entry '{pim_category_id}' must be a dict"
            )

        products_total = pim_data.get("products_total")
        token_product_counts = pim_data.get("token_product_counts")

        if not isinstance(products_total, int):
            raise ValueError(
                f"StableTrainingEvidence {field_name}.by_pim_category['{pim_category_id}'].products_total must be an int"
            )
        if not isinstance(token_product_counts, dict):
            raise ValueError(
                f"StableTrainingEvidence {field_name}.by_pim_category['{pim_category_id}'].token_product_counts must be a dict"
            )

        global_products_total += products_total

        for token, count in token_product_counts.items():
            if not isinstance(count, int):
                raise ValueError(
                    f"StableTrainingEvidence token_product_counts values must be ints for {field_name}"
                )
            global_token_support_count[token] += count

    token_category_occurrence_count = field_data.get("token_category_occurrence_count")
    used_occurrence_from_evidence = isinstance(token_category_occurrence_count, dict)

    if not used_occurrence_from_evidence:
        computed_occurrence_count: Dict[str, int] = defaultdict(int)
        for pim_data in by_pim_category.values():
            token_product_counts = pim_data.get("token_product_counts", {})
            if not isinstance(token_product_counts, dict):
                raise ValueError(
                    f"StableTrainingEvidence {field_name}.by_pim_category entries must contain token_product_counts dicts"
                )
            for token, count in token_product_counts.items():
                if not isinstance(count, int):
                    raise ValueError(
                        f"StableTrainingEvidence token_product_counts values must be ints for {field_name}"
                    )
                if count > 0:
                    computed_occurrence_count[token] += 1
        token_category_occurrence_count = dict(computed_occurrence_count)
    else:
        token_category_occurrence_count = dict(token_category_occurrence_count)

    if global_products_total == 0:
        raise ValueError(f"StableTrainingEvidence {field_name}.products_total sum is zero; cannot build support index")

    field_globals = {
        "pim_category_count": len(by_pim_category),
        "global_products_total": global_products_total,
        "global_token_support_count": dict(global_token_support_count),
        "token_category_occurrence_count": token_category_occurrence_count,
        "used_occurrence_from_evidence": used_occurrence_from_evidence,
    }

    return field_globals, by_pim_category


def section6_1_load_field_globals(run_receipt: dict) -> Tuple[dict, dict]:
    input_bucket = run_receipt["input_bucket"]
    evidence_key = run_receipt.get("outputs_written", {}).get(
        "stable_training_evidence_unigrams_key"
    )

    if not evidence_key:
        raise ValueError("stable_training_evidence_unigrams_key missing from run_receipt outputs")

    s3_client = boto3.client("s3")

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    evidence = load_json_from_s3(input_bucket, evidence_key)

    normalization_profile = evidence.get("normalization_profile")
    if not isinstance(normalization_profile, dict):
        raise ValueError("StableTrainingEvidence normalization_profile must be a dict")

    if "normalization_version" not in normalization_profile:
        raise ValueError("StableTrainingEvidence normalization_version missing in normalization_profile")

    normalization_version = normalization_profile["normalization_version"]

    field_globals: Dict[str, dict] = {"normalization_version": normalization_version}

    for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]:
        globals_for_field, by_pim_category = _compute_field_globals(evidence, field_name)

        field_globals[field_name] = {
            "pim_category_count": globals_for_field["pim_category_count"],
            "global_products_total": globals_for_field["global_products_total"],
            "global_token_support_count": globals_for_field["global_token_support_count"],
            "token_category_occurrence_count": globals_for_field["token_category_occurrence_count"],
        }

    return run_receipt, field_globals


def section6_2_generate_contains_any_rules(
    run_receipt: dict,
    field_globals: dict,
    evidence: dict | None = None,
) -> Tuple[dict, Dict[str, List[dict]], dict]:
    input_bucket = run_receipt["input_bucket"]
    evidence_key = run_receipt.get("outputs_written", {}).get(
        "stable_training_evidence_unigrams_key"
    )

    if not evidence_key:
        raise ValueError("stable_training_evidence_unigrams_key missing from run_receipt outputs")

    s3_client = boto3.client("s3")

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    evidence = evidence or load_json_from_s3(input_bucket, evidence_key)

    normalization_profile = evidence.get("normalization_profile")
    if not isinstance(normalization_profile, dict):
        raise ValueError("StableTrainingEvidence normalization_profile must be a dict")

    if "normalization_version" not in normalization_profile:
        raise ValueError("StableTrainingEvidence normalization_version missing in normalization_profile")

    fields = evidence.get("fields")
    if not isinstance(fields, dict):
        raise ValueError("StableTrainingEvidence fields must be a dict")

    rules_by_pim_category: Dict[str, List[dict]] = defaultdict(list)
    total_rules_generated = 0
    rules_total_by_field: Dict[str, int] = defaultdict(int)

    products_total_min = 8
    support_ratio_min = 0.60
    support_count_min = 5

    def generate_rules_for_field(field_name: str):
        nonlocal total_rules_generated

        field_data = fields.get(field_name)
        if not isinstance(field_data, dict):
            raise ValueError(f"StableTrainingEvidence {field_name} section missing or invalid")

        by_pim_category = field_data.get("by_pim_category")
        if not isinstance(by_pim_category, dict):
            raise ValueError(f"StableTrainingEvidence {field_name}.by_pim_category must be a dict")

        globals_for_field = field_globals.get(field_name)
        if not isinstance(globals_for_field, dict):
            raise ValueError(f"field_globals missing required entry for {field_name}")

        global_products_total = globals_for_field.get("global_products_total")
        if not isinstance(global_products_total, int):
            raise ValueError(f"field_globals[{field_name}] missing required int global_products_total")

        global_token_support_count = globals_for_field.get("global_token_support_count")
        if not isinstance(global_token_support_count, dict):
            raise ValueError(
                f"field_globals[{field_name}] missing required dict global_token_support_count"
            )

        token_category_occurrence_count = globals_for_field.get("token_category_occurrence_count", {})
        if not isinstance(token_category_occurrence_count, dict):
            raise ValueError(
                f"field_globals[{field_name}] token_category_occurrence_count must be a dict"
            )

        for pim_category_id, pim_data in by_pim_category.items():
            if not isinstance(pim_data, dict):
                raise ValueError(
                    f"StableTrainingEvidence {field_name}.by_pim_category entry '{pim_category_id}' must be a dict"
                )

            products_total = pim_data.get("products_total")
            token_product_counts = pim_data.get("token_product_counts")

            if not isinstance(products_total, int):
                raise ValueError(
                    f"StableTrainingEvidence {field_name}.by_pim_category['{pim_category_id}'].products_total must be an int"
                )
            if products_total < products_total_min:
                continue

            if not isinstance(token_product_counts, dict):
                raise ValueError(
                    f"StableTrainingEvidence {field_name}.by_pim_category['{pim_category_id}'].token_product_counts must be a dict"
                )

            for token, inside_support in token_product_counts.items():
                if not isinstance(inside_support, int):
                    raise ValueError(
                        f"StableTrainingEvidence token_product_counts values must be ints for {field_name}"
                    )

                inside_ratio = inside_support / products_total if products_total else 0.0
                if not (inside_ratio >= support_ratio_min or inside_support >= support_count_min):
                    continue

                outside_total = global_products_total - products_total
                outside_support = global_token_support_count.get(token, 0) - inside_support
                outside_categories_with_support_count = (
                    token_category_occurrence_count.get(token, 0) - 1
                )
                if outside_support != 0:
                    continue

                values_include = [token]
                values_exclude: List[str] = []
                include_str = ",".join(sorted(values_include))
                exclude_str = ",".join(sorted(values_exclude))
                rule_id_source = (
                    f"{pim_category_id}|{field_name}|contains_any|{include_str}|{exclude_str}"
                )
                rule_id = hashlib.sha1(rule_id_source.encode("utf-8")).hexdigest()

                rule = {
                    "rule_id": rule_id,
                    "rule_spec": {
                        "field_name": field_name,
                        "operator": "contains_any",
                        "values_include": values_include,
                        "values_exclude": values_exclude,
                    },
                    "training_proof": {
                        "training_inside_products_total": products_total,
                        "training_inside_support_count": inside_support,
                        "training_inside_support_ratio": inside_ratio,
                        "training_outside_products_total": outside_total,
                        "training_outside_support_count": outside_support,
                        "training_outside_categories_with_support_count": max(
                            outside_categories_with_support_count, 0
                        ),
                    },
                    "lifecycle": {
                        "created_run_id": run_receipt.get("run_id"),
                        "status": "active_unvalidated",
                        "last_validated_run_id": None,
                    },
                }

                rules_by_pim_category[str(pim_category_id)].append(rule)
                total_rules_generated += 1
                rules_total_by_field[field_name] += 1

    for field in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]:
        generate_rules_for_field(field)

    fields_processed = ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]
    rules_summary = {
        "normalization_version": field_globals.get("normalization_version"),
        "total_rules_generated": total_rules_generated,
        "categories_with_rules": sum(1 for rules in rules_by_pim_category.values() if rules),
        "rules_total_by_field": {
            field_name: rules_total_by_field.get(field_name, 0) for field_name in fields_processed
        },
        "rules_total_by_operator": {"contains_any": total_rules_generated},
    }

    return run_receipt, dict(rules_by_pim_category), rules_summary


def section6_7_generate_contains_all_rules(
    run_receipt: dict,
    rules_by_pim_category: Dict[str, List[dict]],
    rules_summary: dict | None = None,
) -> Tuple[dict, Dict[str, List[dict]], dict]:
    input_bucket = run_receipt["input_bucket"]
    evidence_key = run_receipt.get("outputs_written", {}).get(
        "stable_training_evidence_pairs_key"
    )

    if not evidence_key:
        raise ValueError("stable_training_evidence_pairs_key missing from run_receipt outputs")

    s3_client = boto3.client("s3")

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    evidence = load_json_from_s3(input_bucket, evidence_key)
    fields = evidence.get("fields")
    if not isinstance(fields, dict):
        raise ValueError("StableTrainingEvidence_Pairs fields must be a dict")

    products_total_min = 8
    support_ratio_min = 0.60
    support_count_min = 5

    contains_all_total_by_field: Dict[str, int] = defaultdict(int)
    mutable_rules_by_category: Dict[str, List[dict]] = defaultdict(list)

    for pim_category_id, rules in rules_by_pim_category.items():
        mutable_rules_by_category[str(pim_category_id)].extend(rules)

    for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]:
        field_data = fields.get(field_name)
        if not isinstance(field_data, dict):
            raise ValueError(f"StableTrainingEvidence_Pairs {field_name} section missing or invalid")

        by_pim_category = field_data.get("by_pim_category")
        if not isinstance(by_pim_category, dict):
            raise ValueError(
                f"StableTrainingEvidence_Pairs {field_name}.by_pim_category must be a dict"
            )

        pair_category_occurrence_any = field_data.get("pair_category_occurrence_any", {})
        if not isinstance(pair_category_occurrence_any, dict):
            raise ValueError(
                f"StableTrainingEvidence_Pairs {field_name}.pair_category_occurrence_any must be a dict"
            )

        for pim_category_id, pim_data in by_pim_category.items():
            if not isinstance(pim_data, dict):
                raise ValueError(
                    f"StableTrainingEvidence_Pairs {field_name}.by_pim_category entry '{pim_category_id}' must be a dict"
                )

            products_total = pim_data.get("products_total")
            pair_counts = pim_data.get("pair_counts")

            if not isinstance(products_total, int):
                raise ValueError(
                    f"StableTrainingEvidence_Pairs {field_name}.by_pim_category['{pim_category_id}'].products_total must be an int"
                )
            if products_total < products_total_min:
                continue

            if not isinstance(pair_counts, dict):
                raise ValueError(
                    f"StableTrainingEvidence_Pairs {field_name}.by_pim_category['{pim_category_id}'].pair_counts must be a dict"
                )

            for pair_key, inside_support in pair_counts.items():
                if not isinstance(inside_support, int):
                    raise ValueError(
                        f"StableTrainingEvidence_Pairs {field_name} pair_counts values must be ints"
                    )

                parts = pair_key.split("||")
                if len(parts) != 2:
                    continue
                values_include = [parts[0], parts[1]]

                inside_ratio = inside_support / products_total if products_total else 0.0
                if not (inside_support >= support_count_min or inside_ratio >= support_ratio_min):
                    continue

                outside_occurrence_any = pair_category_occurrence_any.get(pair_key, 0)
                if outside_occurrence_any != 1:
                    continue

                values_exclude: List[str] = []
                include_str = ",".join(values_include)
                exclude_str = ",".join(sorted(values_exclude))
                rule_id_source = (
                    f"{pim_category_id}|{field_name}|contains_all|{include_str}|{exclude_str}"
                )
                rule_id = hashlib.sha1(rule_id_source.encode("utf-8")).hexdigest()

                rule = {
                    "rule_id": rule_id,
                    "rule_spec": {
                        "field_name": field_name,
                        "operator": "contains_all",
                        "values_include": values_include,
                        "values_exclude": values_exclude,
                    },
                    "training_proof": {
                        "training_inside_products_total": products_total,
                        "training_inside_support_count": inside_support,
                        "training_inside_support_ratio": inside_ratio,
                        "training_outside_support_count": 0,
                        "training_outside_categories_with_support_count": 0,
                        "training_uniqueness_basis": "pair_category_occurrence_any==1",
                    },
                    "evidence_source": "StableTrainingEvidence_Pairs_v1",
                    "lifecycle": {
                        "created_run_id": run_receipt.get("run_id"),
                        "status": "active_unvalidated",
                        "last_validated_run_id": None,
                    },
                }

                mutable_rules_by_category[str(pim_category_id)].append(rule)
                contains_all_total_by_field[field_name] += 1

    rules_total_by_field: Dict[str, int] = defaultdict(int)
    if rules_summary and "rules_total_by_field" in rules_summary:
        for field_name, count in rules_summary.get("rules_total_by_field", {}).items():
            rules_total_by_field[field_name] = count

    for field_name, added_count in contains_all_total_by_field.items():
        rules_total_by_field[field_name] += added_count

    rules_total_by_operator: Dict[str, int] = defaultdict(int)
    if rules_summary and "rules_total_by_operator" in rules_summary:
        for operator, count in rules_summary.get("rules_total_by_operator", {}).items():
            rules_total_by_operator[operator] = count
    rules_total_by_operator["contains_all"] += sum(contains_all_total_by_field.values())

    total_rules_generated_base = rules_summary.get("total_rules_generated", 0) if rules_summary else 0
    contains_all_total = sum(contains_all_total_by_field.values())
    total_rules_generated = total_rules_generated_base + contains_all_total

    categories_with_rules = sum(1 for rules in mutable_rules_by_category.values() if rules)

    updated_rules_summary = dict(rules_summary or {})
    updated_rules_summary.update(
        {
            "total_rules_generated": total_rules_generated,
            "categories_with_rules": categories_with_rules,
            "rules_total_by_field": {
                field: rules_total_by_field.get(field, 0)
                for field in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]
            },
            "rules_total_by_operator": dict(rules_total_by_operator),
        }
    )

    return run_receipt, dict(mutable_rules_by_category), updated_rules_summary


def section6_8_generate_contains_any_exclude_any_rules(
    run_receipt: dict,
    field_globals: dict,
    rules_by_pim_category: Dict[str, List[dict]],
    rules_summary: dict | None = None,
) -> Tuple[dict, Dict[str, List[dict]], dict]:
    input_bucket = run_receipt["input_bucket"]
    evidence_key_unigrams = run_receipt.get("outputs_written", {}).get(
        "stable_training_evidence_unigrams_key"
    )
    evidence_key_pairs = run_receipt.get("outputs_written", {}).get(
        "stable_training_evidence_pairs_key"
    )

    if not evidence_key_unigrams:
        raise ValueError("stable_training_evidence_unigrams_key missing from run_receipt outputs")
    if not evidence_key_pairs:
        raise ValueError("stable_training_evidence_pairs_key missing from run_receipt outputs")

    s3_client = boto3.client("s3")

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    unigram_evidence = load_json_from_s3(input_bucket, evidence_key_unigrams)
    pair_evidence = load_json_from_s3(input_bucket, evidence_key_pairs)

    unigram_fields = unigram_evidence.get("fields")
    pair_fields = pair_evidence.get("fields")
    if not isinstance(unigram_fields, dict):
        raise ValueError("StableTrainingEvidence_Unigrams fields must be a dict")
    if not isinstance(pair_fields, dict):
        raise ValueError("StableTrainingEvidence_Pairs fields must be a dict")

    products_total_min = 8
    support_ratio_min = 0.60
    support_count_min = 5

    mutable_rules_by_category: Dict[str, List[dict]] = defaultdict(list)
    existing_rule_ids_by_category: Dict[str, Set[str]] = defaultdict(set)

    for pim_category_id, rules in rules_by_pim_category.items():
        mutable_rules_by_category[str(pim_category_id)].extend(rules)
        existing_rule_ids_by_category[str(pim_category_id)].update(
            rule.get("rule_id") for rule in rules if isinstance(rule, dict)
        )

    base_rules_total = sum(len(rules) for rules in rules_by_pim_category.values())

    adjacency_map_by_field: Dict[str, Dict[str, Set[str]]] = {
        "KEYWORD": defaultdict(set),
        "DESCRIPTION_SHORT": defaultdict(set),
        "CLASS_CODES": defaultdict(set),
    }
    pair_counts_any_by_field: Dict[str, Dict[str, Dict[str, int]]] = {
        "KEYWORD": {},
        "DESCRIPTION_SHORT": {},
        "CLASS_CODES": {},
    }

    for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]:
        pair_field_data = pair_fields.get(field_name)
        if not isinstance(pair_field_data, dict):
            raise ValueError(f"StableTrainingEvidence_Pairs {field_name} section missing or invalid")

        by_pim_category_pairs = pair_field_data.get("by_pim_category")
        if not isinstance(by_pim_category_pairs, dict):
            raise ValueError(
                f"StableTrainingEvidence_Pairs {field_name}.by_pim_category must be a dict"
            )

        for pim_data in by_pim_category_pairs.values():
            pair_counts = pim_data.get("pair_counts", {})
            if not isinstance(pair_counts, dict):
                raise ValueError(
                    f"StableTrainingEvidence_Pairs {field_name}.by_pim_category entries must contain pair_counts dicts"
                )
            for pair_key in pair_counts.keys():
                parts = pair_key.split("||")
                if len(parts) != 2:
                    continue
                left, right = parts
                adjacency_map_by_field[field_name][left].add(right)
                adjacency_map_by_field[field_name][right].add(left)

        pair_counts_any_by_field[field_name] = {
            str(cat_id): pim_entry.get("pair_counts_any", {})
            for cat_id, pim_entry in by_pim_category_pairs.items()
            if isinstance(pim_entry, dict)
        }

    contains_any_exclude_any_total_by_field: Dict[str, int] = defaultdict(int)

    for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]:
        field_data_unigram = unigram_fields.get(field_name)
        field_data_pair = pair_fields.get(field_name)
        if not isinstance(field_data_unigram, dict):
            raise ValueError(f"StableTrainingEvidence_Unigrams {field_name} section missing or invalid")
        if not isinstance(field_data_pair, dict):
            raise ValueError(f"StableTrainingEvidence_Pairs {field_name} section missing or invalid")

        by_pim_category_unigram = field_data_unigram.get("by_pim_category")
        by_pim_category_pair = field_data_pair.get("by_pim_category")
        if not isinstance(by_pim_category_unigram, dict):
            raise ValueError(
                f"StableTrainingEvidence_Unigrams {field_name}.by_pim_category must be a dict"
            )
        if not isinstance(by_pim_category_pair, dict):
            raise ValueError(f"StableTrainingEvidence_Pairs {field_name}.by_pim_category must be a dict")

        globals_for_field = field_globals.get(field_name)
        if not isinstance(globals_for_field, dict):
            raise ValueError(f"field_globals missing required entry for {field_name}")

        global_products_total = globals_for_field.get("global_products_total")
        token_category_occurrence_count = globals_for_field.get("token_category_occurrence_count", {})
        if not isinstance(global_products_total, int):
            raise ValueError(f"field_globals[{field_name}] missing required int global_products_total")
        if not isinstance(token_category_occurrence_count, dict):
            raise ValueError(
                f"field_globals[{field_name}] token_category_occurrence_count must be a dict"
            )

        for pim_category_id, pim_data in by_pim_category_unigram.items():
            if not isinstance(pim_data, dict):
                raise ValueError(
                    f"StableTrainingEvidence_Unigrams {field_name}.by_pim_category entry '{pim_category_id}' must be a dict"
                )

            products_total = pim_data.get("products_total")
            token_product_counts = pim_data.get("token_product_counts")
            if not isinstance(products_total, int):
                raise ValueError(
                    f"StableTrainingEvidence_Unigrams {field_name}.by_pim_category['{pim_category_id}'].products_total must be an int"
                )
            if products_total < products_total_min:
                continue
            if not isinstance(token_product_counts, dict):
                raise ValueError(
                    f"StableTrainingEvidence_Unigrams {field_name}.by_pim_category['{pim_category_id}'].token_product_counts must be a dict"
                )

            pim_category_key = str(pim_category_id)
            pair_counts_any = pair_counts_any_by_field[field_name].get(pim_category_key, {})
            adjacency_map = adjacency_map_by_field[field_name]

            eligible_include_tokens: List[str] = []
            for token, support_count in token_product_counts.items():
                if not isinstance(support_count, int):
                    raise ValueError(
                        f"StableTrainingEvidence token_product_counts values must be ints for {field_name}"
                    )
                support_ratio = support_count / products_total if products_total else 0.0
                if not (support_count >= support_count_min or support_ratio >= support_ratio_min):
                    continue
                if token_category_occurrence_count.get(token, 0) <= 1:
                    continue
                eligible_include_tokens.append(token)

            for token in eligible_include_tokens:
                neighbors = adjacency_map.get(token, set())
                if not neighbors:
                    continue

                token_support_count = token_product_counts.get(token, 0)
                for neighbor in neighbors:
                    if token == neighbor:
                        continue
                    left, right = sorted([token, neighbor])
                    pair_key = f"{left}||{right}"

                    inside_pair_any_support = pair_counts_any.get(pair_key, 0)
                    inside_support_without_neighbor = token_support_count - inside_pair_any_support
                    if inside_support_without_neighbor <= 0:
                        continue

                    inside_support_ratio = (
                        inside_support_without_neighbor / products_total if products_total else 0.0
                    )
                    if not (
                        inside_support_without_neighbor >= support_count_min
                        or inside_support_ratio >= support_ratio_min
                    ):
                        continue

                    outside_support_count = 0
                    outside_categories_with_support_count = 0

                    for other_category_id, other_unigram_data in by_pim_category_unigram.items():
                        other_category_key = str(other_category_id)
                        if other_category_key == pim_category_key:
                            continue
                        other_token_counts = other_unigram_data.get("token_product_counts", {})
                        if not isinstance(other_token_counts, dict):
                            raise ValueError(
                                f"StableTrainingEvidence_Unigrams {field_name}.by_pim_category entries must contain token_product_counts dicts"
                            )
                        other_token_support = other_token_counts.get(token, 0)

                        other_pair_counts_any = by_pim_category_pair.get(other_category_key, {}).get(
                            "pair_counts_any", {}
                        )
                        other_pair_support = other_pair_counts_any.get(pair_key, 0)
                        outside_support_without_neighbor = other_token_support - other_pair_support
                        if outside_support_without_neighbor > 0:
                            outside_support_count += outside_support_without_neighbor
                            outside_categories_with_support_count += 1
                            break

                    if outside_support_count != 0 or outside_categories_with_support_count != 0:
                        continue

                    outside_products_total = global_products_total - products_total

                    values_include = [token]
                    values_exclude = [neighbor]
                    include_str = ",".join(sorted(values_include))
                    exclude_str = ",".join(sorted(values_exclude))
                    rule_id_source = (
                        f"{pim_category_key}|{field_name}|contains_any_exclude_any|{include_str}|{exclude_str}"
                    )
                    rule_id = hashlib.sha1(rule_id_source.encode("utf-8")).hexdigest()

                    if rule_id in existing_rule_ids_by_category[pim_category_key]:
                        continue

                    rule = {
                        "rule_id": rule_id,
                        "rule_spec": {
                            "field_name": field_name,
                            "operator": "contains_any_exclude_any",
                            "values_include": values_include,
                            "values_exclude": values_exclude,
                        },
                        "training_proof": {
                            "training_inside_products_total": products_total,
                            "training_inside_support_count": inside_support_without_neighbor,
                            "training_inside_support_ratio": inside_support_ratio,
                            "training_inside_support_count_a": token_support_count,
                            "training_inside_support_count_pair": inside_pair_any_support,
                            "training_outside_products_total": outside_products_total,
                            "training_outside_support_count": outside_support_count,
                            "training_outside_categories_with_support_count": outside_categories_with_support_count,
                            "training_uniqueness_basis": "outside_support==0_for_A_and_not_B",
                        },
                        "evidence_source": "StableTrainingEvidence_Pairs_v1",
                        "lifecycle": {
                            "created_run_id": run_receipt.get("run_id"),
                            "status": "active_unvalidated",
                            "last_validated_run_id": None,
                        },
                    }

                    mutable_rules_by_category[pim_category_key].append(rule)
                    existing_rule_ids_by_category[pim_category_key].add(rule_id)
                    contains_any_exclude_any_total_by_field[field_name] += 1

    total_added = sum(contains_any_exclude_any_total_by_field.values())

    rules_total_by_field: Dict[str, int] = defaultdict(int)
    if rules_summary and "rules_total_by_field" in rules_summary:
        for field_name, count in rules_summary.get("rules_total_by_field", {}).items():
            rules_total_by_field[field_name] = count

    for field_name, added_count in contains_any_exclude_any_total_by_field.items():
        rules_total_by_field[field_name] += added_count

    rules_total_by_operator: Dict[str, int] = defaultdict(int)
    if rules_summary and "rules_total_by_operator" in rules_summary:
        for operator, count in rules_summary.get("rules_total_by_operator", {}).items():
            rules_total_by_operator[operator] = count
    rules_total_by_operator["contains_any_exclude_any"] += total_added

    base_total_rules_generated = rules_summary.get("total_rules_generated", base_rules_total) if rules_summary else base_rules_total
    total_rules_generated = base_total_rules_generated + total_added

    categories_with_rules = sum(1 for rules in mutable_rules_by_category.values() if rules)

    updated_rules_summary = dict(rules_summary or {})
    updated_rules_summary.update(
        {
            "total_rules_generated": total_rules_generated,
            "categories_with_rules": categories_with_rules,
            "rules_total_by_field": {
                field: rules_total_by_field.get(field, 0)
                for field in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]
            },
            "rules_total_by_operator": dict(rules_total_by_operator),
        }
    )

    run_receipt.setdefault("counts", {}).setdefault("contains_any_exclude_any_rules", {})
    run_receipt["counts"]["contains_any_exclude_any_rules"].update(
        {
            "total_rules_added": total_added,
            "rules_total_by_field": dict(contains_any_exclude_any_total_by_field),
        }
    )

    return run_receipt, dict(mutable_rules_by_category), updated_rules_summary


def section6_3_write_rules_snapshot(
    run_receipt: dict,
    field_globals: dict,
    rules_by_pim_category: Dict[str, List[dict]],
    rules_summary: dict | None = None,
) -> dict:
    run_id = run_receipt["run_id"]
    vendor_name = run_receipt["vendor_name"]
    prepared_output_prefix = run_receipt["prepared_output_prefix"]
    output_bucket = run_receipt["output_bucket"]
    category_mapping_reference_key_selected = run_receipt["category_mapping_reference_key_selected"]
    stable_training_set_key = run_receipt.get("outputs_written", {}).get("stable_training_set_key")
    stable_training_evidence_unigrams_key = run_receipt.get("outputs_written", {}).get(
        "stable_training_evidence_unigrams_key"
    )
    stable_training_evidence_pairs_key = run_receipt.get("outputs_written", {}).get(
        "stable_training_evidence_pairs_key"
    )

    if not stable_training_set_key or not stable_training_evidence_unigrams_key:
        raise ValueError("Stable training outputs missing from run_receipt outputs_written for rules snapshot")

    s3_client = boto3.client("s3")

    evidence_key = stable_training_evidence_unigrams_key

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    evidence = load_json_from_s3(run_receipt["input_bucket"], evidence_key)

    keyword_field = evidence.get("fields", {}).get("KEYWORD")
    if not isinstance(keyword_field, dict):
        raise ValueError("StableTrainingEvidence KEYWORD section missing or invalid when writing rules snapshot")
    by_pim_category = keyword_field.get("by_pim_category")
    if not isinstance(by_pim_category, dict):
        raise ValueError("StableTrainingEvidence KEYWORD.by_pim_category must be a dict when writing rules snapshot")

    keyword_globals = field_globals.get("KEYWORD", {})

    pim_category_count_keyword = keyword_globals.get("pim_category_count") or len(by_pim_category)

    if rules_summary is None:
        total_rules_generated = sum(len(rules) for rules in rules_by_pim_category.values())
        categories_with_rules = sum(1 for rules in rules_by_pim_category.values() if rules)
        field_totals = {"KEYWORD": 0, "DESCRIPTION_SHORT": 0, "CLASS_CODES": 0}
        operator_totals: Dict[str, int] = defaultdict(int)
        for rules in rules_by_pim_category.values():
            for rule in rules:
                field_name = rule.get("rule_spec", {}).get("field_name")
                if field_name in field_totals:
                    field_totals[field_name] += 1
                operator = rule.get("rule_spec", {}).get("operator")
                if operator:
                    operator_totals[operator] += 1
        rules_summary = {
            "normalization_version": field_globals.get("normalization_version"),
            "total_rules_generated": total_rules_generated,
            "categories_with_rules": categories_with_rules,
            "rules_total_by_field": field_totals,
            "rules_total_by_operator": dict(operator_totals),
        }

    rules_snapshot_key = (
        f"{prepared_output_prefix}/mappingMethodTraining/rules_snapshot/"
        f"rules_snapshot_{vendor_name}_{run_id}.json"
    )

    built_from = {
        "stable_training_set_key": stable_training_set_key,
        "stable_training_evidence_unigrams_key": stable_training_evidence_unigrams_key,
        "category_mapping_reference_key_selected": category_mapping_reference_key_selected,
    }
    if stable_training_evidence_pairs_key is not None:
        built_from["stable_training_evidence_pairs_key"] = stable_training_evidence_pairs_key

    snapshot_body = {
        "schema_version": "MappingMethodTraining_RulesSnapshot_v1",
        "built_at_run_id": run_id,
        "built_from": built_from,
        "normalization_ref": {
            "normalization_version": field_globals.get("normalization_version"),
        },
        "threshold_policy": THRESHOLD_POLICY,
        "training_universe_summary": {
            "pim_category_count": pim_category_count_keyword,
            "product_count_total": keyword_globals.get("global_products_total"),
        },
        "rules_by_pim_category": rules_by_pim_category,
    }

    s3_client.put_object(
        Bucket=output_bucket,
        Key=rules_snapshot_key,
        Body=json.dumps(snapshot_body, indent=2),
    )

    outputs_written = run_receipt.setdefault("outputs_written", {})
    outputs_written["rules_snapshot_key"] = rules_snapshot_key

    categories_with_rules = rules_summary.get("categories_with_rules", 0)
    rules_total_by_field_summary = rules_summary.get("rules_total_by_field") or {}

    resolved_rules_total_by_field: Dict[str, int] = {}
    for field_name in ["KEYWORD", "DESCRIPTION_SHORT", "CLASS_CODES"]:
        field_total = rules_total_by_field_summary.get(field_name)
        if field_total is None:
            field_total = 0
            for rules in rules_by_pim_category.values():
                for rule in rules:
                    if rule.get("rule_spec", {}).get("field_name") == field_name:
                        field_total += 1
        resolved_rules_total_by_field[field_name] = field_total

    rules_total_by_field = resolved_rules_total_by_field
    rules_total = sum(rules_total_by_field.values())
    keyword_rules_total = resolved_rules_total_by_field.get("KEYWORD", 0)
    description_rules_total = resolved_rules_total_by_field.get("DESCRIPTION_SHORT", 0)
    class_codes_rules_total = resolved_rules_total_by_field.get("CLASS_CODES", 0)
    resolved_rules_total_by_operator: Dict[str, int] = {}

    operator_totals_summary = rules_summary.get("rules_total_by_operator") if rules_summary else None
    if operator_totals_summary:
        resolved_rules_total_by_operator.update(operator_totals_summary)

    if not resolved_rules_total_by_operator:
        computed_operator_totals: Dict[str, int] = defaultdict(int)
        for rules in rules_by_pim_category.values():
            for rule in rules:
                operator = rule.get("rule_spec", {}).get("operator")
                if operator:
                    computed_operator_totals[operator] += 1
        resolved_rules_total_by_operator = dict(computed_operator_totals)

    contains_any_count = resolved_rules_total_by_operator.get("contains_any")
    if contains_any_count is None:
        contains_any_count = sum(
            1
            for rules in rules_by_pim_category.values()
            for rule in rules
            if rule.get("rule_spec", {}).get("operator") == "contains_any"
        )
        resolved_rules_total_by_operator["contains_any"] = contains_any_count

    contains_all_count = resolved_rules_total_by_operator.get("contains_all")
    if contains_all_count is None:
        contains_all_count = sum(
            1
            for rules in rules_by_pim_category.values()
            for rule in rules
            if rule.get("rule_spec", {}).get("operator") == "contains_all"
        )
        resolved_rules_total_by_operator["contains_all"] = contains_all_count

    rules_counts = run_receipt.setdefault("counts", {}).setdefault("rules_snapshot", {})
    rules_counts.update(
        {
            "rules_total": rules_total,  # consumer: downstream orchestration; purpose: verifies rules exist; interpretation: >=0 count; non-redundant aggregate
            "pim_categories_with_rules": categories_with_rules,  # consumer: debug/ops; purpose: detect empty/over-filtering; interpretation: >=0; non-redundant
            "rules_total_by_field": {
                "KEYWORD": keyword_rules_total,
                "DESCRIPTION_SHORT": description_rules_total,
                "CLASS_CODES": class_codes_rules_total,
            },  # consumer: future multi-field; purpose: field coverage sanity; interpretation: >=0; non-redundant
            "rules_total_by_operator": dict(resolved_rules_total_by_operator),  # consumer: operator coverage; purpose: ensure contains_any present; interpretation: >=0; non-redundant
        }
    )

    return run_receipt


# === Section 6.9: ACTIVE (Write product_rule_hits NDJSON v1) ===


def section6_9_write_product_rule_hits(
    run_receipt: dict,
    rules_by_pim_category: Dict[str, List[dict]],
    field_globals: dict | None = None,
) -> dict:
    vendor_name = run_receipt["vendor_name"]
    run_id = run_receipt["run_id"]
    prepared_output_prefix = run_receipt["prepared_output_prefix"]
    output_bucket = run_receipt["output_bucket"]
    input_bucket = run_receipt["input_bucket"]

    s3_client = boto3.client("s3")

    product_input_key = f"{prepared_output_prefix}/{vendor_name}_forMapping_products"
    product_rule_hits_key = (
        f"{prepared_output_prefix}/mappingMethodTraining/product_rule_hits/"
        f"product_rule_hits_{vendor_name}_{run_id}.ndjson"
    )
    product_multimapping_exceptions_key = (
        f"{prepared_output_prefix}/mappingMethodTraining/product_rule_hits/"
        f"product_multimapping_exceptions_{vendor_name}_{run_id}.ndjson"
    )

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    stable_training_set_key = run_receipt["stable_training_set_key"]
    stable_training_set = load_json_from_s3(input_bucket, stable_training_set_key)

    stopwords_for_filtering = build_stopword_set()
    plural_map_keyword, plural_map_description, _ = build_plural_maps_from_training_set(
        stable_training_set, stopwords_for_filtering
    )
    denylist_config = load_denylist_config(
        s3_client, input_bucket, DENYLIST_CONFIG_KEY_DEFAULT
    )
    print(
        "Loaded denylist config for product rule hits from "
        f"s3://{input_bucket}/{DENYLIST_CONFIG_KEY_DEFAULT}"
    )

    def load_products_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        for raw_line in response["Body"].iter_lines():
            if raw_line is None:
                continue
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
            yield json.loads(line)

    def build_product_tokens(product: dict) -> Dict[str, Set[str]]:
        tokens = build_token_set_for_product(product, stopwords=stopwords_for_filtering)
        tokens["KEYWORD"] = {plural_map_keyword.get(token, token) for token in tokens["KEYWORD"]}
        tokens["DESCRIPTION_SHORT"] = {
            plural_map_description.get(token, token) for token in tokens["DESCRIPTION_SHORT"]
        }
        return tokens

    flattened_rules: List[tuple[str, dict]] = []
    for pim_category_id, rules in rules_by_pim_category.items():
        if not isinstance(rules, list):
            continue
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            flattened_rules.append((str(pim_category_id), rule))

    buffer = io.BytesIO()
    exceptions_buffer = io.BytesIO()
    product_count_total = 0
    products_with_any_rule_hit = 0
    products_included_single_mapping = 0
    products_excluded_multi_mapping = 0
    denylist_removed_counts = {"KEYWORD": 0, "DESCRIPTION_SHORT": 0}

    for product in load_products_from_s3(output_bucket, product_input_key):
        if not isinstance(product, dict):
            continue

        product_count_total += 1
        article_id = product.get("article_id")
        vendor_mappings = product.get("vendor_mappings")

        vendor_mapping_list = vendor_mappings if isinstance(vendor_mappings, list) else []
        vendor_mapping_count = len(vendor_mapping_list)

        if vendor_mapping_count != 1:
            products_excluded_multi_mapping += 1
            vendor_categories = []
            for mapping in vendor_mapping_list:
                if not isinstance(mapping, dict):
                    continue
                vendor_categories.append(
                    {
                        "vendor_category_id": mapping.get("vendor_category_id"),
                        "vendor_category_name": mapping.get("vendor_category_name"),
                        "vendor_category_path": mapping.get("vendor_category_path"),
                    }
                )

            exception_record = {
                "article_id": article_id,
                "vendor_mapping_count": vendor_mapping_count,
                "vendor_categories": vendor_categories,
            }
            exceptions_buffer.write(json.dumps(exception_record, ensure_ascii=False).encode("utf-8"))
            exceptions_buffer.write(b"\n")
            continue

        products_included_single_mapping += 1
        vendor_mapping = vendor_mapping_list[0] if vendor_mapping_list else {}
        vendor_category = {
            "vendor_category_id": vendor_mapping.get("vendor_category_id"),
            "vendor_category_name": vendor_mapping.get("vendor_category_name"),
            "vendor_category_path": vendor_mapping.get("vendor_category_path"),
        }

        raw_tokens = build_product_tokens(product)
        for field_name in ("KEYWORD", "DESCRIPTION_SHORT"):
            denylist_tokens = denylist_config["global"] | denylist_config["by_field"][field_name]
            if not denylist_tokens:
                continue
            filtered = {token for token in raw_tokens[field_name] if token not in denylist_tokens}
            denylist_removed_counts[field_name] += len(raw_tokens[field_name]) - len(filtered)
            raw_tokens[field_name] = filtered
        product_tokens = raw_tokens

        rule_hits: List[dict] = []
        for target_pim_category_id, rule in flattened_rules:
            rule_spec = rule.get("rule_spec")
            if not isinstance(rule_spec, dict):
                continue
            field_name = rule_spec.get("field_name")
            operator = rule_spec.get("operator")
            values_include_raw = rule_spec.get("values_include", [])
            values_exclude_raw = rule_spec.get("values_exclude", [])

            if not isinstance(field_name, str) or not isinstance(operator, str):
                continue
            if operator not in {"contains_any", "contains_all", "contains_any_exclude_any"}:
                continue

            tokens_in_field = product_tokens.get(field_name, set())
            values_include = [value for value in values_include_raw if isinstance(value, str)]
            values_exclude = [value for value in values_exclude_raw if isinstance(value, str)]

            include_hits = [value for value in values_include if value in tokens_in_field]
            exclude_hits = [value for value in values_exclude if value in tokens_in_field]

            matched = False
            if operator == "contains_any":
                matched = bool(include_hits)
            elif operator == "contains_all":
                matched = all(value in tokens_in_field for value in values_include)
            elif operator == "contains_any_exclude_any":
                matched = bool(include_hits) and not exclude_hits

            if not matched:
                continue

            rule_hits.append(
                {
                    "rule_id": rule.get("rule_id"),
                    "target_pim_category_id": target_pim_category_id,
                    "rule_spec": {
                        "field_name": field_name,
                        "operator": operator,
                        "values_include": values_include,
                        "values_exclude": values_exclude,
                    },
                    "match_evidence": {
                        "include_hits": include_hits,
                        "exclude_hits": exclude_hits,
                    },
                }
            )

        if rule_hits:
            products_with_any_rule_hit += 1

        output_record = {
            "article_id": article_id,
            "vendor_category": vendor_category,
            "rule_hits": rule_hits,
        }

        buffer.write(json.dumps(output_record, ensure_ascii=False).encode("utf-8"))
        buffer.write(b"\n")

    s3_client.put_object(Bucket=output_bucket, Key=product_rule_hits_key, Body=buffer.getvalue())
    s3_client.put_object(
        Bucket=output_bucket, Key=product_multimapping_exceptions_key, Body=exceptions_buffer.getvalue()
    )

    outputs_written = run_receipt.setdefault("outputs_written", {})
    outputs_written["product_rule_hits_key"] = product_rule_hits_key
    outputs_written["product_multimapping_exceptions_key"] = product_multimapping_exceptions_key

    product_rule_hits_counts = run_receipt.setdefault("counts", {}).setdefault(
        "product_rule_hits", {}
    )
    product_rule_hits_counts.update(
        {
            "products_total_read": product_count_total,
            "products_included_single_mapping": products_included_single_mapping,
            "products_excluded_multi_mapping": products_excluded_multi_mapping,
            "products_with_any_rule_hit": products_with_any_rule_hit,
            "denylist_removed_tokens_by_field": denylist_removed_counts,
        }
    )

    return run_receipt


# === Section 7.1: ACTIVE (Write vendor_category_product_rule_hits NDJSON v1) ===


def section7_1_write_vendor_category_product_rule_hits(run_receipt: dict) -> dict:
    vendor_name = run_receipt["vendor_name"]
    run_id = run_receipt["run_id"]
    prepared_output_prefix = run_receipt["prepared_output_prefix"]
    output_bucket = run_receipt["output_bucket"]

    product_rule_hits_key = run_receipt.get("outputs_written", {}).get("product_rule_hits_key")
    if not product_rule_hits_key:
        raise ValueError("product_rule_hits_key missing from run_receipt outputs_written")

    s3_client = boto3.client("s3")

    vendor_category_product_rule_hits_key = (
        f"{prepared_output_prefix}/mappingMethodTraining/vendor_category_product_rule_hits/"
        f"vendor_category_product_rule_hits_{vendor_name}_{run_id}.ndjson"
    )

    def iter_product_rule_hits(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        for raw_line in response["Body"].iter_lines():
            if raw_line is None:
                continue
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
            yield json.loads(line)

    vendor_category_records: Dict[str, dict] = {}
    product_count_total = 0

    for record in iter_product_rule_hits(output_bucket, product_rule_hits_key):
        if not isinstance(record, dict):
            raise ValueError("Each product_rule_hits record must be a JSON object")

        vendor_category = record.get("vendor_category")
        if not isinstance(vendor_category, dict):
            raise ValueError("product_rule_hits record missing vendor_category object")
        vendor_category_id = vendor_category.get("vendor_category_id")
        if vendor_category_id is None:
            raise ValueError("product_rule_hits record missing vendor_category.vendor_category_id")

        article_id = record.get("article_id")
        if article_id is None:
            raise ValueError("product_rule_hits record missing article_id")

        vendor_category_compact = {
            "vendor_category_id": vendor_category.get("vendor_category_id"),
            "vendor_category_name": vendor_category.get("vendor_category_name"),
            "vendor_category_path": vendor_category.get("vendor_category_path"),
        }

        vendor_category_key = str(vendor_category_id)
        vendor_entry = vendor_category_records.get(vendor_category_key)
        if vendor_entry is None:
            vendor_entry = {"vendor_category": vendor_category_compact, "products": []}
            vendor_category_records[vendor_category_key] = vendor_entry

        rule_hits_raw = record.get("rule_hits")
        rule_hits_list = rule_hits_raw if isinstance(rule_hits_raw, list) else []
        transformed_rule_hits = []
        for rule_hit in rule_hits_list:
            if not isinstance(rule_hit, dict):
                continue
            transformed_rule_hits.append(
                {
                    "rule_id": rule_hit.get("rule_id"),
                    "pim_target": rule_hit.get("target_pim_category_id"),
                }
            )

        vendor_entry["products"].append(
            {
                "article_id": article_id,
                "rule_hits": transformed_rule_hits,
            }
        )
        product_count_total += 1

    buffer = io.BytesIO()
    for vendor_entry in vendor_category_records.values():
        buffer.write(json.dumps(vendor_entry, ensure_ascii=False).encode("utf-8"))
        buffer.write(b"\n")

    s3_client.put_object(
        Bucket=output_bucket,
        Key=vendor_category_product_rule_hits_key,
        Body=buffer.getvalue(),
    )

    outputs_written = run_receipt.setdefault("outputs_written", {})
    outputs_written["vendor_category_product_rule_hits_key"] = vendor_category_product_rule_hits_key

    vendor_category_product_rule_hits_counts = run_receipt.setdefault("counts", {}).setdefault(
        "vendor_category_product_rule_hits", {}
    )
    vendor_category_product_rule_hits_counts.update(
        {
            "vendor_category_count": len(vendor_category_records),
            "product_count_total": product_count_total,
        }
    )

    return run_receipt


# === Section 7.2: ACTIVE (Write rule_validation_status NDJSON v1) ===


def section7_2_write_rule_validation_status(run_receipt: dict) -> dict:
    vendor_name = run_receipt["vendor_name"]
    run_id = run_receipt["run_id"]
    prepared_output_prefix = run_receipt["prepared_output_prefix"]
    output_bucket = run_receipt["output_bucket"]

    outputs_written = run_receipt.get("outputs_written", {})
    product_rule_hits_key = outputs_written.get("product_rule_hits_key")
    vendor_category_product_rule_hits_key = outputs_written.get("vendor_category_product_rule_hits_key")
    rules_snapshot_key = outputs_written.get("rules_snapshot_key")

    if not product_rule_hits_key:
        raise ValueError("product_rule_hits_key missing from run_receipt outputs_written")
    if not vendor_category_product_rule_hits_key:
        raise ValueError("vendor_category_product_rule_hits_key missing from run_receipt outputs_written")
    if not rules_snapshot_key:
        raise ValueError("rules_snapshot_key missing from run_receipt outputs_written")

    s3_client = boto3.client("s3")

    rule_validation_status_key = (
        f"{prepared_output_prefix}/mappingMethodTraining/rule_validation_status/"
        f"rule_validation_status_{vendor_name}_{run_id}.ndjson"
    )

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    def iter_ndjson(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        for raw_line in response["Body"].iter_lines():
            if raw_line is None:
                continue
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
            yield json.loads(line)

    run_notes = run_receipt.setdefault("notes", [])
    note_set = set(run_notes)

    def add_note_once(message: str):
        if message not in note_set:
            run_notes.append(message)
            note_set.add(message)

    vendor_category_products_total: Dict[str, int | None] = {}
    for record in iter_ndjson(output_bucket, vendor_category_product_rule_hits_key):
        vendor_category = record.get("vendor_category", {})
        vendor_category_id_raw = vendor_category.get("vendor_category_id")
        vendor_category_key = str(vendor_category_id_raw)
        products_list = record.get("products")
        products_total = len(products_list) if isinstance(products_list, list) else None
        vendor_category_products_total[vendor_category_key] = products_total

    rules_snapshot = load_json_from_s3(output_bucket, rules_snapshot_key)
    rules_by_pim_category = rules_snapshot.get("rules_by_pim_category")
    if not isinstance(rules_by_pim_category, dict):
        raise ValueError("rules_snapshot.rules_by_pim_category must be a dict")

    rules_from_snapshot: Dict[str, dict] = {}
    for pim_category_id, rules in rules_by_pim_category.items():
        if not isinstance(rules, list):
            continue
        pim_category_key = str(pim_category_id)
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            rule_id = rule.get("rule_id")
            if rule_id is None:
                continue
            rule_spec = rule.get("rule_spec")
            if rule_spec is None:
                add_note_once(f"Rule {rule_id} missing rule_spec in snapshot; skipping rule_spec in output")
            if rule_id in rules_from_snapshot:
                add_note_once(f"Duplicate rule_id {rule_id} in rules_snapshot; first occurrence retained")
                continue
            rules_from_snapshot[rule_id] = {
                "target_pim_category_id": pim_category_key,
                "rule_spec": rule_spec,
            }

    matched_articles_by_rule: Dict[str, Set[str]] = defaultdict(set)
    matched_articles_by_rule_and_vendor: Dict[str, Dict[str, Set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    vendor_categories_by_rule: Dict[str, Set[str]] = defaultdict(set)
    vendor_category_metadata_by_id: Dict[str, dict] = {}
    fallback_rule_specs: Dict[str, dict] = {}
    vendor_metadata_conflicts: Set[str] = set()

    for record in iter_ndjson(output_bucket, product_rule_hits_key):
        vendor_category = record.get("vendor_category")
        if not isinstance(vendor_category, dict):
            raise ValueError("product_rule_hits record missing vendor_category object")
        vendor_category_id_raw = vendor_category.get("vendor_category_id")
        if vendor_category_id_raw is None:
            raise ValueError("product_rule_hits record missing vendor_category.vendor_category_id")

        vendor_category_compact = {
            "vendor_category_id": vendor_category.get("vendor_category_id"),
            "vendor_category_name": vendor_category.get("vendor_category_name"),
            "vendor_category_path": vendor_category.get("vendor_category_path"),
        }
        vendor_category_key = str(vendor_category_id_raw)
        existing_vendor_meta = vendor_category_metadata_by_id.get(vendor_category_key)
        if existing_vendor_meta is None:
            vendor_category_metadata_by_id[vendor_category_key] = vendor_category_compact
        elif existing_vendor_meta != vendor_category_compact and vendor_category_key not in vendor_metadata_conflicts:
            add_note_once(
                f"Vendor category metadata conflict for id {vendor_category_key} across product_rule_hits"
            )
            vendor_metadata_conflicts.add(vendor_category_key)

        article_id = record.get("article_id")
        rule_hits_raw = record.get("rule_hits")
        rule_hits_list = rule_hits_raw if isinstance(rule_hits_raw, list) else []

        for rule_hit in rule_hits_list:
            if not isinstance(rule_hit, dict):
                continue
            rule_id = rule_hit.get("rule_id")
            if rule_id is None:
                continue

            matched_articles_by_rule[rule_id].add(article_id)
            matched_articles_by_rule_and_vendor[rule_id][vendor_category_key].add(article_id)
            vendor_categories_by_rule[rule_id].add(vendor_category_key)

            if rule_id not in rules_from_snapshot and rule_id not in fallback_rule_specs:
                fallback_rule_specs[rule_id] = {
                    "target_pim_category_id": rule_hit.get("target_pim_category_id"),
                    "rule_spec": rule_hit.get("rule_spec"),
                }
                add_note_once(
                    f"Rule {rule_id} not found in rules_snapshot; using rule_spec from product_rule_hits"
                )

    all_rule_ids = set(rules_from_snapshot.keys()) | set(matched_articles_by_rule.keys()) | set(
        fallback_rule_specs.keys()
    )

    status_counts = {"supported": 0, "violated": 0, "not_applicable": 0}
    buffer = io.BytesIO()

    for rule_id in sorted(all_rule_ids):
        rule_source = rules_from_snapshot.get(rule_id) or fallback_rule_specs.get(rule_id) or {}
        target_pim_category_id = rule_source.get("target_pim_category_id")
        rule_spec = rule_source.get("rule_spec")

        vendor_categories_hit = vendor_categories_by_rule.get(rule_id, set())
        total_matched_products = len(matched_articles_by_rule.get(rule_id, set()))

        if not vendor_categories_hit:
            rule_status = "not_applicable"
        elif len(vendor_categories_hit) == 1:
            rule_status = "supported"
        else:
            rule_status = "violated"

        status_counts[rule_status] += 1

        matched_vendor_categories_list = []
        for vendor_category_key in vendor_categories_hit:
            matched_products_in_category = len(
                matched_articles_by_rule_and_vendor.get(rule_id, {}).get(vendor_category_key, set())
            )
            products_in_category = vendor_category_products_total.get(vendor_category_key)
            if products_in_category is None:
                add_note_once(
                    f"products_in_category missing for vendor_category_id {vendor_category_key} when writing rule_validation_status"
                )
            coverage = (
                matched_products_in_category / products_in_category
                if products_in_category and products_in_category > 0
                else None
            )
            matched_products_outside_of_category = total_matched_products - matched_products_in_category
            threshold_eval_result = evaluate_threshold(
                products_in_category,
                matched_products_in_category,
                THRESHOLD_POLICY,
            )
            run_outside_categories_with_support_count = max(len(vendor_categories_hit) - 1, 0)
            matched_vendor_categories_list.append(
                {
                    "vendor_category": vendor_category_metadata_by_id.get(vendor_category_key, {}),
                    "products_in_category": products_in_category,
                    "matched_products_in_category": matched_products_in_category,
                    "coverage": coverage,
                    "matched_products_outside_of_category": matched_products_outside_of_category,
                    "run_proof": {
                        "run_inside_products_total": products_in_category,
                        "run_inside_support_count": matched_products_in_category,
                        "run_inside_support_ratio": coverage,
                        "run_outside_support_count": matched_products_outside_of_category,
                        "run_outside_categories_with_support_count": run_outside_categories_with_support_count,
                        "run_uniqueness_basis": "distinct_vendor_categories_fired_count==1",
                    },
                    "threshold_eval": {
                        "pass_threshold": threshold_eval_result["pass_threshold"],
                        "support_ratio": threshold_eval_result["support_ratio"],
                        "policy": THRESHOLD_POLICY,
                    },
                }
            )

        matched_vendor_categories_sorted = sorted(
            matched_vendor_categories_list,
            key=lambda entry: entry.get("matched_products_in_category", 0),
            reverse=True,
        )

        output_record = {
            "rule": {
                "rule_id": rule_id,
                "target_pim_category_id": target_pim_category_id,
                "rule_spec": rule_spec,
                "rule_status": rule_status,
            },
            "matched_vendor_categories": matched_vendor_categories_sorted,
        }

        buffer.write(json.dumps(output_record, ensure_ascii=False).encode("utf-8"))
        buffer.write(b"\n")

    s3_client.put_object(Bucket=output_bucket, Key=rule_validation_status_key, Body=buffer.getvalue())

    outputs_written["rule_validation_status_key"] = rule_validation_status_key

    counts = run_receipt.setdefault("counts", {})
    counts["rule_validation_status_total_rules"] = len(all_rule_ids)
    counts["rule_validation_status_supported_rules"] = status_counts["supported"]
    counts["rule_validation_status_violated_rules"] = status_counts["violated"]
    counts["rule_validation_status_not_applicable_rules"] = status_counts["not_applicable"]

    return run_receipt


# === Section 7.3: ACTIVE (Write vendor_category_mapping_status JSON) ===


def section7_3_write_vendor_category_mapping_status(run_receipt: dict) -> dict:
    vendor_name = run_receipt["vendor_name"]
    run_id = run_receipt["run_id"]
    prepared_output_prefix = run_receipt["prepared_output_prefix"]
    output_bucket = run_receipt["output_bucket"]
    input_bucket = run_receipt["input_bucket"]

    outputs_written = run_receipt.get("outputs_written", {})
    vendor_category_product_rule_hits_key = outputs_written.get("vendor_category_product_rule_hits_key")
    rule_validation_status_key = outputs_written.get("rule_validation_status_key")

    if not vendor_category_product_rule_hits_key:
        raise ValueError("vendor_category_product_rule_hits_key missing from run_receipt outputs_written")
    if not rule_validation_status_key:
        raise ValueError("rule_validation_status_key missing from run_receipt outputs_written")

    s3_client = boto3.client("s3")

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    def iter_ndjson(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        for raw_line in response["Body"].iter_lines():
            if raw_line is None:
                continue
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
            yield json.loads(line)

    def build_pim_category_name_map() -> Dict[str, str]:
        pim_category_names: Dict[str, str] = {}

        def update_from_step2(data):
            if not isinstance(data, dict):
                return
            for vendor_category_data in data.values():
                pim_matches = vendor_category_data.get("pim_matches") or []
                if not isinstance(pim_matches, list):
                    continue
                for pim_match in pim_matches:
                    if not isinstance(pim_match, dict):
                        continue
                    pim_category_id = pim_match.get("pim_category_id")
                    pim_category_name = pim_match.get("pim_category_name")
                    if pim_category_id is None or pim_category_name is None:
                        continue
                    key = str(pim_category_id)
                    pim_category_names.setdefault(key, pim_category_name)

        step2_full = load_json_from_s3(input_bucket, run_receipt["step2_full_key"])
        update_from_step2(step2_full)

        step2_1to1 = load_json_from_s3(input_bucket, run_receipt["step2_1to1_key"])
        update_from_step2(step2_1to1)

        return pim_category_names

    vendor_category_meta: Dict[str, dict] = {}
    pim_category_name_map = build_pim_category_name_map()
    for record in iter_ndjson(output_bucket, vendor_category_product_rule_hits_key):
        vendor_category = record.get("vendor_category", {})
        vendor_category_id = vendor_category.get("vendor_category_id")
        if vendor_category_id is None:
            continue
        products = record.get("products") or []
        vendor_category_meta[str(vendor_category_id)] = {
            "vendor_category": {
                "vendor_category_id": vendor_category.get("vendor_category_id"),
                "vendor_category_name": vendor_category.get("vendor_category_name"),
                "vendor_category_path": vendor_category.get("vendor_category_path"),
            },
            "products_in_category": len(products) if isinstance(products, list) else None,
        }

    vendor_category_rules: Dict[str, List[dict]] = defaultdict(list)

    for record in iter_ndjson(output_bucket, rule_validation_status_key):
        rule_info = record.get("rule", {})
        rule_id = rule_info.get("rule_id")
        target_pim_category_id = rule_info.get("target_pim_category_id")
        rule_spec = rule_info.get("rule_spec")
        rule_status = rule_info.get("rule_status")
        matched_vendor_categories = record.get("matched_vendor_categories") or []

        for vendor_entry in matched_vendor_categories:
            vendor_category = vendor_entry.get("vendor_category", {})
            vendor_category_id = vendor_category.get("vendor_category_id")
            if vendor_category_id is None:
                continue
            vendor_category_key = str(vendor_category_id)

            meta_entry = vendor_category_meta.setdefault(
                vendor_category_key,
                {
                    "vendor_category": {
                        "vendor_category_id": vendor_category.get("vendor_category_id"),
                        "vendor_category_name": vendor_category.get("vendor_category_name"),
                        "vendor_category_path": vendor_category.get("vendor_category_path"),
                    },
                    "products_in_category": vendor_entry.get("products_in_category"),
                },
            )
            if meta_entry.get("products_in_category") is None:
                meta_entry["products_in_category"] = vendor_entry.get("products_in_category")

            products_in_category = meta_entry.get("products_in_category")
            matched_products_in_category = vendor_entry.get("matched_products_in_category")
            coverage = vendor_entry.get("coverage")
            threshold_eval = vendor_entry.get("threshold_eval") or evaluate_threshold(
                products_in_category,
                matched_products_in_category,
                THRESHOLD_POLICY,
            )
            run_proof = vendor_entry.get("run_proof") or {
                "run_inside_products_total": products_in_category,
                "run_inside_support_count": matched_products_in_category,
                "run_inside_support_ratio": coverage,
                "run_outside_support_count": vendor_entry.get("matched_products_outside_of_category"),
                "run_outside_categories_with_support_count": None,
                "run_uniqueness_basis": "distinct_vendor_categories_fired_count==1",
            }
            run_inside_support_ratio = run_proof.get("run_inside_support_ratio", coverage)
            if run_inside_support_ratio is None:
                run_inside_support_ratio = threshold_eval.get("support_ratio") if isinstance(threshold_eval, dict) else None

            vendor_category_rules[vendor_category_key].append(
                {
                    "rule_id": rule_id,
                    "target_pim_category_id": target_pim_category_id,
                    "rule_spec": rule_spec,
                    "rule_status": rule_status,
                    "run_inside_support_count": matched_products_in_category,
                    "run_inside_support_ratio": run_inside_support_ratio,
                    "pass_threshold": bool(threshold_eval.get("pass_threshold") if isinstance(threshold_eval, dict) else False),
                }
            )

    all_vendor_category_ids = set(vendor_category_meta.keys()) | set(vendor_category_rules.keys())
    vendor_categories_output: List[dict] = []

    status_counts = {
        "unambiguous": 0,
        "conflicting": 0,
        "insufficient": 0,
        "no_rule_hits": 0,
    }

    for vendor_category_id in sorted(all_vendor_category_ids):
        meta_entry = vendor_category_meta.get(vendor_category_id) or {
            "vendor_category": {
                "vendor_category_id": vendor_category_id,
                "vendor_category_name": None,
                "vendor_category_path": None,
            },
            "products_in_category": None,
        }
        products_in_category = meta_entry.get("products_in_category")
        rules_for_category = vendor_category_rules.get(vendor_category_id, [])

        rules_fired_total = len(rules_for_category)
        supported_rules = [rule for rule in rules_for_category if rule.get("rule_status") == "supported"]
        violated_rules_fired_total = sum(
            1 for rule in rules_for_category if rule.get("rule_status") == "violated"
        )

        eligible_rules = [
            rule for rule in supported_rules if rule.get("pass_threshold")
        ]

        eligible_targets = {rule.get("target_pim_category_id") for rule in eligible_rules if rule.get("target_pim_category_id") is not None}

        if rules_fired_total == 0:
            mapping_status = "no_rule_hits"
            unambiguous_target = None
        elif not eligible_rules:
            mapping_status = "insufficient"
            unambiguous_target = None
        elif len(eligible_targets) == 1:
            mapping_status = "unambiguous"
            unambiguous_target = next(iter(eligible_targets))
        else:
            mapping_status = "conflicting"
            unambiguous_target = None

        status_counts[mapping_status] += 1
        unambiguous_target_pim_category_name = (
            pim_category_name_map.get(str(unambiguous_target)) if unambiguous_target is not None else None
        )

        supporting_rules = [
            {
                "rule_id": rule.get("rule_id"),
                "target_pim_category_id": rule.get("target_pim_category_id"),
                "rule_spec": rule.get("rule_spec"),
                "run_inside_support_count": rule.get("run_inside_support_count"),
                "run_inside_support_ratio": rule.get("run_inside_support_ratio"),
                "pass_threshold": rule.get("pass_threshold"),
            }
            for rule in eligible_rules
        ]

        vendor_categories_output.append(
            {
                "vendor_category": meta_entry.get("vendor_category", {}),
                "products_in_category": products_in_category,
                "mapping_status": mapping_status,
                "unambiguous_target_pim_category_id": unambiguous_target,
                "pim_category_name": unambiguous_target_pim_category_name,
                "supporting_rules_count": len(eligible_rules),
                "supporting_rules": supporting_rules,
                "all_rules_summary": {
                    "rules_fired_total": rules_fired_total,
                    "supported_rules_fired_total": len(supported_rules),
                    "supported_rules_passing_threshold_total": len(eligible_rules),
                    "violated_rules_fired_total": violated_rules_fired_total,
                },
            }
        )

    vendor_category_mapping_status_body = {
        "vendor_name": vendor_name,
        "run_id": run_id,
        "threshold_policy": THRESHOLD_POLICY,
        "vendor_categories": vendor_categories_output,
    }

    vendor_category_mapping_status_key = (
        f"{prepared_output_prefix}/mappingMethodTraining/vendor_category_mapping_status/"
        f"vendor_category_mapping_status_{vendor_name}_{run_id}.json"
    )

    s3_client.put_object(
        Bucket=output_bucket,
        Key=vendor_category_mapping_status_key,
        Body=json.dumps(vendor_category_mapping_status_body, indent=2),
    )

    outputs_written["vendor_category_mapping_status_key"] = vendor_category_mapping_status_key

    counts = run_receipt.setdefault("counts", {})
    counts["vendor_category_mapping_status"] = {
        "categories_total": len(vendor_categories_output),
        "unambiguous_count": status_counts["unambiguous"],
        "conflicting_count": status_counts["conflicting"],
        "insufficient_count": status_counts["insufficient"],
        "no_rule_hits_count": status_counts["no_rule_hits"],
    }

    return run_receipt


# === Section 8: ACTIVE (Update Category_Mapping_Reference from rule_validation_status) ===


def section8_update_category_mapping_reference(run_receipt: dict) -> dict:
    vendor_name = run_receipt["vendor_name"]
    run_id = run_receipt["run_id"]
    input_bucket = run_receipt["input_bucket"]
    output_bucket = run_receipt["output_bucket"]
    category_mapping_reference_key = run_receipt["category_mapping_reference_key_selected"]

    outputs_written = run_receipt.get("outputs_written", {})
    rule_validation_status_key = outputs_written.get("rule_validation_status_key")
    if not rule_validation_status_key:
        raise ValueError("rule_validation_status_key missing from run_receipt outputs_written")

    s3_client = boto3.client("s3")
    denylist_config = load_denylist_config(
        s3_client, input_bucket, DENYLIST_CONFIG_KEY_DEFAULT
    )
    print(
        "Loaded denylist config for reference update from "
        f"s3://{input_bucket}/{DENYLIST_CONFIG_KEY_DEFAULT}"
    )
    print(
        "Denylist debug (reference update): "
        f"global_count={len(denylist_config.get('global', []))} "
        f"wpb_in_global={'wpb' in denylist_config.get('global', set())}"
    )

    def load_json_from_s3(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)

    def iter_ndjson(bucket: str, key: str):
        response = s3_client.get_object(Bucket=bucket, Key=key)
        for raw_line in response["Body"].iter_lines():
            if raw_line is None:
                continue
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
            yield json.loads(line)

    reference_entries_raw = load_json_from_s3(input_bucket, category_mapping_reference_key)
    if isinstance(reference_entries_raw, dict):
        reference_entries: List[dict] = list(reference_entries_raw.values())
    elif isinstance(reference_entries_raw, list):
        reference_entries = reference_entries_raw
    else:
        raise ValueError("Category_Mapping_Reference must be a list or dict of entries")

    ref_by_pim_id: Dict[str, dict] = {}
    original_vendor_mappings_by_pim: Dict[str, str] = {}
    for entry in reference_entries:
        if not isinstance(entry, dict):
            raise ValueError("Category_Mapping_Reference entries must be JSON objects")
        pim_category_id = entry.get("pim_category_id")
        if pim_category_id is None:
            raise ValueError("Category_Mapping_Reference entry missing pim_category_id")
        pim_category_key = str(pim_category_id)
        ref_by_pim_id[pim_category_key] = entry
        original_vendor_mappings_by_pim[pim_category_key] = json.dumps(
            deepcopy(entry.get("vendor_mappings")), sort_keys=True, ensure_ascii=False
        )

    next_methods_by_pim: Dict[str, List[dict]] = defaultdict(list)
    method_signatures_by_pim: Dict[str, Set[Tuple[str, str, Tuple[str, ...], Tuple[str, ...]]]] = defaultdict(set)

    rules_total = 0
    rules_violated_excluded = 0
    rules_supported_total = 0
    rules_supported_clean_included = 0
    rules_supported_unclean_dropped = 0
    rules_not_applicable_included = 0
    rules_denylisted_dropped = 0

    for record in iter_ndjson(output_bucket, rule_validation_status_key):
        if not isinstance(record, dict):
            raise ValueError("rule_validation_status record must be a JSON object")
        rule = record.get("rule") or {}
        matched_vendor_categories = record.get("matched_vendor_categories") or []

        rule_status = rule.get("rule_status")
        pim_category_id = rule.get("target_pim_category_id")
        rule_spec = rule.get("rule_spec")

        if pim_category_id is None:
            raise ValueError("rule_validation_status record missing target_pim_category_id")
        pim_category_key = str(pim_category_id)

        rules_total += 1

        if rule_status not in {"supported", "violated", "not_applicable"}:
            raise RuntimeError(f"Unknown rule_status '{rule_status}' in rule_validation_status")

        if rule_status == "violated":
            rules_violated_excluded += 1
            continue

        if not isinstance(rule_spec, dict):
            raise ValueError("rule_validation_status record missing or invalid rule_spec")

        field_name = rule_spec.get("field_name")
        operator = rule_spec.get("operator")
        values_include_raw = rule_spec.get("values_include") or []
        values_exclude_raw = rule_spec.get("values_exclude") or []
        if not isinstance(values_include_raw, list) or not isinstance(values_exclude_raw, list):
            raise ValueError("rule_spec values_include and values_exclude must be lists")

        values_include = sorted(values_include_raw)
        values_exclude = sorted(values_exclude_raw)

        denylist_tokens = denylist_config.get("global", set()) | denylist_config.get(
            "by_field", {}
        ).get(field_name, set())
        if denylist_tokens:
            include_denylisted = any(
                is_denylisted_token(value, field_name, denylist_config)
                for value in values_include
                if isinstance(value, str)
            )
            exclude_denylisted = any(
                is_denylisted_token(value, field_name, denylist_config)
                for value in values_exclude
                if isinstance(value, str)
            )
            if include_denylisted or exclude_denylisted:
                rules_denylisted_dropped += 1
                continue

        is_clean_supported = False
        if rule_status == "supported":
            rules_supported_total += 1
            for vendor_entry in matched_vendor_categories:
                threshold_eval = vendor_entry.get("threshold_eval") or {}
                if threshold_eval.get("pass_threshold") is True:
                    is_clean_supported = True
                    break
            if not is_clean_supported:
                rules_supported_unclean_dropped += 1
                continue
            rules_supported_clean_included += 1
        else:
            rules_not_applicable_included += 1

        method_signature = (field_name, operator, tuple(values_include), tuple(values_exclude))
        if method_signature in method_signatures_by_pim[pim_category_key]:
            continue

        method_signatures_by_pim[pim_category_key].add(method_signature)
        next_methods_by_pim[pim_category_key].append(
            {
                "field_name": field_name,
                "operator": operator,
                "values_include": values_include,
                "values_exclude": values_exclude,
            }
        )

    missing_pim_ids = sorted(set(next_methods_by_pim.keys()) - set(ref_by_pim_id.keys()))
    if missing_pim_ids:
        missing_preview = ", ".join(missing_pim_ids[:10])
        raise RuntimeError(
            f"rule_validation_status references PIM categories not present in reference: {missing_preview}"
        )

    def mapping_method_sort_key(method: dict) -> Tuple[str, str, str, str]:
        return (
            method.get("field_name") or "",
            method.get("operator") or "",
            ",".join(method.get("values_include", [])),
            ",".join(method.get("values_exclude", [])),
        )

    for entry in reference_entries:
        pim_category_key = str(entry.get("pim_category_id"))
        mapping_methods = next_methods_by_pim.get(pim_category_key, [])
        entry["mapping_methods"] = sorted(mapping_methods, key=mapping_method_sort_key)

    for entry in reference_entries:
        pim_category_key = str(entry.get("pim_category_id"))
        original_vendor_mappings_json = original_vendor_mappings_by_pim.get(pim_category_key)
        if original_vendor_mappings_json is None:
            continue
        current_vendor_mappings_json = json.dumps(
            deepcopy(entry.get("vendor_mappings")), sort_keys=True, ensure_ascii=False
        )
        if current_vendor_mappings_json != original_vendor_mappings_json:
            print(
                "Vendor mappings changed during reference update; "
                f"pim_category_id={pim_category_key} "
                f"original_length={len(original_vendor_mappings_json)} "
                f"current_length={len(current_vendor_mappings_json)} "
                f"original_preview={original_vendor_mappings_json[:500]} "
                f"current_preview={current_vendor_mappings_json[:500]}"
            )
            raise RuntimeError(
                f"Vendor mappings were modified for pim_category_id {pim_category_key}; aborting write"
            )

    new_suffix = run_id.replace("-", "")
    new_reference_key = f"canonical_mappings/Category_Mapping_Reference_{new_suffix}.json"

    reference_body = json.dumps(reference_entries, indent=2, ensure_ascii=False)
    s3_client.put_object(Bucket=input_bucket, Key=new_reference_key, Body=reference_body)

    outputs_written["category_mapping_reference_key_written"] = new_reference_key

    run_receipt["reference_update"] = {
        "reference_input_key": category_mapping_reference_key,
        "reference_output_key": new_reference_key,
        "rule_validation_status_key": rule_validation_status_key,
        "full_coverage_assumed": True,
        "promotion_policy": "supported_and_pass_threshold_only",
        "violated_policy": "remove",
        "not_applicable_policy": "retain_in_rulebase",
        "counts": {
            "rules_total": rules_total,
            "rules_supported_total": rules_supported_total,
            "rules_supported_clean_included": rules_supported_clean_included,
            "rules_supported_unclean_dropped": rules_supported_unclean_dropped,
            "rules_violated_excluded": rules_violated_excluded,
            "rules_not_applicable_included": rules_not_applicable_included,
            "rules_denylisted_dropped": rules_denylisted_dropped,
        },
    }

    return run_receipt


if __name__ == "__main__":
    main()
