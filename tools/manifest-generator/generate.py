#!/usr/bin/env python3
"""
Manifest Generator Tool

A scaffolding tool that performs static analysis on glue_script.py files
to extract job interface facts and produce draft job_manifest.yaml files.

This is a TOOL (not an agent) per docs/context/target_agent_system.md:
- Deterministic extraction (no interpretation)
- Evidence-based (cites script line numbers)
- Outputs require human/agent review
"""

import ast
import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import yaml


class ManifestExtractor:
    """Extracts manifest data from Python script using AST analysis."""
    
    def __init__(self, script_path: str, verbose: bool = False):
        self.script_path = Path(script_path)
        self.verbose = verbose
        self.source_code = self.script_path.read_text()
        self.lines = self.source_code.splitlines()
        self.tree = ast.parse(self.source_code, filename=str(self.script_path))
        self.evidence = []  # List of evidence notes with line numbers
        
    def log(self, message: str):
        """Log verbose output."""
        if self.verbose:
            print(f"[EXTRACT] {message}")
    
    def add_evidence(self, note: str):
        """Add evidence note."""
        self.evidence.append(note)
        self.log(note)
    
    def extract_job_id(self, override: Optional[str] = None) -> str:
        """Extract job_id from folder name."""
        if override:
            return override
        # job_id is parent directory name
        job_id = self.script_path.parent.name
        self.add_evidence(f"job_id: Derived from folder name '{job_id}'")
        return job_id
    
    def extract_runtime(self) -> str:
        """Detect runtime from imports."""
        has_spark_context = False
        has_glue_context = False
        has_glue_utils = False
        import_lines = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if 'pyspark' in alias.name or 'SparkContext' in alias.name:
                        has_spark_context = True
                        import_lines.append(node.lineno)
                    if 'GlueContext' in alias.name:
                        has_glue_context = True
                        import_lines.append(node.lineno)
                    if 'awsglue' in alias.name:
                        has_glue_utils = True
                        import_lines.append(node.lineno)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    if 'pyspark' in node.module or 'SparkContext' in node.module:
                        has_spark_context = True
                        import_lines.append(node.lineno)
                    if 'GlueContext' in node.module or 'awsglue.context' in node.module:
                        has_glue_context = True
                        import_lines.append(node.lineno)
                    if 'awsglue' in node.module:
                        has_glue_utils = True
                        import_lines.append(node.lineno)
        
        runtime = "TBD"
        if has_spark_context or has_glue_context:
            runtime = "pyspark"
            self.add_evidence(f"runtime: Detected 'pyspark' from SparkContext/GlueContext imports (lines {', '.join(map(str, set(import_lines)))})")
        elif has_glue_utils and not has_spark_context:
            runtime = "python_shell"
            self.add_evidence(f"runtime: Detected 'python_shell' from awsglue.utils without Spark imports (line {min(import_lines) if import_lines else 'N/A'})")
        else:
            runtime = "python"
            self.add_evidence(f"runtime: Defaulting to 'python' (no Glue/Spark imports detected)")
        
        return runtime
    
    def extract_parameters(self) -> List[str]:
        """Extract parameter names from getResolvedOptions."""
        parameters = []
        found_line = None
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                # Check if this is getResolvedOptions call
                if (isinstance(node.func, ast.Name) and node.func.id == 'getResolvedOptions') or \
                   (isinstance(node.func, ast.Attribute) and node.func.attr == 'getResolvedOptions'):
                    # Second argument should be the list of parameter names
                    if len(node.args) >= 2:
                        arg = node.args[1]
                        found_line = node.lineno
                        if isinstance(arg, ast.List):
                            for elt in arg.elts:
                                if isinstance(elt, ast.Constant):
                                    param = elt.value
                                    # Exclude Glue-provided parameters
                                    if param not in ['JOB_NAME', 'JOB_RUN_ID']:
                                        parameters.append(param)
                        elif isinstance(arg, ast.Name):
                            # Reference to a variable - try to find it
                            var_name = arg.id
                            for n in ast.walk(self.tree):
                                if isinstance(n, ast.Assign):
                                    for target in n.targets:
                                        if isinstance(target, ast.Name) and target.id == var_name:
                                            if isinstance(n.value, ast.List):
                                                for elt in n.value.elts:
                                                    if isinstance(elt, ast.Constant):
                                                        param = elt.value
                                                        if param not in ['JOB_NAME', 'JOB_RUN_ID']:
                                                            parameters.append(param)
        
        if found_line:
            self.add_evidence(f"parameters: Extracted {len(parameters)} parameters from getResolvedOptions call (line {found_line})")
        else:
            self.add_evidence(f"parameters: No getResolvedOptions call found - using empty list")
        
        return parameters
    
    def find_s3_operations(self) -> Tuple[List[Dict], List[Dict]]:
        """Find S3 read and write operations."""
        reads = []
        writes = []
        
        # Look for boto3 s3.get_object, s3.put_object, spark.read, df.write patterns
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                # boto3 s3.get_object
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'get_object':
                        bucket, key = self._extract_s3_args(node)
                        if bucket or key:
                            reads.append({
                                'bucket': bucket,
                                'key': key,
                                'line': node.lineno,
                                'method': 'boto3.get_object'
                            })
                    # boto3 s3.put_object
                    elif node.func.attr == 'put_object':
                        bucket, key = self._extract_s3_args(node)
                        if bucket or key:
                            writes.append({
                                'bucket': bucket,
                                'key': key,
                                'line': node.lineno,
                                'method': 'boto3.put_object'
                            })
                    # spark.read.json / .csv / etc
                    elif node.func.attr in ['json', 'csv', 'parquet', 'text']:
                        if len(node.args) > 0:
                            path = self._extract_string_value(node.args[0])
                            if path:
                                bucket, key = self._parse_s3_path(path)
                                reads.append({
                                    'bucket': bucket,
                                    'key': key,
                                    'line': node.lineno,
                                    'method': f'spark.read.{node.func.attr}',
                                    'format': node.func.attr
                                })
        
        self.add_evidence(f"S3 operations: Found {len(reads)} read operations and {len(writes)} write operations")
        return reads, writes
    
    def _extract_s3_args(self, node: ast.Call) -> Tuple[Optional[str], Optional[str]]:
        """Extract Bucket and Key from s3 operation."""
        bucket = None
        key = None
        
        # Check keyword arguments
        for keyword in node.keywords:
            if keyword.arg == 'Bucket':
                bucket = self._extract_string_value(keyword.value)
            elif keyword.arg == 'Key':
                key = self._extract_string_value(keyword.value)
        
        return bucket, key
    
    def _extract_string_value(self, node: ast.AST) -> Optional[str]:
        """Extract string value from AST node, handling variables."""
        if isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Name):
            # It's a variable reference - return placeholder
            return f"${{{node.id}}}"
        elif isinstance(node, ast.JoinedStr):
            # f-string
            parts = []
            for value in node.values:
                if isinstance(value, ast.Constant):
                    parts.append(str(value.value))
                elif isinstance(value, ast.FormattedValue):
                    if isinstance(value.value, ast.Name):
                        parts.append(f"${{{value.value.id}}}")
            return ''.join(parts)
        elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            # String concatenation
            left = self._extract_string_value(node.left)
            right = self._extract_string_value(node.right)
            if left and right:
                return left + right
        elif isinstance(node, ast.Call):
            # Function call - might be format() or similar
            if isinstance(node.func, ast.Attribute) and node.func.attr == 'format':
                # String.format() call
                return self._extract_string_value(node.func.value)
        
        return None
    
    def _parse_s3_path(self, path: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse s3://bucket/key into components."""
        if path.startswith('s3://'):
            parts = path[5:].split('/', 1)
            bucket = parts[0] if parts else None
            key = parts[1] if len(parts) > 1 else None
            return bucket, key
        return None, None
    
    def detect_side_effects(self) -> Dict[str, Any]:
        """Detect delete and overwrite operations."""
        deletes_inputs = False
        overwrites_outputs = True  # Conservative default
        delete_lines = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'delete_object':
                        deletes_inputs = True
                        delete_lines.append(node.lineno)
        
        side_effects = {
            'deletes_inputs': deletes_inputs,
            'overwrites_outputs': overwrites_outputs
        }
        
        if deletes_inputs:
            self.add_evidence(f"side_effects.deletes_inputs: Detected delete_object calls (lines {', '.join(map(str, delete_lines))})")
        else:
            self.add_evidence(f"side_effects.deletes_inputs: No delete operations found")
        
        self.add_evidence(f"side_effects.overwrites_outputs: Defaulting to true (conservative - script does not check existence before write)")
        
        return side_effects
    
    def detect_receipt_and_counters(self) -> Dict[str, Any]:
        """Detect run receipt writing and counter emission."""
        writes_receipt = False
        receipt_bucket = None
        receipt_pattern = None
        counters = []
        receipt_lines = []
        
        reads, writes = self.find_s3_operations()
        
        # Look for writes that might be receipts
        for write in writes:
            key = write.get('key', '')
            if key and ('receipt' in key.lower() or 'run_' in key.lower()):
                writes_receipt = True
                receipt_bucket = write.get('bucket')
                receipt_pattern = key
                receipt_lines.append(write['line'])
        
        result = {
            'writes_run_receipt': writes_receipt,
            'run_receipt_bucket': receipt_bucket if writes_receipt else None,
            'run_receipt_key_pattern': receipt_pattern if writes_receipt else None,
            'counters_observed': counters if counters else []
        }
        
        if writes_receipt:
            self.add_evidence(f"logging_and_receipt.writes_run_receipt: Detected receipt write (line {', '.join(map(str, receipt_lines))})")
            self.add_evidence(f"logging_and_receipt.run_receipt_bucket: {receipt_bucket}")
            self.add_evidence(f"logging_and_receipt.run_receipt_key_pattern: {receipt_pattern}")
        else:
            self.add_evidence(f"logging_and_receipt.writes_run_receipt: No receipt write detected (no S3 put_object with 'receipt' in key)")
        
        self.add_evidence(f"logging_and_receipt.counters_observed: No structured counters detected (would need runtime analysis)")
        
        return result
    
    def detect_config_files(self) -> List[Dict]:
        """Detect config file reads."""
        config_files = []
        reads, _ = self.find_s3_operations()
        
        for read in reads:
            key = read.get('key', '')
            if key and ('config' in key.lower() or 'configuration' in key.lower()):
                config_files.append({
                    'bucket': read.get('bucket'),
                    'key_pattern': key,
                    'format': 'json' if '.json' in key.lower() else 'TBD',
                    'required': True,  # Conservative default
                    'repo_path': None,
                    'line': read['line']
                })
        
        if config_files:
            self.add_evidence(f"config_files: Detected {len(config_files)} config file references")
        
        return config_files
    
    def generate_manifest(self, job_id_override: Optional[str] = None) -> Dict:
        """Generate complete manifest."""
        job_id = self.extract_job_id(job_id_override)
        runtime = self.extract_runtime()
        parameters = self.extract_parameters()
        
        reads, writes = self.find_s3_operations()
        
        # Convert reads to inputs
        inputs = []
        for read in reads:
            # Skip config files (will be in separate section)
            key = read.get('key', '')
            if key and ('config' in key.lower() or 'configuration' in key.lower()):
                continue
            
            inputs.append({
                'bucket': read.get('bucket', 'TBD'),
                'key_pattern': read.get('key', 'TBD'),
                'format': read.get('format', 'TBD'),
                'required': True
            })
        
        # Convert writes to outputs
        outputs = []
        for write in writes:
            # Skip receipts (will be in logging_and_receipt section)
            key = write.get('key', '')
            if key and 'receipt' in key.lower():
                continue
            
            # Detect format from write method or key extension
            format_type = 'TBD'
            if '.json' in key.lower():
                format_type = 'ndjson'  # Default for Spark/Glue
            elif '.csv' in key.lower():
                format_type = 'csv'
            
            outputs.append({
                'bucket': write.get('bucket', 'TBD'),
                'key_pattern': write.get('key', 'TBD'),
                'format': format_type,
                'required': True
            })
        
        side_effects = self.detect_side_effects()
        receipt_info = self.detect_receipt_and_counters()
        config_files = self.detect_config_files()
        
        manifest = {
            'job_id': job_id,
            'glue_job_name': job_id,  # Simple rule: equals job_id
            'runtime': runtime,
            'entrypoint': 'glue_script.py',
            'parameters': parameters if parameters else [],
            'inputs': inputs if inputs else [],
            'outputs': outputs if outputs else [],
            'side_effects': side_effects,
            'logging_and_receipt': receipt_info,
            'notes': self.evidence
        }
        
        # Add config_files only if found
        if config_files:
            manifest['config_files'] = config_files
        
        return manifest


def write_manifest_yaml(manifest: Dict, output_path: Path):
    """Write manifest to YAML file with proper formatting."""
    
    # Custom YAML representer for None/null values
    def represent_none(self, data):
        return self.represent_scalar('tag:yaml.org,2002:null', 'null')
    
    yaml.add_representer(type(None), represent_none)
    
    # Write with nice formatting
    with output_path.open('w') as f:
        # Manual formatting for better control
        f.write(f"job_id: {manifest['job_id']}\n")
        f.write(f"glue_job_name: {manifest['glue_job_name']}\n")
        f.write(f"runtime: {manifest['runtime']}\n")
        f.write(f"entrypoint: {manifest['entrypoint']}\n\n")
        
        # Parameters
        f.write("parameters:\n")
        if manifest['parameters']:
            for param in manifest['parameters']:
                f.write(f"  - {param}\n")
        else:
            f.write("  []\n")
        f.write("\n")
        
        # Inputs
        f.write("inputs:\n")
        if manifest['inputs']:
            for inp in manifest['inputs']:
                f.write(f"  - bucket: {inp['bucket']}\n")
                f.write(f"    key_pattern: {inp['key_pattern']}\n")
                f.write(f"    format: {inp['format']}\n")
                f.write(f"    required: {str(inp['required']).lower()}\n")
        else:
            f.write("  []\n")
        f.write("\n")
        
        # Outputs
        f.write("outputs:\n")
        if manifest['outputs']:
            for out in manifest['outputs']:
                f.write(f"  - bucket: {out['bucket']}\n")
                f.write(f"    key_pattern: {out['key_pattern']}\n")
                f.write(f"    format: {out['format']}\n")
                f.write(f"    required: {str(out['required']).lower()}\n")
        else:
            f.write("  []\n")
        f.write("\n")
        
        # Config files (if any)
        if 'config_files' in manifest and manifest['config_files']:
            f.write("config_files:\n")
            for cfg in manifest['config_files']:
                f.write(f"  - bucket: {cfg['bucket']}\n")
                f.write(f"    key_pattern: {cfg['key_pattern']}\n")
                f.write(f"    format: {cfg['format']}\n")
                f.write(f"    required: {str(cfg['required']).lower()}\n")
                f.write(f"    repo_path: {cfg['repo_path']}\n")
            f.write("\n")
        
        # Side effects
        f.write("side_effects:\n")
        f.write(f"  deletes_inputs: {str(manifest['side_effects']['deletes_inputs']).lower()}\n")
        f.write(f"  overwrites_outputs: {str(manifest['side_effects']['overwrites_outputs']).lower()}\n")
        f.write("\n")
        
        # Logging and receipt
        f.write("logging_and_receipt:\n")
        lr = manifest['logging_and_receipt']
        f.write(f"  writes_run_receipt: {str(lr['writes_run_receipt']).lower()}\n")
        f.write(f"  run_receipt_bucket: {lr['run_receipt_bucket']}\n")
        f.write(f"  run_receipt_key_pattern: {lr['run_receipt_key_pattern']}\n")
        
        f.write("  counters_observed:")
        if lr['counters_observed']:
            f.write("\n")
            for counter in lr['counters_observed']:
                f.write(f"    - {counter}\n")
        else:
            f.write(" []\n")
        f.write("\n")
        
        # Notes
        f.write("notes:\n")
        if manifest['notes']:
            for note in manifest['notes']:
                # Escape quotes in notes
                escaped_note = note.replace('"', '\\"')
                f.write(f'  - "{escaped_note}"\n')
        else:
            f.write("  []\n")


def main():
    parser = argparse.ArgumentParser(
        description="Manifest Generator - Extract job manifest from glue_script.py",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate new manifest
  python generate.py --script jobs/vendor_input_processing/newJob/glue_script.py
  
  # Generate with custom output path
  python generate.py --script path/to/glue_script.py --output path/to/manifest.yaml
  
  # Update existing manifest (preserves manual edits)
  python generate.py --script path/to/glue_script.py --update path/to/existing_manifest.yaml
        """
    )
    
    parser.add_argument('--script', required=True, help='Path to glue_script.py to analyze')
    parser.add_argument('--output', help='Output path for new manifest (default: same dir as script)')
    parser.add_argument('--update', help='Path to existing manifest to update')
    parser.add_argument('--job-id', help='Override job_id (default: parent folder name)')
    parser.add_argument('--verbose', action='store_true', help='Print detailed analysis')
    
    args = parser.parse_args()
    
    script_path = Path(args.script)
    if not script_path.exists():
        print(f"Error: Script not found: {script_path}", file=sys.stderr)
        sys.exit(1)
    
    # Determine output path
    if args.update:
        output_path = Path(args.update)
        print(f"Warning: --update mode not yet implemented. Generating new manifest instead.", file=sys.stderr)
    elif args.output:
        output_path = Path(args.output)
    else:
        output_path = script_path.parent / 'job_manifest.yaml'
    
    print(f"Analyzing: {script_path}")
    print(f"Output to: {output_path}")
    print()
    
    # Extract manifest
    extractor = ManifestExtractor(str(script_path), verbose=args.verbose)
    manifest = extractor.generate_manifest(job_id_override=args.job_id)
    
    # Write output
    write_manifest_yaml(manifest, output_path)
    
    print(f"\n✓ Manifest generated: {output_path}")
    print(f"  - job_id: {manifest['job_id']}")
    print(f"  - runtime: {manifest['runtime']}")
    print(f"  - parameters: {len(manifest['parameters'])} found")
    print(f"  - inputs: {len(manifest['inputs'])} found")
    print(f"  - outputs: {len(manifest['outputs'])} found")
    print(f"  - evidence notes: {len(manifest['notes'])} added")
    print()
    print("⚠️  Review and edit the generated manifest:")
    print("   - Resolve any TBD values")
    print("   - Verify extracted patterns match actual behavior")
    print("   - Add business context to notes section")
    print()


if __name__ == '__main__':
    main()
