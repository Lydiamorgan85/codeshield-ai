"""
Detector for Cross-Site Scripting (XSS) vulnerabilities in Python code.
Catches unsafe HTML output and unescaped user input in web applications.
"""

import re
from typing import List, Dict

class XSSDetector:
    """Detects XSS vulnerabilities in Python web application code."""
    
    def __init__(self):
        self.findings = []
    
    def scan(self, code: str, filename: str = "unknown") -> List[Dict]:
        self.findings = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            if line.strip().startswith('#'):
                continue
            
            stripped = line.strip()
            
            # Pattern 1: f-string with HTML tags
            if re.search(r'f["\'].*<[^>]+>.*\{', stripped):
                self.findings.append({
                    'file': filename,
                    'line': line_num,
                    'column': 1,
                    'vulnerability': 'XSS (Cross-Site Scripting)',
                    'severity': 'HIGH',
                    'message': 'HTML output using f-string with user input. This is vulnerable to XSS attacks.',
                    'code_snippet': stripped,
                    'recommendation': 'Use template engines with auto-escaping (Jinja2, Django templates) or manually escape with html.escape() or markupsafe.escape()'
                })
            
            # Pattern 2: % formatting with HTML tags
            elif re.search(r'["\'].*<[^>]+>.*%s.*["\'].*%', stripped):
                self.findings.append({
                    'file': filename,
                    'line': line_num,
                    'column': 1,
                    'vulnerability': 'XSS (Cross-Site Scripting)',
                    'severity': 'HIGH',
                    'message': 'HTML output using % formatting with user input. This is vulnerable to XSS attacks.',
                    'code_snippet': stripped,
                    'recommendation': 'Use template engines with auto-escaping or manually escape with html.escape()'
                })
            
            # Pattern 3: .format() with HTML tags
            elif re.search(r'["\'].*<[^>]+>.*\{.*\}.*["\'].*\.format\(', stripped):
                self.findings.append({
                    'file': filename,
                    'line': line_num,
                    'column': 1,
                    'vulnerability': 'XSS (Cross-Site Scripting)',
                    'severity': 'HIGH',
                    'message': 'HTML output using .format() with user input. This is vulnerable to XSS attacks.',
                    'code_snippet': stripped,
                    'recommendation': 'Use template engines with auto-escaping or manually escape with html.escape()'
                })
            
            # Pattern 4: String concatenation with HTML tags and variable
            elif '<' in stripped and '>' in stripped and '+' in stripped and '=' in stripped:
                if re.search(r'["\']<[^>]+>["\'].*\+', stripped) or re.search(r'\+.*["\']<[^>]+>["\']', stripped):
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': 1,
                        'vulnerability': 'XSS (Cross-Site Scripting)',
                        'severity': 'HIGH',
                        'message': 'HTML output using string concatenation. This is vulnerable to XSS attacks.',
                        'code_snippet': stripped,
                        'recommendation': 'Use template engines with auto-escaping or manually escape with html.escape()'
                    })
        
        return self.findings
    
    def get_summary(self) -> Dict:
        return {
            'total_issues': len(self.findings),
            'high_severity': len([f for f in self.findings if f['severity'] == 'HIGH']),
            'files_scanned': len(set(f['file'] for f in self.findings))
        }