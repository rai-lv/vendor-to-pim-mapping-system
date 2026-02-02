#!/usr/bin/env python3
"""
Repository Documentation and Manifest Validator

This tool validates repository documentation and manifest files against
specifications defined in docs/standards/.

CURRENT VALIDATION COVERAGE:
  ✅ Job Manifests (job_manifest.yaml)
  ✅ Artifacts Catalog (docs/catalogs/artifacts_catalog.md)
  ✅ Job Inventory (docs/catalogs/job_inventory.md)

VALIDATION RULES:

1. Job Manifests (per docs/standards/job_manifest_spec.md):
   - Required fields: job_id, glue_job_name, runtime, parameters, inputs,
     outputs, side_effects, logging_and_receipt
   - job_id must match folder name
   - Placeholder syntax: Must use ${NAME}, not <NAME> or {NAME}
   - TBD handling: If any field contains "TBD", notes field is required with:
     * TBD_EXPLANATIONS block in notes
     * Each TBD field path mentioned in notes

2. Artifacts Catalog (per docs/standards/artifacts_catalog_spec.md):
   - Required fields (in order): artifact_id, file_name_pattern,
     s3_location_pattern, format, producer_job_id, producers/consumers,
     presence_on_success, purpose, content_contract, evidence_sources
   - Optional governance fields (in order): producer_glue_job_name,
     stability, breaking_change_rules
   - Purpose must not be TBD
   - Entries with "producers" field must be in shared artifacts allowlist

3. Job Inventory (per docs/standards/job_inventory_spec.md):
   - Required headings (in order): # Job Inventory, ## Scope and evidence,
     ## Jobs, ## Dependency links, ## Open verification items
   - Jobs table with required columns (in order)

KNOWN LIMITATIONS (see VALIDATION_ANALYSIS.md):
  ⚠️  Business Descriptions: NOT IMPLEMENTED
  ⚠️  Script Cards: NOT IMPLEMENTED
  ⚠️  Codable Task Specs: NOT IMPLEMENTED
  ⚠️  Decision Records: NOT IMPLEMENTED
  ⚠️  Context Documents: NOT IMPLEMENTED
  ⚠️  Security Checks: NOT IMPLEMENTED
  ⚠️  Consistency Checks: NOT IMPLEMENTED

For detailed specifications and rationale, see:
  - docs/standards/job_manifest_spec.md
  - docs/standards/artifacts_catalog_spec.md
  - docs/standards/job_inventory_spec.md
  - docs/standards/validation_standard.md
  - VALIDATION_ANALYSIS.md (validation coverage analysis)
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]

MANIFEST_REQUIRED_KEYS = {
    "job_id",
    "glue_job_name",
    "runtime",
    "parameters",
    "inputs",
    "outputs",
    "side_effects",
    "logging_and_receipt",
}

ARTIFACTS_REQUIRED_KEYS_WITH_PRODUCERS = [
    "artifact_id",
    "file_name_pattern",
    "s3_location_pattern",
    "format",
    "producer_job_id",
    "producers",
    "consumers",
    "presence_on_success",
    "purpose",
    "content_contract",
    "evidence_sources",
]

ARTIFACTS_REQUIRED_KEYS_WITHOUT_PRODUCERS = [
    "artifact_id",
    "file_name_pattern",
    "s3_location_pattern",
    "format",
    "producer_job_id",
    "consumers",
    "presence_on_success",
    "purpose",
    "content_contract",
    "evidence_sources",
]

# Optional governance fields allowed (in order) after evidence_sources in artifacts_catalog entries.
# These are documented in docs/standards/artifacts_catalog_spec.md Section 6.
# They provide additional metadata for governance and stability tracking.
OPTIONAL_GOVERNANCE_FIELDS = [
    "producer_glue_job_name",  # Glue job name (may differ from job_id)
    "stability",               # Stability rating: experimental, stable, deprecated
    "breaking_change_rules",   # Breaking change policies for this artifact
]

JOB_INVENTORY_HEADINGS = [
    "# Job Inventory",
    "## Scope and evidence",
    "## Jobs",
    "## Dependency links",
    "## Open verification items",
]

JOB_INVENTORY_COLUMNS = [
    "job_id",
    "job_dir",
    "executor",
    "deployment_name",
    "runtime",
    "owner",
    "business_purpose",
    "parameters",
    "inputs",
    "outputs",
    "side_effects",
    "evidence_artifacts",
    "upstream_job_ids",
    "downstream_job_ids",
    "status",
    "last_reviewed",
]


class Violation:
    def __init__(self, scope: str, path: Path, rule_id: str, message: str):
        self.scope = scope
        self.path = path
        self.rule_id = rule_id
        self.message = message

    def format(self) -> str:
        return f"FAIL {self.scope} {self.path.as_posix()} {self.rule_id} {self.message}"


def load_yaml(path: Path):
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except Exception as exc:
        return exc


def collect_tbd_paths(data):
    paths = []

    def walk(value, path):
        if value == "TBD":
            paths.append(path)
            return
        if isinstance(value, dict):
            for key, item in value.items():
                next_path = f"{path}.{key}" if path else key
                walk(item, next_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                next_path = f"{path}[{index}]" if path else f"[{index}]"
                walk(item, next_path)

    walk(data, "")
    return sorted(set(paths))


def contains_invalid_placeholder(value: str) -> bool:
    """
    Check if string contains invalid placeholder syntax.
    
    Valid placeholder syntax: ${NAME} (Bash-style variable references)
    Invalid placeholder syntax:
      - <NAME> (angle brackets reserved for non-placeholder values like URLs)
      - {NAME} (curly braces alone are not valid)
    
    This enforces placeholder normalization per docs/standards/naming_standard.md.
    """
    # Check for <NAME> style (invalid)
    if re.search(r"<[^>]+>", value):
        return True
    # Remove valid ${NAME} style, then check for remaining {NAME} style (invalid)
    cleaned = re.sub(r"\$\{[^}]+\}", "", value)
    return bool(re.search(r"\{[^}]+\}", cleaned))


def scan_for_invalid_placeholders(data):
    invalid_paths = []

    def walk(value, path):
        if isinstance(value, str):
            if contains_invalid_placeholder(value):
                invalid_paths.append(path)
            return
        if isinstance(value, dict):
            for key, item in value.items():
                next_path = f"{path}.{key}" if path else key
                walk(item, next_path)
        elif isinstance(value, list):
            for index, item in enumerate(value):
                next_path = f"{path}[{index}]" if path else f"[{index}]"
                walk(item, next_path)

    walk(data, "")
    return sorted(set(invalid_paths))


def validate_manifest(path: Path):
    violations = []
    data = load_yaml(path)
    if isinstance(data, Exception):
        violations.append(
            Violation(
                "manifest",
                path,
                "invalid_yaml",
                f"Unable to parse YAML: {data}",
            )
        )
        return violations

    if not isinstance(data, dict):
        violations.append(
            Violation(
                "manifest",
                path,
                "invalid_structure",
                "Manifest must be a mapping/object.",
            )
        )
        return violations

    missing_keys = [key for key in sorted(MANIFEST_REQUIRED_KEYS) if key not in data]
    if missing_keys:
        violations.append(
            Violation(
                "manifest",
                path,
                "missing_required_keys",
                f"Missing required top-level keys: {', '.join(missing_keys)}.",
            )
        )

    job_id = data.get("job_id")
    folder_job_id = path.parent.name
    if job_id is not None and job_id != folder_job_id:
        violations.append(
            Violation(
                "manifest",
                path,
                "job_id_mismatch",
                f"job_id '{job_id}' does not match folder '{folder_job_id}'.",
            )
        )

    invalid_placeholder_paths = scan_for_invalid_placeholders(data)
    for invalid_path in invalid_placeholder_paths:
        violations.append(
            Violation(
                "manifest",
                path,
                "invalid_placeholder",
                f"Invalid placeholder style in field '{invalid_path}'.",
            )
        )

    # TBD EXPLANATION REQUIREMENT:
    # Per docs/standards/job_manifest_spec.md, if any field contains "TBD",
    # the manifest must include a "notes" field with:
    #   1. A "TBD_EXPLANATIONS:" block
    #   2. An explanation for each TBD field path
    # This ensures TBD values are tracked and eventually resolved.
    tbd_paths = collect_tbd_paths(data)
    if tbd_paths:
        notes = data.get("notes")
        if notes is None:
            violations.append(
                Violation(
                    "manifest",
                    path,
                    "missing_notes",
                    "notes is required when any TBD appears in the manifest.",
                )
            )
        elif not isinstance(notes, list):
            violations.append(
                Violation(
                    "manifest",
                    path,
                    "invalid_notes",
                    "notes must be a list when TBD values are present.",
                )
            )
        else:
            notes_text = [str(item) for item in notes]
            if not any("TBD_EXPLANATIONS" in item for item in notes_text):
                violations.append(
                    Violation(
                        "manifest",
                        path,
                        "missing_tbd_block",
                        "notes must include a TBD_EXPLANATIONS block.",
                    )
                )
            for tbd_path in tbd_paths:
                if not any(tbd_path in item for item in notes_text):
                    violations.append(
                        Violation(
                            "manifest",
                            path,
                            "missing_tbd_explanation",
                            f"notes must mention TBD field path '{tbd_path}'.",
                        )
                    )

    return violations


def load_shared_artifacts_allowlist(path: Path):
    if not path.exists():
        return set()
    data = load_yaml(path)
    if isinstance(data, Exception):
        return set()
    if isinstance(data, list):
        return {str(item) for item in data}
    if isinstance(data, dict):
        return {str(item) for item in data.get("allowlist", [])}
    return set()


# Markdown bullet: leading spaces allowed; dash; space; then rest
_BULLET_RE = re.compile(r"^(?P<indent>\s*)-\s+(?P<rest>.*)$")


def parse_artifact_entry(lines):
    """
    Extract the ordered list of *top-level* keys from an artifact entry.

    Key design goal:
    - Accept Markdown-valid indentation for the entry's main bullets (often 0–3 spaces, but allow any).
    - Do NOT treat nested bullets (e.g. under content_contract) as top-level keys.

    Strategy:
    - Collect all bullet lines that look like 'key: ...' plus their indentation level.
    - Determine the minimum indentation among those candidates within the entry block.
    - Treat only bullets at that minimum indentation as the entry's top-level keys.
    """
    candidates = []
    for raw in lines:
        m = _BULLET_RE.match(raw)
        if not m:
            continue
        rest = m.group("rest")
        if ":" not in rest:
            continue
        key, value = rest.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        indent_len = len(m.group("indent"))
        candidates.append((indent_len, key, value))

    if not candidates:
        return [], {}

    min_indent = min(i for i, _, _ in candidates)

    keys = []
    values = {}
    for indent_len, key, value in candidates:
        if indent_len != min_indent:
            continue
        keys.append(key)
        if key not in values:
            values[key] = value

    return keys, values


def validate_artifacts_catalog(path: Path, allowlist):
    violations = []

    if not path.exists():
        violations.append(
            Violation(
                "artifacts_catalog",
                path,
                "missing_file",
                "docs/artifacts_catalog.md does not exist.",
            )
        )
        return violations

    lines = path.read_text(encoding="utf-8").splitlines()

    # Spec requires a top-level title; be robust to whitespace.
    if not any(line.strip() == "# Artifacts Catalog" for line in lines):
        violations.append(
            Violation(
                "artifacts_catalog",
                path,
                "missing_title",
                "Artifacts catalog must include the '# Artifacts Catalog' title.",
            )
        )

    heading_indices = [index for index, line in enumerate(lines) if line.startswith("## ")]
    for idx, start in enumerate(heading_indices):
        end = heading_indices[idx + 1] if idx + 1 < len(heading_indices) else len(lines)
        heading_line = lines[start]
        artifact_id = heading_line[3:].strip()
        entry_lines = lines[start + 1 : end]
        keys, values = parse_artifact_entry(entry_lines)

        has_producers = "producers" in keys
        expected_keys = (
            ARTIFACTS_REQUIRED_KEYS_WITH_PRODUCERS
            if has_producers
            else ARTIFACTS_REQUIRED_KEYS_WITHOUT_PRODUCERS
        )

        # Spec allows optional governance fields after evidence_sources (in this exact order):
        # producer_glue_job_name, stability, breaking_change_rules.
        # Accept either:
        # - exact required keys, OR
        # - required keys plus a valid optional governance tail.
        extra_keys = []
        if keys[: len(expected_keys)] == expected_keys:
            extra_keys = keys[len(expected_keys) :]
        is_valid_governance_tail = extra_keys == OPTIONAL_GOVERNANCE_FIELDS[: len(extra_keys)]

        if not (keys == expected_keys or is_valid_governance_tail):
            allowed = ", ".join(expected_keys)
            allowed_with_tail = (
                allowed
                + " [+ optional: "
                + ", ".join(OPTIONAL_GOVERNANCE_FIELDS)
                + "]"
            )
            violations.append(
                Violation(
                    "artifacts_catalog",
                    path,
                    "invalid_entry_structure",
                    f"Entry '{artifact_id}' keys must be in order: {allowed_with_tail}.",
                )
            )

        purpose_value = values.get("purpose")
        if purpose_value == "TBD":
            violations.append(
                Violation(
                    "artifacts_catalog",
                    path,
                    "purpose_tbd",
                    f"Entry '{artifact_id}' purpose must not be TBD.",
                )
            )

        if has_producers and artifact_id not in allowlist:
            violations.append(
                Violation(
                    "artifacts_catalog",
                    path,
                    "producers_not_allowlisted",
                    f"Entry '{artifact_id}' has producers but is not allowlisted.",
                )
            )

    return violations


def validate_job_inventory(path: Path):
    violations = []

    if not path.exists():
        violations.append(
            Violation(
                "job_inventory",
                path,
                "missing_file",
                "docs/job_inventory.md does not exist.",
            )
        )
        return violations

    lines = path.read_text(encoding="utf-8").splitlines()
    heading_positions = {}
    for index, line in enumerate(lines):
        for heading in JOB_INVENTORY_HEADINGS:
            if line.strip() == heading:
                heading_positions[heading] = index

    if len(heading_positions) != len(JOB_INVENTORY_HEADINGS):
        missing = [heading for heading in JOB_INVENTORY_HEADINGS if heading not in heading_positions]
        violations.append(
            Violation(
                "job_inventory",
                path,
                "missing_headings",
                f"Missing required headings: {', '.join(missing)}.",
            )
        )
    else:
        indices = [heading_positions[heading] for heading in JOB_INVENTORY_HEADINGS]
        if indices != sorted(indices):
            violations.append(
                Violation(
                    "job_inventory",
                    path,
                    "heading_order",
                    "Required headings are not in the exact required order.",
                )
            )

    unexpected_headings = [
        line.strip()
        for line in lines
        if line.startswith("## ") and line.strip() not in JOB_INVENTORY_HEADINGS[1:]
    ]
    if unexpected_headings:
        violations.append(
            Violation(
                "job_inventory",
                path,
                "unexpected_headings",
                f"Unexpected top-level headings found: {', '.join(unexpected_headings)}.",
            )
        )

    jobs_heading = "## Jobs"
    if jobs_heading in heading_positions:
        start = heading_positions[jobs_heading]
        end_candidates = [
            heading_positions[heading]
            for heading in JOB_INVENTORY_HEADINGS
            if heading_positions.get(heading, -1) > start
        ]
        end = min(end_candidates) if end_candidates else len(lines)
        section_lines = lines[start + 1 : end]
        table_header = next((line for line in section_lines if line.strip().startswith("|")), None)
        if table_header is None:
            violations.append(
                Violation(
                    "job_inventory",
                    path,
                    "missing_jobs_table",
                    "Jobs section must include a markdown table.",
                )
            )
        else:
            columns = [col.strip() for col in table_header.strip().strip("|").split("|")]
            if columns != JOB_INVENTORY_COLUMNS:
                violations.append(
                    Violation(
                        "job_inventory",
                        path,
                        "invalid_jobs_table_columns",
                        "Jobs table columns must match the spec names and order.",
                    )
                )

    return violations


def find_manifest_paths():
    return sorted(REPO_ROOT.glob("jobs/*/*/job_manifest.yaml"))


def show_coverage():
    """
    Display validation coverage report.
    
    Shows which validation types are implemented vs not implemented.
    Useful for understanding tool limitations and planning future work.
    """
    print("=" * 70)
    print("VALIDATION COVERAGE REPORT")
    print("=" * 70)
    print()
    print("IMPLEMENTED VALIDATORS:")
    print("  ✅ Job Manifests (job_manifest.yaml)")
    print("     - Required fields validation")
    print("     - job_id matching folder name")
    print("     - Placeholder syntax enforcement (${NAME} only)")
    print("     - TBD explanation requirements")
    print()
    print("  ✅ Artifacts Catalog (docs/catalogs/artifacts_catalog.md)")
    print("     - Entry structure validation")
    print("     - Required fields in correct order")
    print("     - Optional governance fields support")
    print("     - Purpose not TBD enforcement")
    print("     - Producers allowlist check")
    print()
    print("  ✅ Job Inventory (docs/catalogs/job_inventory.md)")
    print("     - Required headings validation")
    print("     - Heading order enforcement")
    print("     - Jobs table structure validation")
    print()
    print("-" * 70)
    print("NOT IMPLEMENTED (Future Work):")
    print("  ⚠️  Business Descriptions")
    print("     - See: docs/standards/business_job_description_spec.md")
    print()
    print("  ⚠️  Script Cards")
    print("     - See: docs/standards/script_card_spec.md")
    print()
    print("  ⚠️  Codable Task Specifications")
    print("     - See: docs/standards/codable_task_spec.md")
    print()
    print("  ⚠️  Decision Records")
    print("     - See: docs/standards/decision_records_standard.md")
    print()
    print("  ⚠️  Context Layer Documents")
    print("     - development_approach.md, target_agent_system.md,")
    print("     - documentation_system_catalog.md, glossary.md, system_context.md")
    print()
    print("  ⚠️  Process Layer Documents")
    print("     - workflow_guide.md, contribution_approval_guide.md")
    print()
    print("  ⚠️  Agent Layer Documents")
    print("     - agent_role_charter.md, .github/agents/*.md")
    print()
    print("  ⚠️  Security Validation")
    print("     - Secret detection, credential scanning, SQL injection checks")
    print()
    print("  ⚠️  Consistency Validation")
    print("     - Cross-document reference checking, contradiction detection")
    print()
    print("-" * 70)
    print("COVERAGE: 30% (3/10 validation types)")
    print()
    print("For detailed analysis and recommendations, see VALIDATION_ANALYSIS.md")
    print("=" * 70)


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Validate repo standards compliance.",
        epilog="Run with --coverage to see validation coverage report."
    )
    parser.add_argument("--all", action="store_true", help="Run all validations.")
    parser.add_argument("--manifests", action="store_true", help="Validate job manifests.")
    parser.add_argument(
        "--artifacts-catalog",
        action="store_true",
        help="Validate the artifacts catalog.",
    )
    parser.add_argument(
        "--job-inventory",
        action="store_true",
        help="Validate the job inventory.",
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Show validation coverage report and exit.",
    )
    args = parser.parse_args(argv)
    if not (args.all or args.manifests or args.artifacts_catalog or args.job_inventory or args.coverage):
        parser.error("At least one validation flag must be provided.")
    return args


def main(argv):
    args = parse_args(argv)
    
    # Handle coverage report request
    if args.coverage:
        show_coverage()
        return 0
    
    run_manifests = args.all or args.manifests
    run_artifacts = args.all or args.artifacts_catalog
    run_inventory = args.all or args.job_inventory

    violations = []
    pass_count = 0

    if run_manifests:
        manifest_paths = find_manifest_paths()
        for path in manifest_paths:
            manifest_violations = validate_manifest(path)
            if manifest_violations:
                violations.extend(manifest_violations)
            else:
                pass_count += 1

    if run_artifacts:
        catalog_path = REPO_ROOT / "docs" / "artifacts_catalog.md"
        allowlist_path = REPO_ROOT / "docs" / "registries" / "shared_artifacts_allowlist.yaml"
        allowlist = load_shared_artifacts_allowlist(allowlist_path)
        artifacts_violations = validate_artifacts_catalog(catalog_path, allowlist)
        if artifacts_violations:
            violations.extend(artifacts_violations)
        else:
            pass_count += 1

    if run_inventory:
        inventory_path = REPO_ROOT / "docs" / "job_inventory.md"
        inventory_violations = validate_job_inventory(inventory_path)
        if inventory_violations:
            violations.extend(inventory_violations)
        else:
            pass_count += 1

    for violation in violations:
        print(violation.format())

    fail_count = len(violations)
    print(f"SUMMARY pass={pass_count} fail={fail_count}")

    return 2 if fail_count else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
