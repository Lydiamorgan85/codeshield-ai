"""
Detector for SQL injection vulnerabilities in Python code.
Catches unsafe database queries with string concatenation or formatting.
"""

import re
from typing import List, Dict

class SQLInjectionDetector:
    """Detects SQL injection vulnerabilities in Python code."""
    
    # Patterns that indicate SQL injection risks
    SQL_KEYWORDS = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'EXEC']
    
    def __init__(self):
        self.findings = []
    
    def scan(self, code: str, filename: str = "unknown") -> List[Dict]:
        self.findings = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            # Skip comments
            if line.strip().startswith('#'):
                continue
            
            # Check for SQL keywords in the line
            has_sql = any(keyword in line.upper() for keyword in self.SQL_KEYWORDS)
            
            if has_sql:
                # Pattern 1: String concatenation with +
                if re.search(r'["\'].*?(SELECT|INSERT|UPDATE|DELETE|DROP).*?["\'].*?\+', line, re.IGNORECASE):
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': 1,
                        'vulnerability': 'SQL Injection',
                        'severity': 'CRITICAL',
                        'message': 'SQL query using string concatenation (+). This is vulnerable to SQL injection.',
                        'code_snippet': line.strip(),
                        'recommendation': 'Use parameterized queries or prepared statements instead. Example: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))'
                    })
                
                # Pattern 2: String formatting with %
                elif re.search(r'["\'].*?(SELECT|INSERT|UPDATE|DELETE|DROP).*?%[sd]', line, re.IGNORECASE):
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': 1,
                        'vulnerability': 'SQL Injection',
                        'severity': 'CRITICAL',
                        'message': 'SQL query using % string formatting. This is vulnerable to SQL injection.',
                        'code_snippet': line.strip(),
                        'recommendation': 'Use parameterized queries instead. Example: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))'
                    })
                
                # Pattern 3: f-string with SQL
                elif re.search(r'f["\'].*?(SELECT|INSERT|UPDATE|DELETE|DROP).*?\{', line, re.IGNORECASE):
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': 1,
                        'vulnerability': 'SQL Injection',
                        'severity': 'CRITICAL',
                        'message': 'SQL query using f-string interpolation. This is vulnerable to SQL injection.',
                        'code_snippet': line.strip(),
                        'recommendation': 'Use parameterized queries instead. Example: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))'
                    })
                
                # Pattern 4: .format() with SQL
                elif re.search(r'["\'].*?(SELECT|INSERT|UPDATE|DELETE|DROP).*?["\'].*?\.format\(', line, re.IGNORECASE):
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': 1,
                        'vulnerability': 'SQL Injection',
                        'severity': 'CRITICAL',
                        'message': 'SQL query using .format() method. This is vulnerable to SQL injection.',
                        'code_snippet': line.strip(),
                        'recommendation': 'Use parameterized queries instead. Example: cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))'
                    })
        
        return self.findings
    
    def get_summary(self) -> Dict:
        return {
            'total_issues': len(self.findings),
            'critical_severity': len([f for f in self.findings if f['severity'] == 'CRITICAL']),
            'files_scanned': len(set(f['file'] for f in self.findings))
        }