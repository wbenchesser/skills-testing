"""
SQL Injection Test Case: Parameterized Query
CWE-89: SQL Injection
Expected: SAFE (False Positive Test)
"""

import sqlite3

def get_user_by_id(user_id):
    """
    Fetch user by ID.
    SAFE: Uses parameterized query with placeholder.
    """
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()

    # SAFE: Parameterized query with ? placeholder
    query = "SELECT * FROM users WHERE id = ?"

    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    conn.close()

    return user
