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

# VULNERABILITY 5: SQL Injection with string concatenation
def get_user_by_id_unsafe(user_id):
    """Dangerous: SQL injection via string concatenation"""
    query = "SELECT * FROM users WHERE id = '" + user_id + "'"  # CRITICAL RISK!
    return query

# VULNERABILITY 6: SQL Injection with % formatting
def get_user_by_name_unsafe(username):
    """Dangerous: SQL injection via % formatting"""
    query = "SELECT * FROM users WHERE name = '%s'" % username  # CRITICAL RISK!
    return query

# VULNERABILITY 7: SQL Injection with f-string
def delete_user_unsafe(user_id):
    """Dangerous: SQL injection via f-string"""
    query = f"DELETE FROM users WHERE id = {user_id}"  # CRITICAL RISK!
    return query

# VULNERABILITY 8: SQL Injection with .format()
def update_user_unsafe(user_id, new_name):
    """Dangerous: SQL injection via .format()"""
    query = "UPDATE users SET name = '{}' WHERE id = {}".format(new_name, user_id)  # CRITICAL RISK!
    return query

# Example of SAFE code (this should NOT trigger warnings)
def safe_calculation(a, b):
    """This is safe - no dangerous functions"""
    return a + b

def safe_sql_query(user_id):
    """This is safe - using parameterized queries"""
    # This would be safe if executed with proper parameters:
    # cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return "SELECT * FROM users WHERE id = ?"

if __name__ == "__main__":
    print("This file contains vulnerable code for testing purposes only!")