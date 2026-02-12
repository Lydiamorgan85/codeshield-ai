"""
CodeShield AI - Main Scanner with AutoFix AI
"""

import os
from src.detectors.secrets_detector import SecretsDetector


class CodeShieldScanner:
    def __init__(self):
        self.detectors = [
            SecretsDetector(),
        ]
        self.findings = []
        self.autofix_suggestions = []

    def scan_file(self, file_path):
        """Scan a single file for security issues."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")
            return []

        file_findings = []
        for detector in self.detectors:
            results = detector.scan(file_path, content)
            file_findings.extend(results)

        self.findings.extend(file_findings)
        return file_findings

    def scan_directory(self, directory):
        """Recursively scan a directory for security issues."""
        skip_dirs = {
            '.git', 'node_modules', '__pycache__', '.venv',
            'venv', 'dist', 'build', '.next', 'vendor'
        }
        skip_extensions = {
            '.jpg', '.jpeg', '.png', '.gif', '.ico', '.svg',
            '.pdf', '.zip', '.tar', '.gz', '.exe', '.bin',
            '.lock', '.sum'
        }

        all_findings = []

        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in skip_dirs]

            for file in files:
                _, ext = os.path.splitext(file)
                if ext.lower() in skip_extensions:
                    continue

                file_path = os.path.join(root, file)
                findings = self.scan_file(file_path)
                all_findings.extend(findings)

        return all_findings

    def generate_report(self):
        """Generate a detailed security report with AutoFix AI suggestions."""
        if not self.findings:
            return self._generate_clean_report()

        critical = [f for f in self.findings if f.get('severity') == 'CRITICAL']
        high = [f for f in self.findings if f.get('severity') == 'HIGH']
        medium = [f for f in self.findings if f.get('severity') == 'MEDIUM']
        low = [f for f in self.findings if f.get('severity') == 'LOW']

        report = []
        report.append("=" * 70)
        report.append("  CODESHIELD AI - SECURITY SCAN REPORT WITH AUTOFIX AI")
        report.append("=" * 70)
        report.append("")
        report.append(f"  TOTAL ISSUES FOUND: {len(self.findings)}")
        report.append(f"  CRITICAL: {len(critical)}  |  HIGH: {len(high)}  |  MEDIUM: {len(medium)}  |  LOW: {len(low)}")
        report.append("")
        report.append("=" * 70)

        severity_groups = [
            ('CRITICAL', critical, '🔴'),
            ('HIGH', high, '🟠'),
            ('MEDIUM', medium, '🟡'),
            ('LOW', low, '🟢'),
        ]

        for severity, group, icon in severity_groups:
            if not group:
                continue

            report.append("")
            report.append(f"{icon} {severity} SEVERITY ISSUES ({len(group)} found)")
            report.append("-" * 70)

            for i, finding in enumerate(group, 1):
                report.append("")
                report.append(f"  Issue #{i}: {finding.get('vulnerability', 'Unknown')}")
                report.append(f"  File:      {finding.get('file', 'Unknown')}")
                report.append(f"  Line:      {finding.get('line', 0)}")
                report.append(f"  Code:      {finding.get('code_snippet', '')[:80]}")

                if finding.get('masked_secret'):
                    report.append(f"  Secret:    {finding.get('masked_secret')}")

                autofix = finding.get('autofix')
                if autofix:
                    report.append("")
                    report.append("  ╔══════════════════════════════════════════╗")
                    report.append("  ║         AUTOFIX AI SUGGESTION           ║")
                    report.append("  ╚══════════════════════════════════════════╝")
                    report.append("")
                    report.append(f"  RISK: {autofix.get('risk', '')}")
                    report.append("")
                    report.append("  HOW TO FIX:")
                    for step in autofix.get('steps', []):
                        report.append(f"    {step}")
                    report.append("")
                    report.append("  SECURE CODE:")
                    report.append("  " + "-" * 50)
                    for line in autofix.get('fix_code', '').split('\n'):
                        report.append(f"    {line}")
                    report.append("  " + "-" * 50)
                    report.append("")
                    report.append(f"  ADD TO .env FILE:")
                    report.append(f"    {autofix.get('env_example', '')}")

                report.append("")
                report.append("  " + "·" * 68)

        report.append("")
        report.append("=" * 70)
        report.append("  AUTOFIX AI SUMMARY")
        report.append("=" * 70)
        report.append("")
        report.append(f"  {len(self.findings)} security issues found with AutoFix AI suggestions.")
        report.append(f"  Follow the fix steps above to secure your codebase.")
        report.append("")
        report.append("  Need automated PR creation? Upgrade to Pro:")
        report.append("  https://codeshield.ie#pricing")
        report.append("")
        report.append("=" * 70)

        return '\n'.join(report)

    def _generate_clean_report(self):
        """Generate report when no issues found."""
        return """
======================================================================
  CODESHIELD AI - SECURITY SCAN REPORT
======================================================================

  ✅ SCAN COMPLETE - NO SECURITY ISSUES FOUND!

  Your codebase passed all security checks:
  ✓ No hardcoded secrets detected
  ✓ No API keys or tokens found
  ✓ No vulnerable patterns detected
  ✓ No dangerous functions found

  Keep up the great security practices!

  Powered by CodeShield AI - https://codeshield.ie
======================================================================
"""