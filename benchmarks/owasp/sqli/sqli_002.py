"""
SQL Injection Test Case: f-string in Query
CWE-89: SQL Injection
Expected: VULNERABLE (True Positive)
"""

import psycopg2

def get_user_by_email(email):
    """
    Fetch user by email address.
    VULNERABILITY: Uses f-string to embed user input in SQL query.
    """
    conn = psycopg2.connect("dbname=myapp user=postgres")
    cursor = conn.cursor()

    # VULNERABLE: f-string interpolation with user input
    query = f"SELECT id, username, email FROM users WHERE email = '{email}'"

    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    return user
