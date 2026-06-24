"""
Command Injection Test Case: subprocess.run() with List Arguments
CWE-78: OS Command Injection
Expected: SAFE (False Positive Test)
"""

import subprocess

def check_file_permissions(filepath):
    """
    Check file permissions using stat.
    SAFE: Uses list arguments with shell=False (default).
    """
    # SAFE: List arguments prevent shell injection, shell=False is default
    result = subprocess.run(['stat', '-c', '%a', filepath], capture_output=True, text=True)
    return result.stdout.strip()
