"""
Secrets detector for CodeShield AI.
Detects hardcoded secrets and provides AutoFix AI suggestions.
"""

import re


class SecretsDetector:
    def __init__(self):
        self.patterns = [
            {
                'name': 'AWS Access Key',
                'pattern': r'AKIA[0-9A-Z]{16}',
                'severity': 'CRITICAL',
                'description': 'Hardcoded AWS Access Key detected',
                'env_var': 'AWS_ACCESS_KEY_ID',
            },
            {
                'name': 'AWS Secret Key',
                'pattern': r'(?i)aws.{0,20}secret.{0,20}["\']([A-Za-z0-9/+=]{40})["\']',
                'severity': 'CRITICAL',
                'description': 'Hardcoded AWS Secret Key detected',
                'env_var': 'AWS_SECRET_ACCESS_KEY',
            },
            {
                'name': 'GitHub Token',
                'pattern': r'ghp_[A-Za-z0-9]{36}',
                'severity': 'CRITICAL',
                'description': 'Hardcoded GitHub Personal Access Token detected',
                'env_var': 'GITHUB_TOKEN',
            },
            {
                'name': 'Stripe Live Secret Key',
                'pattern': r'sk_live_[A-Za-z0-9]{24,}',
                'severity': 'CRITICAL',
                'description': 'Hardcoded Stripe Live Secret Key detected',
                'env_var': 'STRIPE_SECRET_KEY',
            },
            {
                'name': 'Stripe Live Public Key',
                'pattern': r'pk_live_[A-Za-z0-9]{24,}',
                'severity': 'HIGH',
                'description': 'Hardcoded Stripe Live Public Key detected',
                'env_var': 'STRIPE_PUBLIC_KEY',
            },
            {
                'name': 'OpenAI API Key',
                'pattern': r'sk-[A-Za-z0-9]{48}',
                'severity': 'CRITICAL',
                'description': 'Hardcoded OpenAI API Key detected',
                'env_var': 'OPENAI_API_KEY',
            },
            {
                'name': 'Google API Key',
                'pattern': r'AIza[0-9A-Za-z\-_]{35}',
                'severity': 'HIGH',
                'description': 'Hardcoded Google API Key detected',
                'env_var': 'GOOGLE_API_KEY',
            },
            {
                'name': 'Slack Token',
                'pattern': r'xox[baprs]-[A-Za-z0-9\-]{10,}',
                'severity': 'HIGH',
                'description': 'Hardcoded Slack Token detected',
                'env_var': 'SLACK_TOKEN',
            },
            {
                'name': 'Private Key',
                'pattern': r'-----BEGIN (RSA |EC |PGP )?PRIVATE KEY-----',
                'severity': 'CRITICAL',
                'description': 'Private key found in source code',
                'env_var': 'PRIVATE_KEY',
            },
            {
                'name': 'Database URL',
                'pattern': r'(postgres|mysql|mongodb)://[A-Za-z0-9]+:[A-Za-z0-9@#$%^&+=]{8,}@',
                'severity': 'CRITICAL',
                'description': 'Hardcoded database connection string with credentials detected',
                'env_var': 'DATABASE_URL',
            },
            {
                'name': 'Generic Password',
                'pattern': r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']{6,}["\']',
                'severity': 'HIGH',
                'description': 'Hardcoded password detected',
                'env_var': 'APP_PASSWORD',
            },
            {
                'name': 'Generic API Key',
                'pattern': r'(?i)(api_key|apikey|api-key)\s*=\s*["\'][^"\']{10,}["\']',
                'severity': 'HIGH',
                'description': 'Hardcoded API key detected',
                'env_var': 'API_KEY',
            },
            {
                'name': 'JWT Token',
                'pattern': r'eyJ[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_.+/=]*',
                'severity': 'HIGH',
                'description': 'Hardcoded JWT token detected',
                'env_var': 'JWT_TOKEN',
            },
        ]

    def _mask_secret(self, secret):
        if len(secret) <= 8:
            return '*' * len(secret)
        return secret[:4] + '*' * (len(secret) - 8) + secret[-4:]

    def _generate_autofix(self, pattern_info, code_snippet, language):
        """Generate AutoFix AI suggestion based on language and issue type."""
        env_var = pattern_info['env_var']
        name = pattern_info['name']

        fixes = {
            'python': {
                'import': 'import os',
                'fix': f"os.environ.get('{env_var}')",
                'env_example': f"{env_var}=your_{env_var.lower()}_here",
                'full_example': f"import os\n\n# Load from environment variable\n{env_var.lower()} = os.environ.get('{env_var}')\nif not {env_var.lower()}:\n    raise ValueError('{env_var} environment variable not set')",
            },
            'javascript': {
                'import': '',
                'fix': f"process.env.{env_var}",
                'env_example': f"{env_var}=your_{env_var.lower()}_here",
                'full_example': f"// Load from environment variable\nconst {env_var.lower()} = process.env.{env_var};\nif (!{env_var.lower()}) {{\n  throw new Error('{env_var} environment variable not set');\n}}",
            },
            'typescript': {
                'import': '',
                'fix': f"process.env.{env_var}",
                'env_example': f"{env_var}=your_{env_var.lower()}_here",
                'full_example': f"// Load from environment variable\nconst {env_var.lower()}: string = process.env.{env_var} ?? '';\nif (!{env_var.lower()}) {{\n  throw new Error('{env_var} environment variable not set');\n}}",
            },
            'ruby': {
                'import': '',
                'fix': f"ENV['{env_var}']",
                'env_example': f"{env_var}=your_{env_var.lower()}_here",
                'full_example': f"# Load from environment variable\n{env_var.downcase} = ENV['{env_var}']\nraise '{env_var} environment variable not set' if {env_var.downcase}.nil?",
            },
            'go': {
                'import': 'import "os"',
                'fix': f'os.Getenv("{env_var}")',
                'env_example': f"{env_var}=your_{env_var.lower()}_here",
                'full_example': f'import "os"\n\n// Load from environment variable\n{env_var.lower()} := os.Getenv("{env_var}")\nif {env_var.lower()} == "" {{\n    panic("{env_var} environment variable not set")\n}}',
            },
            'php': {
                'import': '',
                'fix': f"$_ENV['{env_var}']",
                'env_example': f"{env_var}=your_{env_var.lower()}_here",
                'full_example': f"// Load from environment variable\n${env_var.lower()} = $_ENV['{env_var}'] ?? getenv('{env_var}');\nif (!${env_var.lower()}) {{\n    throw new RuntimeException('{env_var} environment variable not set');\n}}",
            },
        }

        lang_fix = fixes.get(language, fixes['python'])

        return {
            'issue': f'Hardcoded {name} found in source code',
            'risk': f'This secret could be exposed if your repository becomes public or is accessed by unauthorised users. Attackers actively scan GitHub for exposed credentials.',
            'fix_code': lang_fix['full_example'],
            'env_example': lang_fix['env_example'],
            'steps': [
                f"1. Remove the hardcoded value from your code",
                f"2. Add {env_var}=your_value to your .env file",
                f"3. Add .env to your .gitignore file",
                f"4. Use {lang_fix['fix']} in your code instead",
                f"5. Add {lang_fix['env_example']} to your .env.example file (without the real value)",
            ]
        }

    def _detect_language(self, file_path):
        """Detect programming language from file extension."""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.rb': 'ruby',
            '.go': 'go',
            '.php': 'php',
            '.java': 'java',
            '.cs': 'csharp',
            '.cpp': 'cpp',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.env': 'env',
        }
        for ext, lang in ext_map.items():
            if file_path.endswith(ext):
                return lang
        return 'python'

    def _is_false_positive(self, match, line):
        """Filter out common false positives."""
        false_positive_indicators = [
            'example', 'sample', 'test', 'dummy', 'fake',
            'placeholder', 'your_', 'xxx', '123456', 'changeme',
            'TODO', 'FIXME', 'replace_me'
        ]
        line_lower = line.lower()
        for indicator in false_positive_indicators:
            if indicator in line_lower:
                return True
        return False

    def scan(self, file_path, content):
        """Scan file content for secrets and generate AutoFix suggestions."""
        findings = []
        language = self._detect_language(file_path)
        lines = content.split('\n')

        for pattern_info in self.patterns:
            try:
                regex = re.compile(pattern_info['pattern'])
                for line_num, line in enumerate(lines, 1):
                    matches = regex.findall(line)
                    if matches:
                        match_str = matches[0] if isinstance(matches[0], str) else matches[0][0]
                        if self._is_false_positive(match_str, line):
                            continue

                        masked = self._mask_secret(match_str)
                        autofix = self._generate_autofix(pattern_info, line.strip(), language)

                        findings.append({
                            'file': file_path,
                            'line': line_num,
                            'column': line.find(match_str) + 1,
                            'severity': pattern_info['severity'],
                            'vulnerability': pattern_info['description'],
                            'code_snippet': line.strip()[:100],
                            'masked_secret': masked,
                            'recommendation': f"Replace hardcoded {pattern_info['name']} with environment variable {pattern_info['env_var']}",
                            'autofix': autofix,
                            'language': language,
                        })
            except re.error:
                continue

        return findings