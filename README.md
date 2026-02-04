
# CodeShield AI - Security Scanner for AI-Generated Code

**Stop AI coding tools from introducing critical vulnerabilities into your codebase.**

## The Problem

AI coding assistants like GitHub Copilot, Cursor, and ChatGPT are revolutionizing development speed - but at what cost?

- **45% of AI-generated code contains security vulnerabilities** (Veracode 2025)
- **Java applications have 72% security failure rates** with AI code
- **SQL injection vulnerabilities are 1.88x more likely** in AI-generated code
- **XSS attacks are 2.74x more common** when AI writes your frontend
- **Microsoft patched 1,139 CVEs in 2025** - AI bugs are becoming more prevalent

AI doesn't understand your security context. It replicates patterns from public repos - including vulnerable ones.

## The Solution

CodeShield AI automatically scans Python code for the most dangerous vulnerabilities AI assistants introduce:

### What It Detects

**Critical Vulnerabilities:**
- SQL Injection (4 attack patterns)
- Cross-Site Scripting / XSS (4 injection methods)
- Code Injection (eval, exec, compile)
- Unsafe Dynamic Imports

**Detection Accuracy:**
- 16 vulnerability patterns
- Zero false negatives on test suite
- Actionable fix recommendations for every issue

## Why CodeShield AI?

### Built for the AI Coding Era

Traditional SAST tools weren't designed for AI-generated code patterns. CodeShield AI specifically targets:

- F-string SQL injection
- Template literal XSS
- Dynamic eval() usage
- Unsafe string concatenation in queries

### Fast & Lightweight

- Scans 1000+ lines of code in under 1 second
- No external dependencies or cloud API calls
- Runs locally in your CI/CD pipeline
- Works offline

### Designed for DevOps

- Exit codes for CI/CD integration
- Structured JSON output (coming soon)
- Scan entire directories recursively
- Integrates with GitHub Actions (coming soon)

## Installation
```bash
git clone https://github.com/Lydiamorgan85/codeshield-ai.git
cd codeshield-ai
pip install -r requirements.txt
```

## Usage

**Scan a single file:**
```bash
python run_scan.py
```

**Example Output:**
```
CODESHIELD AI - SECURITY SCAN REPORT
================================================================================

File: examples/vulnerable_code.py
   Found 16 issue(s)

   Issue #1:
   |- Line 32, Column 1
   |- Severity: CRITICAL
   |- Vulnerability: SQL Injection
   |- Message: SQL query using string concatenation (+). This is vulnerable to SQL injection.
   |- Code: query = "SELECT * FROM users WHERE id = '" + user_id + "'"
   |- Fix: Use parameterized queries or prepared statements instead.

================================================================================
SUMMARY
================================================================================
Total Issues: 16
Files Scanned: 1
High/Critical Severity: 16
================================================================================
```

## Real-World Impact

**Before CodeShield AI:**
- Developers trust AI-generated code blindly
- SQL injection vulnerabilities reach production
- Security reviews catch issues too late
- Remediation costs 10x more post-deployment

**After CodeShield AI:**
- Catch vulnerabilities at commit time
- Prevent security debt accumulation
- Educate developers with actionable fixes
- Ship faster without sacrificing security

## Roadmap

- [ ] GitHub Action for automated PR scanning
- [ ] JSON output format for CI/CD integration
- [ ] JavaScript/TypeScript support
- [ ] Hardcoded secrets detection
- [ ] OWASP Top 10 coverage expansion
- [ ] VS Code extension
- [ ] Custom rule configuration

## Contributing

Issues and PRs welcome. See CONTRIBUTING.md (coming soon).

## Research References

This tool is built on security research showing AI code vulnerabilities:

- Veracode 2025 GenAI Code Security Report
- Cloud Security Alliance: Understanding Security Risks in AI-Generated Code
- CodeRabbit 2025: State of AI vs Human Code Generation
- University of Naples: Human-Written vs AI-Generated Code Study

## License

MIT License - see LICENSE file

## Author

Built by [@Lydiamorgan85](https://github.com/Lydiamorgan85)

**Securing the AI coding revolution, one scan at a time.**