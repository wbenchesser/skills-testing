---
name: example-sql-injection
description: >
  Apply when reviewing Python code that constructs SQL queries
  using string concatenation, f-strings, or .format() with user-controlled input.
  Trigger on: sqlite3, psycopg2, SQLAlchemy text(), mysql.connector query construction.
category: "secure_development"
subcategory: "injection-prevention"
---

# SQL Injection Detection

Detect and prevent SQL injection vulnerabilities in Python database code.

## What to Look For

**Vulnerable patterns:**

1. **String concatenation** in queries:
   ```python
   query = "SELECT * FROM users WHERE id = " + user_id
   cursor.execute(query)
   ```

2. **f-strings** with user input:
   ```python
   query = f"SELECT * FROM users WHERE name = '{username}'"
   cursor.execute(query)
   ```

3. **`.format()` method**:
   ```python
   query = "SELECT * FROM users WHERE email = '{}'".format(email)
   cursor.execute(query)
   ```

4. **SQLAlchemy `text()` with concatenation**:
   ```python
   from sqlalchemy import text
   query = text(f"SELECT * FROM users WHERE id = {user_id}")
   ```

**Safe patterns (do NOT flag these):**

1. **Parameterized queries** with placeholders:
   ```python
   cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
   cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
   ```

2. **SQLAlchemy ORM** (no raw SQL):
   ```python
   session.query(User).filter(User.id == user_id).first()
   ```

3. **Named parameters**:
   ```python
   cursor.execute("SELECT * FROM users WHERE id = :id", {"id": user_id})
   ```

## Review Checklist

When reviewing code:

- [ ] Identify all database query construction sites
- [ ] Check if user-controlled data flows into queries
- [ ] Verify queries use parameterized statements, NOT string operations
- [ ] Flag any use of `+`, `f""`, or `.format()` in SQL query strings
- [ ] Check SQLAlchemy `text()` calls for dynamic content
- [ ] Verify ORM usage doesn't drop to raw SQL with user input

## Remediation

**Before:**
```python
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return cursor.execute(query).fetchone()
```

**After:**
```python
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    return cursor.execute(query, (username,)).fetchone()
```

## Common False Positives

- Static SQL strings (no variables): SAFE
- Queries with only integer type-casting: LOWER RISK (still verify)
- ORM query builders: SAFE unless using `.raw()` or `.text()`

## Resources

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [Python DB-API 2.0 Parameterized Queries](https://peps.python.org/pep-0249/)
- [SQLAlchemy SQL Injection Prevention](https://docs.sqlalchemy.org/en/20/core/tutorial.html#using-textual-sql)
