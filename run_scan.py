"""
Simple script to run CodeShield AI scanner.
"""

from src.scanner import CodeShieldScanner

def main():
    print("🛡️  Starting CodeShield AI Scanner...\n")
    
    scanner = CodeShieldScanner()
    
    # Scan the vulnerable example file
    findings = scanner.scan_file("examples/vulnerable_code.py")
    
    # Generate and print report
    report = scanner.generate_report()
    print(report)
    
    # Exit with error code if issues found
    if findings:
        exit(1)
    else:
        exit(0)

if __name__ == "__main__":
    main()