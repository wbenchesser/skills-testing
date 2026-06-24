# OWASP Benchmark Test Cases

This directory contains Python code samples representing common vulnerability patterns from the OWASP Benchmark project, adapted for skills testing.

## Organization

Test cases are organized by CWE category:

```
owasp/
├── expected-results.csv    # Ground truth for all test cases
├── sqli/                   # CWE-89: SQL Injection
├── xss/                    # CWE-79: Cross-Site Scripting
└── cmdi/                   # CWE-78: OS Command Injection
```

Each category contains:
- **True Positive** test cases (vulnerable code that SHOULD be flagged)
- **False Positive** test cases (secure code that should NOT be flagged)

## Naming Convention

Files follow the pattern: `{category}_{NNN}.py`

- `category`: Short name (sqli, xss, cmdi)
- `NNN`: Zero-padded 3-digit number (001, 002, etc.)

Examples:
- `sqli_001.py` - First SQL injection test case
- `xss_004.py` - Fourth XSS test case

## Ground Truth File

`expected-results.csv` maps each test case to its expected result:

```csv
file,category,cwe,is_vulnerable,description
sqli/sqli_001.py,sqli,89,true,String concatenation in SQL query
sqli/sqli_004.py,sqli,89,false,Parameterized query with placeholder
```

**Columns:**
- `file`: Relative path from owasp/ directory
- `category`: Short category name
- `cwe`: CWE identifier number
- `is_vulnerable`: `true` for vulnerable code, `false` for secure code
- `description`: One-line summary of the test case

## Current Coverage

| Category | CWE | True Positives | False Positives | Total |
|----------|-----|----------------|-----------------|-------|
| SQL Injection | 89 | 3 | 2 | 5 |
| Cross-Site Scripting | 79 | 3 | 2 | 5 |
| Command Injection | 78 | 3 | 2 | 5 |
| **Total** | | **9** | **6** | **15** |

## Test Case Structure

Each Python file:
- Is syntactically valid (can be parsed by Python)
- Contains a docstring header with CWE, expected result, and description
- Focuses on ONE vulnerability pattern
- Is self-contained (imports, function definition, clear vulnerable/safe line)

**Example:**

```python
"""
SQL Injection Test Case: String Concatenation
CWE-89: SQL Injection
Expected: VULNERABLE (True Positive)
"""

import sqlite3

def search_users(username):
    """VULNERABILITY: Uses string concatenation"""
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()
```

## Adding New Test Cases

1. **Choose a category** (or create a new directory for a new CWE)

2. **Write the vulnerable or safe code**:
   - Keep it focused on ONE pattern
   - Use realistic code (Flask, Django, common libraries)
   - Include clear inline comments marking the vulnerable line

3. **Follow the naming convention**:
   - Find the highest existing number in that category
   - Increment by 1, zero-pad to 3 digits

4. **Add to expected-results.csv**:
   ```csv
   sqli/sqli_006.py,sqli,89,true,New vulnerability pattern description
   ```

5. **Validate syntax**:
   ```bash
   python -c "import ast; ast.parse(open('benchmarks/owasp/sqli/sqli_006.py').read())"
   ```

6. **Balance true/false positives**:
   - Aim for ~60% true positives, ~40% false positives
   - False positives are critical for measuring precision

## Adding New Categories

To add a new CWE category (e.g., Path Traversal - CWE-22):

1. Create a new directory:
   ```bash
   mkdir benchmarks/owasp/pathtraver
   ```

2. Choose a short category name (4-10 chars, lowercase)
   - Refer to OWASP Benchmark naming: `sqli`, `xss`, `cmdi`, `pathtraver`, `ldapi`, `xpathi`

3. Write 3-5 true positive and 2-3 false positive test cases

4. Add entries to `expected-results.csv`

5. Update this README with the new category in the coverage table

## Resources

- [OWASP Benchmark Project](https://owasp.org/www-project-benchmark/)
- [OWASP BenchmarkJava Repository](https://github.com/OWASP-Benchmark/BenchmarkJava)
- [CWE List](https://cwe.mitre.org/data/index.html)
- [OWASP Top 10:2025](https://owasp.org/Top10/2025/en/)

## Known Limitations

- **Language**: Only Python test cases currently (OWASP Benchmark includes Java, .NET, Python)
- **Framework coverage**: Focuses on Flask, Django, SQLAlchemy (could add FastAPI, Tornado, etc.)
- **Complexity**: Simple, single-function examples (real-world vulnerabilities often span multiple files)
- **Data flow depth**: Direct vulnerabilities (not multi-hop taint tracking scenarios)

These limitations are intentional for MVP — the goal is to test skill trigger accuracy and precision on clear patterns before expanding to more complex scenarios.
