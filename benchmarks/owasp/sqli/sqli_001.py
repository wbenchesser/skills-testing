"""
SQL Injection Test Case: String Concatenation
CWE-89: SQL Injection
Expected: VULNERABLE (True Positive)
"""

import sqlite3

def search_users(username):
    """
    Search for users by username.
    VULNERABILITY: Uses string concatenation to build SQL query.
    """
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # VULNERABLE: Direct string concatenation with user input
    query = "SELECT * FROM users WHERE username = '" + username + "'"

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results
