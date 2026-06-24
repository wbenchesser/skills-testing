"""
Command Injection Test Case: os.system() with User Input
CWE-78: OS Command Injection
Expected: VULNERABLE (True Positive)
"""

import os

def ping_host(hostname):
    """
    Ping a hostname to check connectivity.
    VULNERABILITY: User input passed directly to os.system().
    """
    # VULNERABLE: Direct command execution with user input
    command = "ping -c 4 " + hostname
    os.system(command)
