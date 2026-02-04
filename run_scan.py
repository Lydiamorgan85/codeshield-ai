"""
Simple script to run CodeShield AI scanner.
Works both standalone and as a GitHub Action.
"""

import sys
import os
from src.scanner import CodeShieldScanner

def validate_license(license_key):
    """
    Validate license key for Pro/Team features.
    Returns: (is_valid, plan_type)
    """
    if not license_key:
        return False, None
    
    # Simple validation for now (we'll improve this later)
    valid_keys = {
        # Pro keys
        'PRO-2026-DEMO-0001': 'pro',
        'PRO-2026-DEMO-0002': 'pro',
        # Team keys
        'TEAM-2026-DEMO-0001': 'team',
        'TEAM-2026-DEMO-0002': 'team',
    }
    
    if license_key in valid_keys:
        return True, valid_keys[license_key]
    
    return False, None

def main():
    print("Starting CodeShield AI Scanner...\n")
    
    # Get license key from environment variable
    license_key = os.environ.get('INPUT_LICENSE-KEY', '')
    
    # Validate license
    is_licensed, plan_type = validate_license(license_key)
    
    if is_licensed:
        print(f"License validated: {plan_type.upper()} plan\n")
    else:
        print("Running in FREE mode (public repos only)\n")
    
    scanner = CodeShieldScanner()
    
    # Get target from command line or environment variable
    target = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('INPUT_TARGET', 'examples/vulnerable_code.py')
    
    # Determine if we should fail on issues
    fail_on_issues = os.environ.get('INPUT_FAIL-ON-ISSUES', 'true').lower() == 'true'
    
    # Check if target is private repo (simplified check)
    is_private_repo = os.environ.get('GITHUB_REPOSITORY_PRIVATE', 'false').lower() == 'true'
    
    # Enforce license for private repos
    if is_private_repo and not is_licensed:
        print("\nERROR: Private repository scanning requires a Pro or Team license.")
        print("Get your license at: https://lydiamorgan85.github.io/codeshield-ai#pricing")
        print("\nTo use your license key, add it to your GitHub Action:")
        print("  - uses: Lydiamorgan85/codeshield-ai@v1.0.0")
        print("    with:")
        print("      license-key: ${{ secrets.CODESHIELD_LICENSE }}")
        sys.exit(1)
    
    # Scan file or directory
    if os.path.isfile(target):
        findings = scanner.scan_file(target)
    elif os.path.isdir(target):
        findings = scanner.scan_directory(target)
    else:
        print(f"Error: {target} is not a valid file or directory")
        sys.exit(1)
    
    # Generate and print report
    report = scanner.generate_report()
    print(report)
    
    # Write report to file
    with open('codeshield-report.txt', 'w') as f:
        f.write(report)
    print("\nReport saved to: codeshield-report.txt")
    
    # Set GitHub Action outputs if running in GitHub Actions
    if os.environ.get('GITHUB_ACTIONS'):
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"issues-found={len(findings)}\n")
                critical = len([i for i in findings if i.get('severity') in ['HIGH', 'CRITICAL']])
                f.write(f"critical-issues={critical}\n")
                f.write(f"report-path=codeshield-report.txt\n")
    
    # Exit with error if critical issues found and fail_on_issues is true
    if fail_on_issues and findings:
        critical_count = len([i for i in findings if i.get('severity') in ['HIGH', 'CRITICAL']])
        if critical_count > 0:
            print(f"\nFailing build: Found {critical_count} critical security issues")
            sys.exit(1)
    
    # Success
    sys.exit(0)

if __name__ == "__main__":
    main()