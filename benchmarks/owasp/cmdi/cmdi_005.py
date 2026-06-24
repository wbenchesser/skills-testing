"""
Command Injection Test Case: shlex.quote() Sanitized Input
CWE-78: OS Command Injection
Expected: SAFE (False Positive Test)
"""

import subprocess
import shlex

def search_logs(search_term):
    """
    Search log files for a term.
    SAFE: Uses shlex.quote() to sanitize user input before shell execution.
    """
    # SAFE: shlex.quote() escapes shell metacharacters
    safe_term = shlex.quote(search_term)
    cmd = f"grep {safe_term} /var/log/app.log"

    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout
