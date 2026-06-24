"""
SQL Injection Test Case: .format() Method
CWE-89: SQL Injection
Expected: VULNERABLE (True Positive)
"""

from sqlalchemy import create_engine, text

def find_orders(order_id):
    """
    Find orders by ID using SQLAlchemy.
    VULNERABILITY: Uses .format() to build SQL query with user input.
    """
    engine = create_engine('postgresql://user:pass@localhost/db')

    # VULNERABLE: String formatting in SQLAlchemy text()
    query = text("SELECT * FROM orders WHERE id = {}".format(order_id))

    with engine.connect() as conn:
        result = conn.execute(query)
        return result.fetchall()
