"""
Secrets Detector for CodeShield
Detects hardcoded passwords, API keys, tokens, and other secrets
"""

import re
from typing import List, Dict

class SecretsDetector:
    def __init__(self):
        self.name = "Secrets Detector"
        self.severity = "CRITICAL"
        
        # Patterns for different types of secrets
        self.patterns = {
            'generic_secret': [
                r'password\s*=\s*["\']([^"\']{3,})["\']',
                r'pwd\s*=\s*["\']([^"\']{3,})["\']',
                r'passwd\s*=\s*["\']([^"\']{3,})["\']',
                r'api[_-]?key\s*=\s*["\']([^"\']{10,})["\']',
                r'secret\s*=\s*["\']([^"\']{10,})["\']',
                r'token\s*=\s*["\']([^"\']{10,})["\']',
                r'auth[_-]?token\s*=\s*["\']([^"\']{10,})["\']',
            ],
            'aws_key': [
                r'AKIA[0-9A-Z]{16}',
                r'aws[_-]?access[_-]?key[_-]?id\s*=\s*["\']([^"\']+)["\']',
                r'aws[_-]?secret[_-]?access[_-]?key\s*=\s*["\']([^"\']+)["\']',
            ],
            'github_token': [
                r'ghp_[a-zA-Z0-9]{36}',
                r'gho_[a-zA-Z0-9]{36}',
                r'github[_-]?token\s*=\s*["\']([^"\']+)["\']',
            ],
            'stripe_key': [
                r'sk_live_[a-zA-Z0-9]{24,}',
                r'pk_live_[a-zA-Z0-9]{24,}',
                r'stripe[_-]?key\s*=\s*["\']([^"\']+)["\']',
            ],
            'openai_key': [
                r'sk-[a-zA-Z0-9]{48}',
                r'openai[_-]?key\s*=\s*["\']([^"\']+)["\']',
            ],
            'google_api': [
                r'AIza[a-zA-Z0-9]{35}',
                r'google[_-]?api[_-]?key\s*=\s*["\']([^"\']+)["\']',
            ],
            'slack_token': [
                r'xox[baprs]-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24,}',
                r'slack[_-]?token\s*=\s*["\']([^"\']+)["\']',
            ],
            'private_key': [
                r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
                r'-----BEGIN PGP PRIVATE KEY BLOCK-----',
            ],
            'database_url': [
                r'postgresql://[^:]+:[^@]+@[^/]+/\w+',
                r'mysql://[^:]+:[^@]+@[^/]+/\w+',
                r'mongodb://[^:]+:[^@]+@[^/]+/\w+',
                r'postgres://[^:]+:[^@]+@[^/]+/\w+',
            ],
            'jwt_token': [
                r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}',
            ],
        }
        
        # Common false positives to ignore
        self.false_positives = [
            'password = ""',
            'password = \'\'',
            "password = 'your_password_here'",
            "password = 'changeme'",
            "password = 'password'",
            "password = '123456'",
            "api_key = 'YOUR_API_KEY'",
            "token = 'your_token_here'",
        ]
    
    def scan(self, code: str, filename: str = "") -> List[Dict]:
        """
        Scan code for hardcoded secrets
        
        Args:
            code: Source code to analyze
            filename: Name of the file being analyzed
            
        Returns:
            List of detected issues in CodeShield format
        """
        issues = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            # Skip comments
            if line.strip().startswith('#') or line.strip().startswith('//'):
                continue
            
            # Check if line contains common false positives
            if any(fp in line.lower() for fp in self.false_positives):
                continue
            
            # Check each pattern type
            for secret_type, patterns in self.patterns.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        # Extract the matched secret (mask it for display)
                        secret_value = match.group(0)
                        masked_value = self._mask_secret(secret_value)
                        
                        issues.append({
                            'file': filename,
                            'line': line_num,
                            'column': 0,
                            'severity': self.severity,
                            'vulnerability': secret_type.replace("_", " "),
                            'message': f'Hardcoded {secret_type.replace("_", " ")} detected: {masked_value}',
                            'code_snippet': line.strip(),
                            'recommendation': self._get_recommendation(secret_type),
                        })
        
        return issues
    
    def _mask_secret(self, secret: str) -> str:
        """Mask the secret value for safe display"""
        if len(secret) <= 8:
            return '*' * len(secret)
        return secret[:4] + '*' * (len(secret) - 8) + secret[-4:]
    
    def _get_recommendation(self, secret_type: str) -> str:
        """Get specific recommendation based on secret type"""
        recommendations = {
            'generic_secret': 'Store secrets in environment variables or a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)',
            'aws_key': 'Use AWS IAM roles and AWS Secrets Manager. Never commit AWS credentials to code.',
            'github_token': 'Use GitHub Actions secrets or environment variables. Rotate this token immediately if committed.',
            'stripe_key': 'Use environment variables for Stripe keys. Rotate this key immediately if exposed.',
            'openai_key': 'Store OpenAI API keys in environment variables. Rotate immediately if exposed.',
            'google_api': 'Use Google Cloud Secret Manager or environment variables for API keys.',
            'slack_token': 'Store Slack tokens in environment variables or secrets manager.',
            'private_key': 'NEVER commit private keys. Use SSH agent forwarding or secure key management systems.',
            'database_url': 'Use environment variables for database URLs. Connection strings contain sensitive credentials.',
            'jwt_token': 'JWT tokens should never be hardcoded. Generate them dynamically at runtime.',
        }
        return recommendations.get(secret_type, 'Store sensitive data in environment variables or a secrets management system.')