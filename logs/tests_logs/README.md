# Test Logs

This directory contains logs from automated test runs executed by the Testing Agent.

## Log Format

Each log file follows the naming convention: `test_run_YYYYMMDD_HHMMSS.log`

Example: `test_run_20260127_093000.log`

## Log Contents

Each log includes:

1. **Test Run Metadata**
   - Timestamp
   - Specification reference (if applicable)

2. **Test Results**
   - Repository validation tests
   - Python syntax checks
   - YAML syntax checks
   - Specification-based tests (if applicable)

3. **Summary**
   - Number of tests passed
   - Number of tests failed
   - Overall status

## Viewing Logs

### List recent logs:
```bash
python tools/testing_agent.py logs
```

### View a specific log:
```bash
cat logs/tests_logs/test_run_20260127_093000.log
```

### Via GitHub Actions:
Test logs are automatically uploaded as artifacts and can be downloaded from:
- Actions → Testing Agent Workflow → [specific run] → Artifacts → test-logs

## Retention

- **Local logs**: Kept indefinitely unless manually cleaned
- **GitHub Actions artifacts**: Retained for 30 days

## Automated Testing

Tests run automatically:
- On pull requests (for validation)
- On merge to main (with log generation)
- When manually triggered via Testing Agent Workflow

## Log Cleanup

To clean up old logs:
```bash
# Remove logs older than 90 days
find logs/tests_logs -name "*.log" -mtime +90 -delete
```

## Best Practices

1. Review logs after failed test runs
2. Keep logs for successful production deployments
3. Reference log timestamps in issue reports
4. Archive critical logs before cleanup

## Troubleshooting

If logs are not being generated:
1. Check that `logs/tests_logs/` directory exists
2. Ensure tests are run without `--no-log` flag
3. Verify write permissions on the directory
4. Check GitHub Actions workflow permissions
