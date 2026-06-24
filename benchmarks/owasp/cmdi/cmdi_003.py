"""
Command Injection Test Case: os.popen() with Concatenated Input
CWE-78: OS Command Injection
Expected: VULNERABLE (True Positive)
"""

import os

def list_directory(path):
    """
    List contents of a directory.
    VULNERABILITY: os.popen() with concatenated user input.
    """
    # VULNERABLE: os.popen executes shell commands
    command = "ls -la " + path
    output = os.popen(command).read()
    return output
