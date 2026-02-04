"""
Detector for dangerous function usage in Python code.
Catches eval(), exec(), __import__(), compile(), and other risky functions.
"""

import re
from typing import List, Dict

class DangerousFunctionsDetector:
    """Detects usage of dangerous Python functions that can lead to code injection."""
    
    DANGEROUS_FUNCTIONS = [
        'eval',
        'exec',
        'compile',
        '__import__',
        'execfile',
        'input',
    ]
    
    def __init__(self):
        self.findings = []
    
    def scan(self, code: str, filename: str = "unknown") -> List[Dict]:
        self.findings = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            if line.strip().startswith('#'):
                continue
            
            for func in self.DANGEROUS_FUNCTIONS:
                pattern = rf'\b{func}\s*\('
                
                if re.search(pattern, line):
                    self.findings.append({
                        'file': filename,
                        'line': line_num,
                        'column': line.index(func) + 1,
                        'function': func,
                        'severity': 'HIGH',
                        'message': f"Dangerous function '{func}()' detected. This can lead to code injection vulnerabilities.",
                        'code_snippet': line.strip(),
                        'recommendation': self._get_recommendation(func)
                    })
        
        return self.findings
    
    def _get_recommendation(self, function: str) -> str:
        recommendations = {
            'eval': "Avoid eval(). Use ast.literal_eval() for safe evaluation of literals, or json.loads() for JSON data.",
            'exec': "Avoid exec(). Consider using specific functions or safer alternatives for your use case.",
            'compile': "Avoid compile() with untrusted input. Validate and sanitize all inputs first.",
            '__import__': "Use importlib.import_module() instead of __import__() for safer dynamic imports.",
            'execfile': "execfile() is removed in Python 3. Use exec(open(file).read()) only with trusted files.",
            'input': "In Python 2, input() uses eval(). Use raw_input() instead, or upgrade to Python 3."
        }
        return recommendations.get(function, "Review this function usage carefully and ensure input is validated.")
    
    def get_summary(self) -> Dict:
        return {
            'total_issues': len(self.findings),
            'high_severity': len([f for f in self.findings if f['severity'] == 'HIGH']),
            'files_scanned': len(set(f['file'] for f in self.findings))
        }