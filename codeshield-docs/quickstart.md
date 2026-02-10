# Quick Start Guide

Get up and running with CodeShield AI in under 5 minutes.

## Installation

```bash
git clone https://github.com/Lydiamorgan85/codeshield-ai.git
cd codeshield-ai
npm install
```

## Your First Scan

### Analyze a Single File

```bash
npx codeshield analyze mycode.js
```

### Analyze Entire Project

```bash
npx codeshield analyze ./src
```

### Example Output

```
CodeShield AI Security Report
=============================

Found 3 vulnerabilities:

CRITICAL: Hardcoded API Key
  File: api.js:12
  Code: const apiKey = "sk-1234567890abcdef"
  Fix: Use environment variables

HIGH: SQL Injection Risk
  File: database.js:45
  Code: query = "SELECT * FROM users WHERE id = " + userId
  Fix: Use parameterized queries

MEDIUM: Weak Password Validation
  File: auth.js:23
  Code: password.length >= 6
  Fix: Enforce stronger password requirements

Total: 3 issues (1 critical, 1 high, 1 medium)
```

## Common Use Cases

### Pre-Commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/sh
npx codeshield analyze --staged --fail-on-critical
```

### CI/CD Pipeline

```yaml
# .github/workflows/security.yml
- name: Security Scan
  run: npx codeshield analyze ./src --output report.json
```

### IDE Integration

```bash
# Watch mode for real-time feedback
npx codeshield watch ./src
```

## What Gets Detected?

✅ Hardcoded credentials (API keys, passwords, tokens)  
✅ SQL injection vulnerabilities  
✅ XSS (Cross-Site Scripting) risks  
✅ Insecure authentication patterns  
✅ Exposed sensitive data  
✅ Deprecated/vulnerable dependencies  

## Configuration

Create `.codeshield.json`:

```json
{
  "severity": ["critical", "high"],
  "exclude": ["node_modules/**", "*.test.js"],
  "autoFix": false
}
```

## Next Steps

- [Full CLI Reference](cli-reference.md)
- [CI/CD Integration Guide](cicd-integration.md)
- [Custom Rules](custom-rules.md)

## Need Help?

- Check [Troubleshooting Guide](troubleshooting.md)
- Open an issue on GitHub
- Email: lydiamorgan000@gmail.com
