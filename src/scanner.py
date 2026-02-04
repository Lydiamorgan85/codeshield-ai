"""
Main scanner module for CodeShield AI.
Orchestrates all detectors and provides scanning functionality.
"""

from typing import List, Dict
import os
from src.detectors.dangerous_functions import DangerousFunctionsDetector
from src.detectors.sql_injection import SQLInjectionDetector

class CodeShieldScanner:
    """Main scanner that runs all security detectors."""
    
    def __init__(self):
        self.detectors = [
            DangerousFunctionsDetector(),
            SQLInjectionDetector(),
        ]
        self.all_findings = []
    
    def scan_file(self, filepath: str) -> List[Dict]:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()
        
        findings = []
        for detector in self.detectors:
            findings.extend(detector.scan(code, filepath))
        
        self.all_findings.extend(findings)
        return findings
    
    def scan_directory(self, directory: str, extensions: List[str] = None) -> List[Dict]:
        if extensions is None:
            extensions = ['.py']
        
        findings = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    filepath = os.path.join(root, file)
                    findings.extend(self.scan_file(filepath))
        
        return findings
    
    def generate_report(self) -> str:
        if not self.all_findings:
            return "✅ No security issues found!"
        
        report = []
        report.append("=" * 80)
        report.append("🛡️  CODESHIELD AI - SECURITY SCAN REPORT")
        report.append("=" * 80)
        report.append("")
        
        files = {}
        for finding in self.all_findings:
            filename = finding['file']
            if filename not in files:
                files[filename] = []
            files[filename].append(finding)
        
        for filename, findings in files.items():
            report.append(f"📄 File: {filename}")
            report.append(f"   Found {len(findings)} issue(s)")
            report.append("")
            
            for i, finding in enumerate(findings, 1):
                report.append(f"   Issue #{i}:")
                report.append(f"   ├─ Line {finding['line']}, Column {finding['column']}")
                report.append(f"   ├─ Severity: {finding['severity']}")
                
                # Handle both formats (function or vulnerability)
                if 'function' in finding:
                    report.append(f"   ├─ Function: {finding['function']}()")
                elif 'vulnerability' in finding:
                    report.append(f"   ├─ Vulnerability: {finding['vulnerability']}")
                
                report.append(f"   ├─ Message: {finding['message']}")
                report.append(f"   ├─ Code: {finding['code_snippet']}")
                report.append(f"   └─ Fix: {finding['recommendation']}")
                report.append("")
        
        report.append("=" * 80)
        report.append("📊 SUMMARY")
        report.append("=" * 80)
        report.append(f"Total Issues: {len(self.all_findings)}")
        report.append(f"Files Scanned: {len(files)}")
        report.append(f"High/Critical Severity: {len([f for f in self.all_findings if f['severity'] in ['HIGH', 'CRITICAL']])}")
        report.append("=" * 80)
        
        return "\n".join(report)