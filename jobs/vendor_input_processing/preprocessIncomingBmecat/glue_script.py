import sys
import os
import json
import traceback
import boto3
import xml.etree.ElementTree as ET

from awsglue.utils import getResolvedOptions

# ---------- Glue arguments ----------

REQUIRED_ARGS = [
    "JOB_NAME",
    # "JOB_RUN_ID",  # removed to avoid argparse conflict – Glue already defines it
    "INPUT_BUCKET",
    "OUTPUT_BUCKET",
    "vendor_name",
    "bmecat_input_key",
    "bmecat_output_prefix",
]

args = getResolvedOptions(sys.argv, REQUIRED_ARGS)

JOB_NAME = args["JOB_NAME"]
# Read JOB_RUN_ID from environment; Glue injects it, but we do NOT parse it via getResolvedOptions
JOB_RUN_ID = os.environ.get("JOB_RUN_ID", "UNKNOWN")

INPUT_BUCKET = args["INPUT_BUCKET"]
OUTPUT_BUCKET = args["OUTPUT_BUCKET"]

VENDOR_NAME = args["vendor_name"]
BMECAT_INPUT_KEY = args["bmecat_input_key"].lstrip("/")
BMECAT_OUTPUT_PREFIX = args["bmecat_output_prefix"].lstrip("/")

if BMECAT_OUTPUT_PREFIX and not BMECAT_OUTPUT_PREFIX.endswith("/"):
    BMECAT_OUTPUT_PREFIX = BMECAT_OUTPUT_PREFIX + "/"

print(f"[INFO] JOB_NAME={JOB_NAME}, JOB_RUN_ID={JOB_RUN_ID}")
print(f"[INFO] INPUT_BUCKET={INPUT_BUCKET}, OUTPUT_BUCKET={OUTPUT_BUCKET}")
print(f"[INFO] VENDOR_NAME={VENDOR_NAME}")
print(f"[INFO] BMECAT_INPUT_KEY={BMECAT_INPUT_KEY}")
print(f"[INFO] BMECAT_OUTPUT_PREFIX={BMECAT_OUTPUT_PREFIX}")

s3 = boto3.client("s3")

# ---------- Helpers ----------


def read_text_from_s3(bucket: str, key: str) -> str:
    print(f"[INFO] Reading from s3://{bucket}/{key}")
    resp = s3.get_object(Bucket=bucket, Key=key)
    return resp["Body"].read().decode("utf-8")


def write_ndjson_to_s3(bucket: str, key: str, records) -> None:
    """
    Write a list of dicts as newline-delimited JSON to a single S3 object.
    """
    print(f"[INFO] Writing {len(records)} records to s3://{bucket}/{key}")
    body_lines = []
    for rec in records:
        body_lines.append(json.dumps(rec, ensure_ascii=False))
    body_bytes = ("\n".join(body_lines)).encode("utf-8")
    s3.put_object(Bucket=bucket, Key=key, Body=body_bytes)


def findall_path(root: ET.Element, path: str):
    """
    Simple path resolver for 'A/B/C' style paths.
    Special handling: if the first segment equals root.tag, we skip it.
    """
    parts = [p for p in path.split("/") if p]
    if not parts:
        return []

    idx = 0
    if root.tag == parts[0]:
        idx = 1

    elems = [root]
    for p in parts[idx:]:
        next_elems = []
        for e in elems:
            next_elems.extend(e.findall(p))
        elems = next_elems
    return elems


def findall_rel(elem: ET.Element, rel_path: str):
    """
    Like findall_path, but relative to 'elem' (no root.tag special case).
    Returns a list of matching elements for a simple 'A/B/C' style path.
    """
    if not rel_path:
        return []
    parts = [p for p in rel_path.split("/") if p]
    if not parts:
        return []

    elems = [elem]
    for p in parts:
        next_elems = []
        for e in elems:
            next_elems.extend(e.findall(p))
        elems = next_elems
    return elems


def get_text_rel(elem: ET.Element, rel_path: str):
    """
    Resolve a simple relative path from 'elem' like 'A/B'.
    Returns the element text or None if path is missing.
    Does NOT strip whitespace.
    """
    if not rel_path:
        return None

    parts = [p for p in rel_path.split("/") if p]
    cur = elem
    for p in parts:
        child = cur.find(p)
        if child is None:
            return None
        cur = child
    return cur.text


# For tracking missing config paths (for logging once per path)
missing_path_warnings = set()


def get_text_rel_with_warn(elem: ET.Element, rel_path: str, field_label: str):
    """
    Wrapper around get_text_rel that logs a WARNING once per (field_label, path)
    when the path does not exist for the given element.
    """
    if not rel_path:
        return None
    val = get_text_rel(elem, rel_path)
    if val is None:
        key = f"{field_label}::{rel_path}"
        if key not in missing_path_warnings:
            print(
                f"[WARN] Configured path '{rel_path}' for '{field_label}' "
                f"was not found (at least for one record)."
            )
            missing_path_warnings.add(key)
    return val


def strip_namespace(elem: ET.Element):
    """
    Remove default XML namespace from this element and all children, in-place.
    Turns '{uri}TAG' into 'TAG', so config paths like 'BMECAT/T_NEW_CATALOG/ARTICLE'
    work even if the BMECAT XML uses a default namespace.
    """
    if elem.tag.startswith("{"):
        elem.tag = elem.tag.split("}", 1)[1]
    for child in list(elem):
        strip_namespace(child)


# ---------- Load config ----------

config_key = (
    "configuration-files/incomingVendorBmecatPreprocessing_configs/"
    f"incomingVendorBmecatPreprocessing_config_{VENDOR_NAME}.json"
)

print(f"[INFO] Using config file s3://{INPUT_BUCKET}/{config_key}")

try:
    config_text = read_text_from_s3(INPUT_BUCKET, config_key)
    config = json.loads(config_text)
except Exception as e:
    print("[ERROR] Failed to load or parse config JSON.")
    print(str(e))
    traceback.print_exc()
    raise

outputs_cfg = config.get("outputs", {})

vendor_products_cfg = outputs_cfg.get("vendor_products")
product_features_cfg = outputs_cfg.get("product_features")
product_category_links_cfg = outputs_cfg.get("product_category_links")
product_mimes_cfg = outputs_cfg.get("product_mimes")         # optional
product_relations_cfg = outputs_cfg.get("product_relations") # optional
product_prices_cfg = outputs_cfg.get("product_prices")       # optional
vendor_categories_cfg = outputs_cfg.get("vendor_categories") # optional

if not vendor_products_cfg or not product_features_cfg or not product_category_links_cfg:
    print(
        "[ERROR] Config missing one of required outputs: "
        "vendor_products, product_features, product_category_links."
    )
    raise RuntimeError("Incomplete config: missing outputs blocks.")

# ---------- Load and parse BMECAT XML ----------

try:
    bmecat_xml = read_text_from_s3(INPUT_BUCKET, BMECAT_INPUT_KEY)
except Exception as e:
    print("[ERROR] Failed to read BMECAT input file from S3.")
    print(str(e))
    traceback.print_exc()
    raise

try:
    root = ET.fromstring(bmecat_xml)
except Exception as e:
    print("[ERROR] Failed to parse BMECAT XML.")
    print(str(e))
    traceback.print_exc()
    raise

# Strip default namespace so config paths without prefixes work
strip_namespace(root)

# ---------- 1) vendor_products ----------

vp_root_path = vendor_products_cfg["root_path"]
vp_key_fields = vendor_products_cfg["key_fields"]
vp_fields = vendor_products_cfg.get("fields", {})
vp_class_codes_cfg = vendor_products_cfg.get("class_codes", [])
vp_keywords_cfg = vendor_products_cfg.get("keywords", [])

vp_article_nodes = findall_path(root, vp_root_path)

if not vp_article_nodes:
    print(f"[ERROR] No ARTICLE nodes found for root_path='{vp_root_path}'.")
    raise RuntimeError("No ARTICLE nodes found – failing job as agreed.")

print(f"[INFO] Found {len(vp_article_nodes)} ARTICLE nodes for vendor_products.")

vp_records = []
skipped_articles_no_id = 0

for art in vp_article_nodes:
    # --- article_id with fallback ---
    article_id_cfg = vp_key_fields["article_id"]
    primary_path = article_id_cfg.get("primary_path") or article_id_cfg.get("primary")
    fallback_path = article_id_cfg.get("fallback_path") or article_id_cfg.get("fallback")

    article_id = get_text_rel_with_warn(
        art, primary_path, "vendor_products.article_id.primary"
    )
    if not article_id:
        article_id = get_text_rel_with_warn(
            art, fallback_path, "vendor_products.article_id.fallback"
        )

    if not article_id:
        # As per your decision: skip article when no key is available
        skipped_articles_no_id += 1
        continue

    record = {
        "vendor_name": VENDOR_NAME,
        "article_id": str(article_id),
    }

    # --- simple fields ---
    for out_name, rel_path in vp_fields.items():
        val = get_text_rel_with_warn(art, rel_path, f"vendor_products.{out_name}")
        record[out_name] = str(val) if val is not None else None

    # --- keywords (e.g. USER_DEFINED_EXTENSIONS/UDX.NM.SYNONYM) ---
    # Expect config: "keywords": [ { "source": "<relative path from ARTICLE>" }, ... ]
    keywords_out = []
    for kw_rule in vp_keywords_cfg:
        source_path = kw_rule.get("source")
        if not source_path:
            continue
        kw_elems = findall_rel(art, source_path)
        for kw_el in kw_elems:
            if kw_el is None:
                continue
            kw_text = kw_el.text
            if kw_text is not None:
                keywords_out.append(str(kw_text))
    if vp_keywords_cfg:
        record["keywords"] = keywords_out

    # --- class_codes (from ARTICLE_FEATURES) ---
    class_codes_out = []
    for rule in vp_class_codes_cfg:
        source_parent = rule.get("source_parent", "ARTICLE_FEATURES")
        system_field = rule["system_field"]
        code_field = rule["code_field"]
        allowed_systems = rule.get("systems") or []

        for feat_block in art.findall(source_parent):
            system_name = get_text_rel(feat_block, system_field)
            code_val = get_text_rel(feat_block, code_field)

            if not system_name or not code_val:
                continue

            if allowed_systems and system_name not in allowed_systems:
                continue

            class_codes_out.append(
                {
                    "system": str(system_name),
                    "code": str(code_val),
                }
            )

    record["class_codes"] = class_codes_out

    vp_records.append(record)

print(
    f"[INFO] vendor_products: built {len(vp_records)} records; "
    f"skipped {skipped_articles_no_id} articles with no article_id."
)

# ---------- 2) product_features ----------

# Config shape (Fein):
# "product_features": {
#   "entity_name": "product_features",
#   "root_path": "BMECAT/T_NEW_CATALOG/ARTICLE",
#   "source_parent": "ARTICLE_FEATURES",
#   "fields": {
#       "article_id": { "vendor_products.key_fields.article_id": "article_id" },
#       "system_name": "REFERENCE_FEATURE_SYSTEM_NAME",
#       "group_id": "REFERENCE_FEATURE_GROUP_ID",
#       "group_name": "REFERENCE_FEATURE_GROUP_NAME",
#       "fname": "FEATURE/FNAME",
#       "fvalue": "FEATURE/FVALUE",
#       "funit": "FEATURE/FUNIT",
#       "forder": "FEATURE/FORDER"
#   },
#   "options": {
#       "explode_multiple_fvalues": true
#   }
# }

pf_root_path = product_features_cfg["root_path"]
pf_source_parent = product_features_cfg.get("source_parent", "ARTICLE_FEATURES")
pf_fields_cfg = product_features_cfg.get("fields", {})
pf_options = product_features_cfg.get("options", {})
pf_dedup_cfg = product_features_cfg.get("deduplication", {})

# --- derive article_id definition for product_features ---

article_id_primary_path = None
article_id_fallback_path = None

pf_key_fields = product_features_cfg.get("key_fields")
if pf_key_fields and "article_id" in pf_key_fields:
    pf_article_id_cfg = pf_key_fields["article_id"]
    article_id_primary_path = pf_article_id_cfg.get("primary_path") or pf_article_id_cfg.get("primary")
    article_id_fallback_path = pf_article_id_cfg.get("fallback_path") or pf_article_id_cfg.get("fallback")
else:
    article_id_field_cfg = pf_fields_cfg.get("article_id")
    if isinstance(article_id_field_cfg, dict):
        if "vendor_products.key_fields.article_id" in article_id_field_cfg:
            vp_kf = vendor_products_cfg.get("key_fields", {})
            vp_article_cfg = vp_kf.get("article_id")
            if vp_article_cfg:
                article_id_primary_path = vp_article_cfg.get("primary_path") or vp_article_cfg.get("primary")
                article_id_fallback_path = vp_article_cfg.get("fallback_path") or vp_article_cfg.get("fallback")

if not article_id_primary_path and not article_id_fallback_path:
    raise RuntimeError(
        "No article_id definition for product_features: "
        "either provide product_features.key_fields.article_id or "
        "fields.article_id with vendor_products.key_fields.article_id reference."
    )

pf_fields_no_article = {k: v for k, v in pf_fields_cfg.items() if k != "article_id"}

pf_article_nodes = findall_path(root, pf_root_path)
print(f"[INFO] Found {len(pf_article_nodes)} ARTICLE nodes for product_features.")

pf_records = []
dedup_key_cols = pf_dedup_cfg.get("by_columns", ["article_id", "fname", "fvalue"])
seen_pf_keys = set()
explode_multiple_fvalues = bool(pf_options.get("explode_multiple_fvalues", False))

for art in pf_article_nodes:
    # derive article_id
    article_id = None
    if article_id_primary_path:
        article_id = get_text_rel_with_warn(
            art, article_id_primary_path, "product_features.article_id.primary"
        )
    if not article_id and article_id_fallback_path:
        article_id = get_text_rel_with_warn(
            art, article_id_fallback_path, "product_features.article_id.fallback"
        )

    if not article_id:
        continue

    article_id = str(article_id)

    # detect FEATURE tag
    feature_tag = None
    for f_name, path in pf_fields_no_article.items():
        if path and isinstance(path, str) and "/" in path:
            feature_tag = path.split("/", 1)[0]
            break

    for feat_block in art.findall(pf_source_parent):
        # fields directly under ARTICLE_FEATURES
        section_base_values = {}
        for f_name, path in pf_fields_no_article.items():
            if not path or not isinstance(path, str) or "/" in path:
                continue
            val = get_text_rel_with_warn(
                feat_block, path, f"product_features.{f_name}"
            )
            section_base_values[f_name] = str(val) if val is not None else None

        # FEATURE level
        if feature_tag:
            feature_elems = feat_block.findall(feature_tag)
        else:
            feature_elems = [feat_block]

        for feat in feature_elems:
            feature_values = dict(section_base_values)
            fvalue_path_name = None
            fvalue_rel_path = None

            # non-FVALUE fields under FEATURE
            for f_name, path in pf_fields_no_article.items():
                if not path or not isinstance(path, str):
                    continue
                if "/" in path:
                    first, rest = path.split("/", 1)
                    if first != feature_tag:
                        continue
                    if f_name == "fvalue":
                        fvalue_path_name = f_name
                        fvalue_rel_path = rest
                        continue
                    val = get_text_rel(feat, rest)
                    feature_values[f_name] = str(val) if val is not None else None

            # fvalue handling
            if fvalue_path_name and fvalue_rel_path:
                fvalue_tag = fvalue_rel_path
                if "/" in fvalue_rel_path:
                    fvalue_tag = fvalue_rel_path.split("/")[-1]

                fvalue_elems = feat.findall(fvalue_tag)

                if not explode_multiple_fvalues:
                    if fvalue_elems:
                        single = fvalue_elems[0]
                        val = single.text
                        feature_values["fvalue"] = str(val) if val is not None else None

                        record = {
                            "vendor_name": VENDOR_NAME,
                            "article_id": article_id,
                        }
                        record.update(feature_values)

                        dedup_key = tuple(record.get(col) for col in dedup_key_cols)
                        if dedup_key not in seen_pf_keys:
                            seen_pf_keys.add(dedup_key)
                            pf_records.append(record)
                    continue

                # explode_multiple_fvalues = True
                for fv in fvalue_elems:
                    fv_text = fv.text
                    fv_record_values = dict(feature_values)
                    fv_record_values["fvalue"] = str(fv_text) if fv_text is not None else None

                    record = {
                        "vendor_name": VENDOR_NAME,
                        "article_id": article_id,
                    }
                    record.update(fv_record_values)

                    dedup_key = tuple(record.get(col) for col in dedup_key_cols)
                    if dedup_key in seen_pf_keys:
                        continue
                    seen_pf_keys.add(dedup_key)
                    pf_records.append(record)
            else:
                record = {
                    "vendor_name": VENDOR_NAME,
                    "article_id": article_id,
                }
                record.update(feature_values)

                dedup_key = tuple(record.get(col) for col in dedup_key_cols)
                if dedup_key not in seen_pf_keys:
                    seen_pf_keys.add(dedup_key)
                    pf_records.append(record)

print(f"[INFO] product_features: built {len(pf_records)} records (after dedup).")

# ---------- 3) product_mimes (optional block) ----------

pm_records = []

if product_mimes_cfg:
    # "product_mimes": {
    #   "entity_name": "product_mimes",
    #   "root_path": "BMECAT/T_NEW_CATALOG/ARTICLE",
    #   "source_parent": "MIME_INFO/MIME",
    #   "fields": {
    #       "article_id": { "vendor_products.key_fields.article_id": "article_id" },
    #       "mime_type": "MIME_TYPE",
    #       "mime_source": "MIME_SOURCE",
    #       "mime_purpose": "MIME_PURPOSE",
    #       "mime_descr": "MIME_DESCR",
    #       "mime_order": "MIME_ORDER"
    #   }
    # }

    pm_root_path = product_mimes_cfg["root_path"]
    pm_source_parent = product_mimes_cfg.get("source_parent", "MIME_INFO/MIME")
    pm_fields_cfg = product_mimes_cfg.get("fields", {})

    pm_article_id_primary_path = None
    pm_article_id_fallback_path = None

    pm_key_fields = product_mimes_cfg.get("key_fields")
    if pm_key_fields and "article_id" in pm_key_fields:
        pm_article_id_cfg = pm_key_fields["article_id"]
        pm_article_id_primary_path = pm_article_id_cfg.get("primary_path") or pm_article_id_cfg.get("primary")
        pm_article_id_fallback_path = pm_article_id_cfg.get("fallback_path") or pm_article_id_cfg.get("fallback")
    else:
        pm_article_id_field_cfg = pm_fields_cfg.get("article_id")
        if isinstance(pm_article_id_field_cfg, dict):
            if "vendor_products.key_fields.article_id" in pm_article_id_field_cfg:
                vp_kf = vendor_products_cfg.get("key_fields", {})
                vp_article_cfg = vp_kf.get("article_id")
                if vp_article_cfg:
                    pm_article_id_primary_path = vp_article_cfg.get("primary_path") or vp_article_cfg.get("primary")
                    pm_article_id_fallback_path = vp_article_cfg.get("fallback_path") or vp_article_cfg.get("fallback")

    if not pm_article_id_primary_path and not pm_article_id_fallback_path:
        raise RuntimeError(
            "No article_id definition for product_mimes: "
            "either provide product_mimes.key_fields.article_id or "
            "fields.article_id with vendor_products.key_fields.article_id reference."
        )

    pm_fields_no_article = {k: v for k, v in pm_fields_cfg.items() if k != "article_id"}

    pm_article_nodes = findall_path(root, pm_root_path)
    print(f"[INFO] Found {len(pm_article_nodes)} ARTICLE nodes for product_mimes.")

    for art in pm_article_nodes:
        article_id = None
        if pm_article_id_primary_path:
            article_id = get_text_rel_with_warn(
                art, pm_article_id_primary_path, "product_mimes.article_id.primary"
            )
        if not article_id and pm_article_id_fallback_path:
            article_id = get_text_rel_with_warn(
                art, pm_article_id_fallback_path, "product_mimes.article_id.fallback"
            )

        if not article_id:
            continue

        article_id = str(article_id)

        for mime_elem in art.findall(pm_source_parent):
            record = {
                "vendor_name": VENDOR_NAME,
                "article_id": article_id,
            }

            for out_name, rel_path in pm_fields_no_article.items():
                if not rel_path or not isinstance(rel_path, str):
                    continue
                val = get_text_rel_with_warn(
                    mime_elem, rel_path, f"product_mimes.{out_name}"
                )
                record[out_name] = str(val) if val is not None else None

            pm_records.append(record)

    print(f"[INFO] product_mimes: built {len(pm_records)} records.")
else:
    print("[INFO] product_mimes config not present; skipping product_mimes extraction.")

# ---------- 4) product_relations (optional block) ----------

pr_records = []

if product_relations_cfg:
    # "product_relations": {
    #   "entity_name": "product_relations",
    #   "root_path": "BMECAT/T_NEW_CATALOG/ARTICLE",
    #   "source_parent": "ARTICLE_REFERENCE",
    #   "fields": {
    #       "article_id": { "vendor_products.key_fields.article_id": "article_id" },
    #       "relation_type": "@type",
    #       "target_article_id": "ART_ID_TO"
    #   }
    # }

    pr_root_path = product_relations_cfg["root_path"]
    pr_source_parent = product_relations_cfg.get("source_parent", "ARTICLE_REFERENCE")
    pr_fields_cfg = product_relations_cfg.get("fields", {})

    pr_article_id_primary_path = None
    pr_article_id_fallback_path = None

    pr_key_fields = product_relations_cfg.get("key_fields")
    if pr_key_fields and "article_id" in pr_key_fields:
        pr_article_id_cfg = pr_key_fields["article_id"]
        pr_article_id_primary_path = pr_article_id_cfg.get("primary_path") or pr_article_id_cfg.get("primary")
        pr_article_id_fallback_path = pr_article_id_cfg.get("fallback_path") or pr_article_id_cfg.get("fallback")
    else:
        pr_article_id_field_cfg = pr_fields_cfg.get("article_id")
        if isinstance(pr_article_id_field_cfg, dict):
            if "vendor_products.key_fields.article_id" in pr_article_id_field_cfg:
                vp_kf = vendor_products_cfg.get("key_fields", {})
                vp_article_cfg = vp_kf.get("article_id")
                if vp_article_cfg:
                    pr_article_id_primary_path = vp_article_cfg.get("primary_path") or vp_article_cfg.get("primary")
                    pr_article_id_fallback_path = vp_article_cfg.get("fallback_path") or vp_article_cfg.get("fallback")

    if not pr_article_id_primary_path and not pr_article_id_fallback_path:
        raise RuntimeError(
            "No article_id definition for product_relations: "
            "either provide product_relations.key_fields.article_id or "
            "fields.article_id with vendor_products.key_fields.article_id reference."
        )

    pr_fields_no_article = {k: v for k, v in pr_fields_cfg.items() if k != "article_id"}

    pr_article_nodes = findall_path(root, pr_root_path)
    print(f"[INFO] Found {len(pr_article_nodes)} ARTICLE nodes for product_relations.")

    for art in pr_article_nodes:
        article_id = None
        if pr_article_id_primary_path:
            article_id = get_text_rel_with_warn(
                art, pr_article_id_primary_path, "product_relations.article_id.primary"
            )
        if not article_id and pr_article_id_fallback_path:
            article_id = get_text_rel_with_warn(
                art, pr_article_id_fallback_path, "product_relations.article_id.fallback"
            )

        if not article_id:
            continue

        article_id = str(article_id)

        for rel_elem in art.findall(pr_source_parent):
            record = {
                "vendor_name": VENDOR_NAME,
                "article_id": article_id,
            }

            for out_name, rel_path in pr_fields_no_article.items():
                if not rel_path or not isinstance(rel_path, str):
                    continue

                if rel_path.startswith("@"):
                    attr_name = rel_path[1:]
                    val = rel_elem.get(attr_name)
                    if val is None:
                        key = f"product_relations.{out_name}::{rel_path}"
                        if key not in missing_path_warnings:
                            print(
                                f"[WARN] Configured attribute '{rel_path}' for "
                                f"'product_relations.{out_name}' was not found "
                                f"(at least for one record)."
                            )
                            missing_path_warnings.add(key)
                else:
                    val = get_text_rel_with_warn(
                        rel_elem, rel_path, f"product_relations.{out_name}"
                    )

                record[out_name] = str(val) if val is not None else None

            pr_records.append(record)

    print(f"[INFO] product_relations: built {len(pr_records)} records.")
else:
    print("[INFO] product_relations config not present; skipping product_relations extraction.")

# ---------- 5) product_category_links ----------

pcl_root_path = product_category_links_cfg["root_path"]
pcl_fields = product_category_links_cfg.get("fields", {})

pcl_nodes = findall_path(root, pcl_root_path)
print(
    f"[INFO] Found {len(pcl_nodes)} ARTICLE_TO_CATALOGGROUP_MAP nodes for "
    f"product_category_links."
)

pcl_records = []

for elem in pcl_nodes:
    record = {"vendor_name": VENDOR_NAME}

    for out_name, rel_path in pcl_fields.items():
        val = get_text_rel_with_warn(
            elem, rel_path, f"product_category_links.{out_name}"
        )
        record[out_name] = str(val) if val is not None else None

    pcl_records.append(record)

print(f"[INFO] product_category_links: built {len(pcl_records)} records.")

# ---------- 6) product_prices (optional block) ----------

pp_records = []

if product_prices_cfg:
    # "product_prices": {
    #   "entity_name": "product_prices",
    #   "root_path": "BMECAT/T_NEW_CATALOG/ARTICLE",
    #   "source_parent": "ARTICLE_PRICE_DETAILS/ARTICLE_PRICE",
    #   "fields": {
    #       "article_id": { "vendor_products.key_fields.article_id": "article_id" },
    #       "price_type": "@price_type",
    #       "price_amount": "PRICE_AMOUNT",
    #       "price_currency": "PRICE_CURRENCY"
    #   }
    # }

    pp_root_path = product_prices_cfg["root_path"]
    pp_source_parent = product_prices_cfg.get("source_parent", "ARTICLE_PRICE_DETAILS/ARTICLE_PRICE")
    pp_fields_cfg = product_prices_cfg.get("fields", {})

    pp_article_id_primary_path = None
    pp_article_id_fallback_path = None

    pp_key_fields = product_prices_cfg.get("key_fields")
    if pp_key_fields and "article_id" in pp_key_fields:
        pp_article_id_cfg = pp_key_fields["article_id"]
        pp_article_id_primary_path = pp_article_id_cfg.get("primary_path") or pp_article_id_cfg.get("primary")
        pp_article_id_fallback_path = pp_article_id_cfg.get("fallback_path") or pp_article_id_cfg.get("fallback")
    else:
        pp_article_id_field_cfg = pp_fields_cfg.get("article_id")
        if isinstance(pp_article_id_field_cfg, dict):
            if "vendor_products.key_fields.article_id" in pp_article_id_field_cfg:
                vp_kf = vendor_products_cfg.get("key_fields", {})
                vp_article_cfg = vp_kf.get("article_id")
                if vp_article_cfg:
                    pp_article_id_primary_path = vp_article_cfg.get("primary_path") or vp_article_cfg.get("primary")
                    pp_article_id_fallback_path = vp_article_cfg.get("fallback_path") or vp_article_cfg.get("fallback")

    if not pp_article_id_primary_path and not pp_article_id_fallback_path:
        raise RuntimeError(
            "No article_id definition for product_prices: "
            "either provide product_prices.key_fields.article_id or "
            "fields.article_id with vendor_products.key_fields.article_id reference."
        )

    pp_fields_no_article = {k: v for k, v in pp_fields_cfg.items() if k != "article_id"}

    pp_article_nodes = findall_path(root, pp_root_path)
    print(f"[INFO] Found {len(pp_article_nodes)} ARTICLE nodes for product_prices.")

    for art in pp_article_nodes:
        article_id = None
        if pp_article_id_primary_path:
            article_id = get_text_rel_with_warn(
                art, pp_article_id_primary_path, "product_prices.article_id.primary"
            )
        if not article_id and pp_article_id_fallback_path:
            article_id = get_text_rel_with_warn(
                art, pp_article_id_fallback_path, "product_prices.article_id.fallback"
            )

        if not article_id:
            continue

        article_id = str(article_id)

        for price_elem in art.findall(pp_source_parent):
            record = {
                "vendor_name": VENDOR_NAME,
                "article_id": article_id,
            }

            for out_name, rel_path in pp_fields_no_article.items():
                if not rel_path or not isinstance(rel_path, str):
                    continue

                if rel_path.startswith("@"):
                    attr_name = rel_path[1:]
                    val = price_elem.get(attr_name)
                    if val is None:
                        key = f"product_prices.{out_name}::{rel_path}"
                        if key not in missing_path_warnings:
                            print(
                                f"[WARN] Configured attribute '{rel_path}' for "
                                f"'product_prices.{out_name}' was not found "
                                f"(at least for one record)."
                            )
                            missing_path_warnings.add(key)
                else:
                    val = get_text_rel_with_warn(
                        price_elem, rel_path, f"product_prices.{out_name}"
                    )

                record[out_name] = str(val) if val is not None else None

            pp_records.append(record)

    print(f"[INFO] product_prices: built {len(pp_records)} records.")
else:
    print("[INFO] product_prices config not present; skipping product_prices extraction.")

# ---------- 7) vendor_categories (optional block) ----------

vc_records = []

if vendor_categories_cfg:
    # Expected config example:
    # "vendor_categories": {
    #   "entity_name": "vendor_categories",
    #   "root_path": "BMECAT/T_NEW_CATALOG/CATALOG_GROUP_SYSTEM/CATALOG_STRUCTURE",
    #   "fields": {
    #       "category_id": "GROUP_ID",
    #       "category_name": "GROUP_NAME",
    #       "categry_path": "ancestors.GROUP_NAME",
    #       "order": "GROUP_ORDER",
    #       "type": "@type"
    #   }
    # }

    vc_root_path = vendor_categories_cfg["root_path"]
    vc_fields_cfg = vendor_categories_cfg.get("fields", {})

    # Resolve all category nodes
    vc_nodes = findall_path(root, vc_root_path)
    print(f"[INFO] Found {len(vc_nodes)} CATALOG_STRUCTURE nodes for vendor_categories.")

    # For building category_path we need parent relationships and names.
    categories_cfg = config.get("categories", {})
    cat_tree_fields = categories_cfg.get("fields", {})

    id_path_for_tree = cat_tree_fields.get("category_id") or vc_fields_cfg.get("category_id") or "GROUP_ID"
    pid_path_for_tree = cat_tree_fields.get("parent_id")
    name_path_for_tree = cat_tree_fields.get("name") or vc_fields_cfg.get("category_name") or "GROUP_NAME"

    cat_parents = {}
    cat_names = {}

    for node in vc_nodes:
        cid = get_text_rel_with_warn(node, id_path_for_tree, "vendor_categories.tree.category_id")
        if not cid:
            continue
        cid = str(cid)
        pid = None
        if pid_path_for_tree:
            pid_val = get_text_rel(node, pid_path_for_tree)
            if pid_val is not None:
                pid = str(pid_val)
        name_val = get_text_rel(node, name_path_for_tree)
        cat_names[cid] = str(name_val) if name_val is not None else None
        cat_parents[cid] = pid

    def build_category_path(category_id: str):
        if not category_id:
            return None
        path_names = []
        current = category_id
        visited = set()
        while current and current not in visited:
            visited.add(current)
            name = cat_names.get(current)
            if name:
                path_names.append(name)
            current = cat_parents.get(current)
        if not path_names:
            return None
        path_names.reverse()
        return " > ".join(path_names)

    for node in vc_nodes:
        record = {"vendor_name": VENDOR_NAME}

        # Resolve current node's id once for re-use (e.g. for path)
        cid_val = get_text_rel_with_warn(node, id_path_for_tree, "vendor_categories.category_id_for_record")
        cid = str(cid_val) if cid_val is not None else None

        for out_name, rel_path in vc_fields_cfg.items():
            if not isinstance(rel_path, str):
                record[out_name] = None
                continue

            # special handling for ancestors.* notation (e.g. "ancestors.GROUP_NAME")
            if rel_path.startswith("ancestors."):
                record[out_name] = build_category_path(cid)
                continue

            # attribute-based fields like "@type"
            if rel_path.startswith("@"):
                attr_name = rel_path[1:]
                val = node.get(attr_name)
                if val is None:
                    key = f"vendor_categories.{out_name}::{rel_path}"
                    if key not in missing_path_warnings:
                        print(
                            f"[WARN] Configured attribute '{rel_path}' for "
                            f"'vendor_categories.{out_name}' was not found "
                            f"(at least for one record)."
                        )
                        missing_path_warnings.add(key)
                record[out_name] = str(val) if val is not None else None
                continue

            # standard element text
            val = get_text_rel_with_warn(node, rel_path, f"vendor_categories.{out_name}")
            record[out_name] = str(val) if val is not None else None

        vc_records.append(record)

    print(f"[INFO] vendor_categories: built {len(vc_records)} records.")
else:
    print("[INFO] vendor_categories config not present; skipping vendor_categories extraction.")

# ---------- Write outputs ----------

vp_key = f"{BMECAT_OUTPUT_PREFIX}{VENDOR_NAME}_vendor_products.json"
pf_key = f"{BMECAT_OUTPUT_PREFIX}{VENDOR_NAME}_product_features.json"
pcl_key = f"{BMECAT_OUTPUT_PREFIX}{VENDOR_NAME}_product_category_links.json"

write_ndjson_to_s3(OUTPUT_BUCKET, vp_key, vp_records)
write_ndjson_to_s3(OUTPUT_BUCKET, pf_key, pf_records)
write_ndjson_to_s3(OUTPUT_BUCKET, pcl_key, pcl_records)

if product_mimes_cfg:
    pm_key = f"{BMECAT_OUTPUT_PREFIX}{VENDOR_NAME}_product_mimes.json"
    write_ndjson_to_s3(OUTPUT_BUCKET, pm_key, pm_records)

if product_relations_cfg:
    pr_key = f"{BMECAT_OUTPUT_PREFIX}{VENDOR_NAME}_product_relations.json"
    write_ndjson_to_s3(OUTPUT_BUCKET, pr_key, pr_records)

if product_prices_cfg:
    pp_key = f"{BMECAT_OUTPUT_PREFIX}{VENDOR_NAME}_product_prices.json"
    write_ndjson_to_s3(OUTPUT_BUCKET, pp_key, pp_records)

if vendor_categories_cfg:
    vc_key = f"{BMECAT_OUTPUT_PREFIX}{VENDOR_NAME}_vendor_categories.json"
    write_ndjson_to_s3(OUTPUT_BUCKET, vc_key, vc_records)

# ---------- Summary log ----------

summary = {
    "status": "ok",
    "job_name": JOB_NAME,
    "job_run_id": JOB_RUN_ID,
    "vendor_name": VENDOR_NAME,
    "input_bucket": INPUT_BUCKET,
    "input_key": BMECAT_INPUT_KEY,
    "output_bucket": OUTPUT_BUCKET,
    "output_prefix": BMECAT_OUTPUT_PREFIX,
    "counts": {
        "vendor_products": len(vp_records),
        "product_features": len(pf_records),
        "product_mimes": len(pm_records),
        "product_relations": len(pr_records),
        "product_category_links": len(pcl_records),
        "product_prices": len(pp_records),
        "vendor_categories": len(vc_records),
        "skipped_articles_no_id": skipped_articles_no_id,
    },
}

print("[INFO] Job summary:")
print(json.dumps(summary, ensure_ascii=False, indent=2))
