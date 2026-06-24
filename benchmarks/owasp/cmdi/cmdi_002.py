"""
Command Injection Test Case: subprocess.call with shell=True
CWE-78: OS Command Injection
Expected: VULNERABLE (True Positive)
"""

import subprocess

def compress_file(filename):
    """
    Compress a file using gzip.
    VULNERABILITY: shell=True with user-controlled input allows command injection.
    """
    # VULNERABLE: shell=True makes string concatenation dangerous
    cmd = f"gzip {filename}"
    subprocess.call(cmd, shell=True)
