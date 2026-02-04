"""
Detector for Cross-Site Scripting (XSS) vulnerabilities in Python code.
Catches unsafe HTML output and unescaped user input in web applications.
"""

import re
from typing import List, Dict

class XSSDetector:
    """Detects XSS vulnerabilities in Python web application code."""
    
    # HTML output functions that can be unsafe
    HTML_OUTPUT_PATTERNS = [
        r'\.write\(',           # response.write()
        r'\.send\(',            # response.send()
        r'render_template_string\(',  # Flask
        r'HttpResponse\(',      # Django
        r'\.innerHTML',         # JavaScript-like
    ]
    
    # Unsafe HTML construction patterns
    UNSAFE_HTML_PATTERNS = [
        r'<[^>]*\{[^}]*\}[^>]*>',  # HTML tags with variable interpolation
        r'<[^>]*%s[^>]*>',          # HTML tags with % formatting
        r'<[^>]*\.format\(',        # HTML tags with .format()
    ]
    
    def __init__(self):
        self.findings = []
    
    def scan(self, code: str, filename: str = "unknown") -> List[Dict]:
        self.findings = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            # Skip comments
            if line.strip().startswith('#'):
                continue
            
            # Check for HTML tags in the line
            has_html = bool(re.search(r'<[a-zA-Z]+[^>]*>', line))
            
            if has_html:
                # Pattern 1: HTML with f-string interpolation
                if re.search(r'f["\'].*?<[^>]*\{.*?\}.*?>', line):
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': 1,
                        'vulnerability': 'XSS (Cross-Site Scripting)',
                        'severity': 'HIGH',
                        'message': 'HTML output using f-string with user input. This is vulnerable to XSS attacks.',
                        'code_snippet': line.strip(),
                        'recommendation': 'Use template engines with auto-escaping (Jinja2, Django templates) or manually escape with html.escape() or markupsafe.escape()'
                    })
                
                # Pattern 2: HTML with % formatting
                elif re.search(r'["\'].*?<[^>]*%[sd].*?>', line):
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': 1,
                        'vulnerability': 'XSS (Cross-Site Scripting)',
                        'severity': 'HIGH',
                        'message': 'HTML output using % formatting with user input. This is vulnerable to XSS attacks.',
                        'code_snippet': line.strip(),
                        'recommendation': 'Use template engines with auto-escaping or manually escape with html.escape()'
                    })
                
                # Pattern 3: HTML with .format()
                elif re.search(r'["\'].*?<[^>]*\{\}.*?>.*?\.format\(', line):
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': 1,
                        'vulnerability': 'XSS (Cross-Site Scripting)',
                        'severity': 'HIGH',
                        'message': 'HTML output using .format() with user input. This is vulnerable to XSS attacks.',
                        'code_snippet': line.strip(),
                        'recommendation': 'Use template engines with auto-escaping or manually escape with html.escape()'
                    })
                
                # Pattern 4: HTML with + concatenation
                elif re.search(r'<[^>]*["\'].*?\+', line) and 'html' in line.lower():
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': 1,
                        'vulnerability': 'XSS (Cross-Site Scripting)',
                        'severity': 'HIGH',
                        'message': 'HTML output using string concatenation. This is vulnerable to XSS attacks.',
                        'code_snippet': line.strip(),
                        'recommendation': 'Use template engines with auto-escaping or manually escape with html.escape()'
                    })
            
            # Pattern 5: render_template_string with variables (Flask specific)
            if 'render_template_string' in line and ('{' in line or '%' in line):
                self.findings.append({
                    'file': filename,
                    'line': line_num,
                    'column': 1,
                    'vulnerability': 'XSS (Cross-Site Scripting)',
                    'severity': 'HIGH',
                    'message': 'Using render_template_string with user input. This can lead to XSS or template injection.',
                    'code_snippet': line.strip(),
                    'recommendation': 'Use render_template() with separate template files and Jinja2 auto-escaping enabled'
                })
            
            # Pattern 6: HttpResponse with unescaped content (Django specific)
            if 'HttpResponse' in line and ('+' in line or '%' in line or 'format' in line or 'f"' in line or "f'" in line):
                if '<' in line or 'html' in line.lower():
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': 1,
                        'vulnerability': 'XSS (Cross-Site Scripting)',
                        'severity': 'HIGH',
                        'message': 'HttpResponse with dynamic HTML content. This is vulnerable to XSS attacks.',
                        'code_snippet': line.strip(),
                        'recommendation': 'Use Django templates with auto-escaping or django.utils.html.escape()'
                    })
        
        return self.findings
    
    def get_summary(self) -> Dict:
        return {
            'total_issues': len(self.findings),
            'high_severity': len([f for f in self.findings if f['severity'] == 'HIGH']),
            'files_scanned': len(set(f['file'] for f in self.findings))
        }