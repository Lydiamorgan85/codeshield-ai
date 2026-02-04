"""
Simple script to run CodeShield AI scanner.
Works both standalone and as a GitHub Action.
"""

import sys
import os
import urllib.request
import json
from src.scanner import CodeShieldScanner

def validate_license_lemonsqueezy(license_key):
    """
    Validate license key with LemonSqueezy API.
    Returns: (is_valid, plan_type)
    """
    if not license_key:
        return False, None
    
    try:
        url = f"https://api.lemonsqueezy.com/v1/licenses/validate"
        data = json.dumps({"license_key": license_key}).encode('utf-8')
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('valid'):
                product_name = result.get('meta', {}).get('product_name', '').lower()
                if 'team' in product_name:
                    return True, 'team'
                else:
                    return True, 'pro'
            
            return False, None
    
    except Exception as e:
        print(f"License validation warning: {e}")
        return False, None

def main():
    print("Starting CodeShield AI Scanner...\n")
    
    license_key = os.environ.get('INPUT_LICENSE-KEY', '')
    
    is_licensed, plan_type = validate_license_lemonsqueezy(license_key)
    
    if is_licensed:
        print(f"License validated: {plan_type.upper()} plan\n")
    else:
        print("Running in FREE mode (public repos only)\n")
    
    scanner = CodeShieldScanner()
    
    target = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('INPUT_TARGET', 'examples/vulnerable_code.py')
    
    fail_on_issues = os.environ.get('INPUT_FAIL-ON-ISSUES', 'true').lower() == 'true'
    
    is_private_repo = os.environ.get('GITHUB_REPOSITORY_PRIVATE', 'false').lower() == 'true'
    
    if is_private_repo and not is_licensed:
        print("\nERROR: Private repository scanning requires a Pro or Team license.")
        print("Get your license at: https://lydiamorgan85.github.io/codeshield-ai#pricing")
        print("\nTo use your license key, add it to your GitHub Action:")
        print("  - uses: Lydiamorgan85/codeshield-ai@v1.0.1")
        print("    with:")
        print("      license-key: ${{ secrets.CODESHIELD_LICENSE }}")
        sys.exit(1)
    
    if os.path.isfile(target):
        findings = scanner.scan_file(target)
    elif os.path.isdir(target):
        findings = scanner.scan_directory(target)
    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)
    
    report = scanner.generate_report()
    print(report)
    
    with open('codeshield-report.txt', 'w') as f:
        f.write(report)
    print("\nReport saved to: codeshield-report.txt")
    
    if os.environ.get('GITHUB_ACTIONS'):
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"issues-found={len(findings)}\n")
                critical = len([i for i in findings if i.get('severity') in ['HIGH', 'CRITICAL']])
                f.write(f"critical-issues={critical}\n")
                f.write(f"report-path=codeshield-report.txt\n")
    
    if fail_on_issues and findings:
        critical_count = len([i for i in findings if i.get('severity') in ['HIGH', 'CRITICAL']])
        if critical_count > 0:
            print(f"\nFailing build: Found {critical_count} critical security issues")
            sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main()