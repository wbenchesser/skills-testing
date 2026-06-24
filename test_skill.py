#!/usr/bin/env python3
"""
Automated Skills Testing Harness

Tests AI security skills against OWASP benchmark test cases and calculates metrics.
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import anthropic
import requests
import urllib3

# Suppress InsecureRequestWarning for internal proxies with self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SkillTester:
    """Test a skill against benchmark test cases."""

    def __init__(self, skill_path: Path, api_key: Optional[str] = None,
                 model: str = "claude-sonnet-4-20250514",
                 use_models_corp: bool = False):
        """
        Initialize the skill tester.

        Args:
            skill_path: Path to the skill directory containing SKILL.md
            api_key: API key (or Bearer token for Models.corp)
            model: Model ID to use
            use_models_corp: Whether to use Red Hat Models.corp proxy
        """
        self.skill_path = Path(skill_path)
        self.skill_md_path = self.skill_path / "SKILL.md"

        if not self.skill_md_path.exists():
            raise FileNotFoundError(f"Skill file not found: {self.skill_md_path}")

        # Load skill content
        with open(self.skill_md_path, 'r') as f:
            self.skill_content = f.read()

        # Initialize Anthropic client or Models.corp config
        self.use_models_corp = use_models_corp

        if use_models_corp:
            # Red Hat Models.corp proxy configuration
            self.base_url = os.getenv(
                'MODEL_API',
                'https://claude--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443'
            )
            self.api_key = api_key or os.getenv('USER_KEY')
            if not self.api_key:
                raise ValueError("USER_KEY environment variable or --api-key required for Models.corp")
            self.client = None
        else:
            # Standard Anthropic API
            self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
            if not self.api_key:
                raise ValueError("ANTHROPIC_API_KEY environment variable or --api-key required")
            self.client = anthropic.Anthropic(api_key=self.api_key)

        self.model = model

    def _call_models_corp(self, prompt: str) -> str:
        """
        Call Models.corp proxy using Vertex-style API format.

        Args:
            prompt: User prompt text

        Returns:
            Response text from Claude
        """
        # Vertex-style endpoint format
        endpoint = f"{self.base_url}/sonnet/models/{self.model}:streamRawPredict"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Vertex-style request body
        # Content must be an array of objects with type and text fields
        payload = {
            "anthropic_version": "vertex-2023-10-16",
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ],
            "max_tokens": 1024,
            "temperature": 0
        }

        # Disable SSL verification for internal proxies with self-signed certs
        response = requests.post(endpoint, headers=headers, json=payload, timeout=120, verify=False)
        response.raise_for_status()

        # Parse Vertex-style response
        result = response.json()

        # Extract text from content blocks
        if "content" in result and isinstance(result["content"], list):
            text_blocks = [block["text"] for block in result["content"] if block.get("type") == "text"]
            return " ".join(text_blocks)
        else:
            raise ValueError(f"Unexpected response format: {result}")

    def review_file(self, file_path: Path) -> Dict:
        """
        Ask Claude to review a benchmark file using the skill.

        Returns:
            Dict with 'flagged' (bool), 'reasoning' (str), 'raw_response' (str)
        """
        with open(file_path, 'r') as f:
            code_content = f.read()

        # Construct prompt
        prompt = f"""You are a security code reviewer. Use the following skill to review the code:

<skill>
{self.skill_content}
</skill>

Review this Python code and determine if it contains a security vulnerability that matches the skill's criteria:

<code>
{code_content}
</code>

Respond in JSON format:
{{
    "flagged": true/false,
    "vulnerability_type": "sqli|xss|cmdi|none",
    "reasoning": "brief explanation",
    "confidence": "high|medium|low"
}}
"""

        try:
            if self.use_models_corp:
                # Use Vertex-style API for Models.corp
                response_text = self._call_models_corp(prompt)
            else:
                # Use standard Anthropic API
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = message.content[0].text

            # Try to parse JSON response
            try:
                # Extract JSON if it's wrapped in markdown code blocks
                if '```json' in response_text:
                    json_start = response_text.find('```json') + 7
                    json_end = response_text.find('```', json_start)
                    response_text = response_text[json_start:json_end].strip()
                elif '```' in response_text:
                    json_start = response_text.find('```') + 3
                    json_end = response_text.find('```', json_start)
                    response_text = response_text[json_start:json_end].strip()

                result = json.loads(response_text)
                return {
                    'flagged': result.get('flagged', False),
                    'vulnerability_type': result.get('vulnerability_type', 'unknown'),
                    'reasoning': result.get('reasoning', ''),
                    'confidence': result.get('confidence', 'unknown'),
                    'raw_response': response_text
                }
            except json.JSONDecodeError:
                # Fallback: look for keywords indicating a finding
                response_lower = response_text.lower()
                flagged = any(keyword in response_lower for keyword in [
                    'vulnerable', 'vulnerability', 'injection', 'unsafe',
                    'security risk', 'flagged: true'
                ])

                return {
                    'flagged': flagged,
                    'vulnerability_type': 'unknown',
                    'reasoning': response_text[:200],
                    'confidence': 'unknown',
                    'raw_response': response_text
                }

        except Exception as e:
            print(f"Error reviewing {file_path}: {e}", file=sys.stderr)
            return {
                'flagged': False,
                'vulnerability_type': 'error',
                'reasoning': str(e),
                'confidence': 'error',
                'raw_response': ''
            }

    def test_category(self, category: str, benchmarks_dir: Path) -> Dict:
        """
        Test the skill against all benchmarks in a category.

        Returns:
            Dict with results and metrics
        """
        owasp_dir = benchmarks_dir / "owasp"
        category_dir = owasp_dir / category
        expected_csv = owasp_dir / "expected-results.csv"

        if not category_dir.exists():
            raise FileNotFoundError(f"Category directory not found: {category_dir}")
        if not expected_csv.exists():
            raise FileNotFoundError(f"Expected results CSV not found: {expected_csv}")

        # Load expected results
        expected_results = {}
        with open(expected_csv, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['category'] == category:
                    expected_results[row['file']] = row['is_vulnerable'] == 'true'

        # Test each file
        results = []
        for test_file in sorted(category_dir.glob("*.py")):
            relative_path = f"{category}/{test_file.name}"
            expected_vulnerable = expected_results.get(relative_path, None)

            if expected_vulnerable is None:
                print(f"Warning: {relative_path} not in expected-results.csv", file=sys.stderr)
                continue

            print(f"Testing {test_file.name}...", end=' ')
            sys.stdout.flush()

            review_result = self.review_file(test_file)
            flagged = review_result['flagged']

            # Determine result
            if expected_vulnerable and flagged:
                result_type = "TP"  # True Positive
            elif not expected_vulnerable and not flagged:
                result_type = "TN"  # True Negative
            elif not expected_vulnerable and flagged:
                result_type = "FP"  # False Positive
            else:  # expected_vulnerable and not flagged
                result_type = "FN"  # False Negative

            print(f"{result_type}")

            results.append({
                'file': test_file.name,
                'expected_vulnerable': expected_vulnerable,
                'flagged': flagged,
                'result_type': result_type,
                'reasoning': review_result['reasoning'],
                'confidence': review_result['confidence']
            })

        # Calculate metrics
        tp = sum(1 for r in results if r['result_type'] == 'TP')
        tn = sum(1 for r in results if r['result_type'] == 'TN')
        fp = sum(1 for r in results if r['result_type'] == 'FP')
        fn = sum(1 for r in results if r['result_type'] == 'FN')

        total_vulnerable = sum(1 for r in results if r['expected_vulnerable'])
        total_safe = sum(1 for r in results if not r['expected_vulnerable'])

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        accuracy = (tp + tn) / len(results) if results else 0

        return {
            'category': category,
            'results': results,
            'metrics': {
                'tp': tp,
                'tn': tn,
                'fp': fp,
                'fn': fn,
                'total_vulnerable': total_vulnerable,
                'total_safe': total_safe,
                'precision': precision,
                'recall': recall,
                'f1': f1,
                'accuracy': accuracy
            }
        }


def print_results(test_results: Dict):
    """Print formatted test results."""
    category = test_results['category']
    metrics = test_results['metrics']
    results = test_results['results']

    print(f"\n{'='*60}")
    print(f"Results for category: {category.upper()}")
    print(f"{'='*60}\n")

    print("Confusion Matrix:")
    print(f"  True Positives (TP):  {metrics['tp']}/{metrics['total_vulnerable']} "
          f"({metrics['tp']/metrics['total_vulnerable']*100:.1f}% of vulnerable code flagged)")
    print(f"  False Negatives (FN): {metrics['fn']}/{metrics['total_vulnerable']} "
          f"({metrics['fn']/metrics['total_vulnerable']*100:.1f}% of vulnerable code missed)")
    print(f"  True Negatives (TN):  {metrics['tn']}/{metrics['total_safe']} "
          f"({metrics['tn']/metrics['total_safe']*100:.1f}% of safe code passed)")
    print(f"  False Positives (FP): {metrics['fp']}/{metrics['total_safe']} "
          f"({metrics['fp']/metrics['total_safe']*100:.1f}% of safe code incorrectly flagged)")

    print(f"\nMetrics:")
    print(f"  Precision: {metrics['precision']*100:.1f}% (of flagged code, how much was actually vulnerable)")
    print(f"  Recall:    {metrics['recall']*100:.1f}% (of vulnerable code, how much was caught)")
    print(f"  F1 Score:  {metrics['f1']*100:.1f}%")
    print(f"  Accuracy:  {metrics['accuracy']*100:.1f}%")

    # Show failures
    failures = [r for r in results if r['result_type'] in ['FP', 'FN']]
    if failures:
        print(f"\nFailures ({len(failures)}):")
        for f in failures:
            print(f"  [{f['result_type']}] {f['file']}: {f['reasoning'][:80]}...")


def save_detailed_results(test_results: Dict, output_path: Path):
    """Save detailed results to JSON."""
    with open(output_path, 'w') as f:
        json.dump(test_results, f, indent=2)
    print(f"\nDetailed results saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Test a security skill against OWASP benchmarks"
    )
    parser.add_argument(
        "--skill",
        required=True,
        help="Path to skill directory (containing SKILL.md)"
    )
    parser.add_argument(
        "--category",
        required=True,
        choices=["sqli", "xss", "cmdi"],
        help="OWASP category to test against"
    )
    parser.add_argument(
        "--benchmarks",
        default="benchmarks",
        help="Path to benchmarks directory (default: benchmarks)"
    )
    parser.add_argument(
        "--output",
        help="Path to save detailed JSON results (default: results/<skill>-<category>.json)"
    )
    parser.add_argument(
        "--api-key",
        help="API key (overrides environment variables)"
    )
    parser.add_argument(
        "--model",
        help="Model ID to use (default: from MODEL_ID env var, or claude-sonnet-4-20250514 for Anthropic API, or claude-sonnet-4@20250514 for Models.corp)"
    )
    parser.add_argument(
        "--models-corp",
        action="store_true",
        help="Use Red Hat Models.corp proxy instead of direct Anthropic API"
    )

    args = parser.parse_args()

    # Resolve paths
    skill_path = Path(args.skill)
    benchmarks_dir = Path(args.benchmarks)

    if args.output:
        output_path = Path(args.output)
    else:
        output_dir = Path("results")
        output_dir.mkdir(exist_ok=True)
        skill_name = skill_path.name
        output_path = output_dir / f"{skill_name}-{args.category}.json"

    # Determine model ID based on API type
    if args.model:
        model = args.model
    elif args.models_corp:
        model = os.getenv('MODEL_ID', 'claude-sonnet-4@20250514')
    else:
        model = 'claude-sonnet-4-20250514'

    # Run tests
    try:
        tester = SkillTester(
            skill_path,
            api_key=args.api_key,
            model=model,
            use_models_corp=args.models_corp
        )
        results = tester.test_category(args.category, benchmarks_dir)

        print_results(results)
        save_detailed_results(results, output_path)

        # Exit with error code if precision or recall is below 80%
        if results['metrics']['precision'] < 0.8 or results['metrics']['recall'] < 0.8:
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
