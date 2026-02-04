"""
Example code with security vulnerabilities for testing CodeShield AI.
WARNING: This code contains intentional security flaws - DO NOT USE IN PRODUCTION!
"""

# VULNERABILITY 1: Using eval() with user input
def calculate_user_input(user_formula):
    """Dangerous: eval() can execute arbitrary code"""
    result = eval(user_formula)  # HIGH RISK!
    return result

# VULNERABILITY 2: Using exec() to run dynamic code
def run_user_code(code_string):
    """Dangerous: exec() can execute any Python code"""
    exec(code_string)  # HIGH RISK!

# VULNERABILITY 3: Using compile() with untrusted input
def compile_user_function(user_code):
    """Dangerous: compile() with untrusted input"""
    compiled = compile(user_code, '<string>', 'exec')  # HIGH RISK!
    exec(compiled)

# VULNERABILITY 4: Dynamic imports
def import_user_module(module_name):
    """Dangerous: __import__ with user input"""
    module = __import__(module_name)  # HIGH RISK!
    return module

# Example of SAFE code (this should NOT trigger warnings)
def safe_calculation(a, b):
    """This is safe - no dangerous functions"""
    return a + b

if __name__ == "__main__":
    print("This file contains vulnerable code for testing purposes only!")