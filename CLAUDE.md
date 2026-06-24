# Skills Testing Framework

This repository provides a framework for benchmarking AI agent skills against known vulnerability patterns from the OWASP Benchmark.

## What This Is

A testing harness to measure how reliably security skills:
1. **Trigger** when reviewing vulnerable code (trigger accuracy)
2. **Identify** the correct vulnerability type (detection accuracy)
3. **Avoid false positives** on secure code (precision)

The primary use case is validating security skills before deploying them in the Agentic Development Life Cycle (ADLC).

## Quick Start

### Automated Testing (Recommended)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API access**:

   For **standard Anthropic API**:
   ```bash
   export ANTHROPIC_API_KEY=your-api-key
   ```

   For **Red Hat Models.corp proxy**:
   ```bash
   export USER_KEY=your-bearer-token
   export MODEL_API=https://claude--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443
   ```

3. **Run automated tests**:
   ```bash
   # Test a skill against SQL injection benchmarks
   python test_skill.py --skill skills/example-sql-injection --category sqli

   # For Models.corp proxy, add the --models-corp flag:
   python test_skill.py --skill skills/example-sql-injection --category sqli --models-corp
   ```

4. **Review results**:
   ```
   Results for category: SQLI
   
   Confusion Matrix:
     True Positives (TP):  3/3 (100% of vulnerable code flagged)
     False Negatives (FN): 0/3 (0% of vulnerable code missed)
     True Negatives (TN):  2/2 (100% of safe code passed)
     False Positives (FP): 0/2 (0% of safe code incorrectly flagged)
   
   Metrics:
     Precision: 100%
     Recall:    100%
     F1 Score:  100%
   ```

### Manual Testing

1. **Add your skill** to the `skills/` directory:
   ```
   skills/
   └── my-sql-injection-detector/
       └── SKILL.md
   ```

2. **Tell Claude Code to load the skill** in your prompt:
   ```
   Using the skill in skills/my-sql-injection-detector/, review each file 
   in benchmarks/owasp/sqli/ and report whether you detected a vulnerability.
   ```

3. **Record results** by comparing Claude's findings against `benchmarks/owasp/expected-results.csv`

4. **Calculate metrics**:
   - **Trigger Accuracy**: Did the skill activate when reviewing vulnerable code?
   - **True Positive Rate**: Of the files marked `is_vulnerable=true`, how many did the skill flag?
   - **False Positive Rate**: Of the files marked `is_vulnerable=false`, how many did the skill incorrectly flag?
   - **Precision**: TP / (TP + FP)
   - **Recall**: TP / (TP + FN)

### Interpreting Results

**Good skill performance:**
- Trigger accuracy >90% on relevant files
- Recall >85% (catches most real vulnerabilities)
- Precision >90% (few false alarms)
- Executes consistently across multiple runs

**Needs improvement:**
- Inconsistent triggering (<80% activation)
- High false positive rate (>15%)
- Misses entire categories of vulnerabilities
- Different findings on identical inputs

## Directory Structure

```
skills-testing/
├── CLAUDE.md                    # This file - usage instructions
├── README.md                    # Research context and approach
├── skills/                      # Drop skills here to test them
│   └── example-sql-injection/
│       └── SKILL.md
├── benchmarks/
│   └── owasp/
│       ├── README.md            # How benchmarks are organized
│       ├── expected-results.csv # Ground truth for all test cases
│       ├── sqli/                # SQL Injection (CWE-89)
│       ├── xss/                 # Cross-Site Scripting (CWE-79)
│       └── cmdi/                # Command Injection (CWE-78)
└── results/                     # Your test output goes here (gitignored)
```

## How Skills Are Discovered

Claude Code reads `SKILL.md` files when explicitly instructed. Skills follow this format:

```yaml
---
name: skill-name
description: >
  When to trigger this skill (be specific)
category: "secure_development"
subcategory: "injection-prevention"
---

# Skill Body

Actionable guidance, code examples, checklists.
```

See `skills/example-sql-injection/SKILL.md` for a reference implementation.

## Benchmark Test Cases

The `benchmarks/owasp/` directory contains Python code samples organized by CWE category:

- **True Positives** (vulnerable code): Should trigger skill findings
- **False Positives** (secure code): Should NOT trigger findings

Each file represents one test case. The `expected-results.csv` file is the ground truth mapping:

```csv
file,category,cwe,is_vulnerable,description
sqli/sqli_001.py,sqli,89,true,String concatenation in SQL query
sqli/sqli_004.py,sqli,89,false,Parameterized query with placeholders
```

See `benchmarks/owasp/README.md` for details on adding new test cases.

## Adding Your Own Skills

1. Create a directory under `skills/` with your skill name (kebab-case)
2. Add a `SKILL.md` file with YAML frontmatter (see example skill)
3. Write clear, actionable guidance in the body
4. Test against relevant benchmark categories

## Adding New Benchmarks

1. Choose a CWE category (or create a new one under `benchmarks/owasp/`)
2. Write 3-5 vulnerable samples (true positives)
3. Write 2-3 secure samples that might look vulnerable but aren't (false positives)
4. Add entries to `expected-results.csv`
5. Validate syntax: `python -c "import ast; ast.parse(open('file.py').read())"`

## Test Harness Usage

### Basic Usage

```bash
# Test against SQL injection benchmarks
python test_skill.py --skill skills/example-sql-injection --category sqli

# Test against XSS benchmarks
python test_skill.py --skill skills/my-xss-detector --category xss

# Test against command injection benchmarks
python test_skill.py --skill skills/my-cmdi-detector --category cmdi
```

### Advanced Options

```bash
# Specify output location
python test_skill.py --skill skills/example-sql-injection --category sqli \
  --output results/custom-output.json

# Use a specific model
python test_skill.py --skill skills/example-sql-injection --category sqli \
  --model claude-opus-4-20250514

# Use Red Hat Models.corp proxy
python test_skill.py --skill skills/example-sql-injection --category sqli \
  --models-corp --api-key $USER_KEY
```

### Understanding Output

**Detailed JSON results** are saved to `results/<skill-name>-<category>.json`:

```json
{
  "category": "sqli",
  "results": [
    {
      "file": "sqli_001.py",
      "expected_vulnerable": true,
      "flagged": true,
      "result_type": "TP",
      "reasoning": "String concatenation in SQL query",
      "confidence": "high"
    }
  ],
  "metrics": {
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0
  }
}
```

### Exit Codes

- `0`: All tests passed with precision and recall ≥ 80%
- `1`: Tests failed (precision or recall < 80%) or error occurred

Use in CI/CD:
```bash
python test_skill.py --skill skills/my-skill --category sqli || echo "Skill failed quality threshold"
```

## Known Limitations

- **Trigger accuracy** depends heavily on the skill's `description` field in frontmatter
- Skills may require multiple runs to measure consistency (see Cloudflare findings: single runs find ~50% of issues)
- False positive thresholds vary by organization — adjust based on your tolerance

## Resources

- [Agent Eval Harness](https://github.com/opendatahub-io/agent-eval-harness) - Generic framework for skills evaluation
- [OWASP Benchmark Project](https://owasp.org/www-project-benchmark/) - Source for vulnerability test cases
- [Red Hat ProdSec Skills](https://github.com/RedHatProductSecurity/prodsec-skills) - Example production security skills
- [Cloudflare Vulnerability Scanning](https://blog.cloudflare.com/build-your-own-vulnerability-harness/) - Multi-agent approach to security scanning
