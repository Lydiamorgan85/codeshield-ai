"""
Simple script to run CodeShield AI scanner.
Works both standalone and as a GitHub Action.
"""

import sys
import os
from src.scanner import CodeShieldScanner

def main():
    print("Starting CodeShield AI Scanner...\n")
    
    scanner = CodeShieldScanner()
    
    # Get target from command line or environment variable
    target = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('INPUT_TARGET', 'examples/vulnerable_code.py')
    
    # Determine if we should fail on issues
    fail_on_issues = os.environ.get('INPUT_FAIL-ON-ISSUES', 'true').lower() == 'true'
    
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
    
    # Set GitHub Action outputs if running in GitHub Actions
    if os.environ.get('GITHUB_ACTIONS'):
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"issues-found={len(findings)}\n")
                critical = len([i for i in findings if i.get('severity') in ['HIGH', 'CRITICAL']])
                f.write(f"severity-critical={critical}\n")
    
    # Exit with error code if issues found and fail_on_issues is true
    if findings and fail_on_issues:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()