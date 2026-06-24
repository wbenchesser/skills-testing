#!/usr/bin/env python3
"""
Test Models.corp or Anthropic API connection.

Helps debug API configuration issues by testing authentication,
endpoint URLs, and request/response format.
"""

import argparse
import json
import os
import sys
import requests
import urllib3
import anthropic

# Suppress SSL warnings for internal proxies
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def test_anthropic_api(api_key: str, model: str = "claude-sonnet-4-20250514"):
    """Test standard Anthropic API connection."""
    print("Testing Anthropic API...")
    print(f"Model: {model}")
    print()

    try:
        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model=model,
            max_tokens=100,
            messages=[{"role": "user", "content": "Say 'API connection successful' and nothing else."}]
        )

        response_text = message.content[0].text
        print("✓ Connection successful!")
        print(f"Response: {response_text}")
        print()
        print(f"Usage: {message.usage}")
        return True

    except Exception as e:
        print("✗ Connection failed!")
        print(f"Error: {e}")
        return False


def test_models_corp(api_key: str, base_url: str, model: str = "claude-sonnet-4-20250514"):
    """Test Red Hat Models.corp proxy connection."""
    print("Testing Models.corp Proxy...")
    print(f"Base URL: {base_url}")
    print(f"Model: {model}")
    print()

    # Try different endpoint formats
    endpoint_variants = [
        f"{base_url}/sonnet/models/{model}:streamRawPredict",
        f"{base_url}/v1/messages",
        f"{base_url}/anthropic/v1/messages",
        f"{base_url}/{model}:streamRawPredict",
    ]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Vertex-style payload
    # Content must be an array of objects with type and text fields
    payload = {
        "anthropic_version": "vertex-2023-10-16",
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": "Say 'API connection successful' and nothing else."}]
            }
        ],
        "max_tokens": 100,
        "temperature": 0
    }

    for i, endpoint in enumerate(endpoint_variants, 1):
        print(f"\nAttempt {i}: Testing endpoint...")
        print(f"URL: {endpoint}")
        print(f"Headers: Authorization: Bearer {api_key[:10]}...")
        print(f"Payload: {json.dumps(payload, indent=2)[:200]}...")
        print()

        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=30,
                verify=False
            )

            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {dict(response.headers)}")
            print()

            if response.status_code == 200:
                result = response.json()
                print("✓ Connection successful!")
                print(f"Response: {json.dumps(result, indent=2)[:500]}")

                # Try to extract message text
                if "content" in result and isinstance(result["content"], list):
                    text_blocks = [block["text"] for block in result["content"] if block.get("type") == "text"]
                    if text_blocks:
                        print(f"\nExtracted text: {text_blocks[0]}")

                print(f"\n✓ This endpoint works: {endpoint}")
                return True
            else:
                print(f"✗ Request failed")
                print(f"Response: {response.text[:500]}")

        except requests.exceptions.RequestException as e:
            print(f"✗ Request error: {e}")

        print("\n" + "="*60)

    print("\n✗ All endpoint variants failed")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Test Models.corp or Anthropic API connection"
    )
    parser.add_argument(
        "--models-corp",
        action="store_true",
        help="Test Red Hat Models.corp proxy (default: test Anthropic API)"
    )
    parser.add_argument(
        "--api-key",
        help="API key or Bearer token (overrides env vars)"
    )
    parser.add_argument(
        "--base-url",
        help="Models.corp base URL (default: from MODEL_API env var)"
    )
    parser.add_argument(
        "--model",
        help="Model ID to test (default: from MODEL_ID env var or claude-sonnet-4@20250514)"
    )

    args = parser.parse_args()

    print("="*60)
    print("API Connection Test")
    print("="*60)
    print()

    if args.models_corp:
        # Test Models.corp
        api_key = args.api_key or os.getenv('USER_KEY')
        base_url = args.base_url or os.getenv(
            'MODEL_API',
            'https://claude--apicast-production.apps.int.stc.ai.prod.us-east-1.aws.paas.redhat.com:443'
        )
        model = args.model or os.getenv('MODEL_ID', 'claude-sonnet-4@20250514')

        if not api_key:
            print("Error: USER_KEY environment variable or --api-key required")
            sys.exit(1)

        success = test_models_corp(api_key, base_url, model)
    else:
        # Test Anthropic API
        api_key = args.api_key or os.getenv('ANTHROPIC_API_KEY')
        model = args.model or 'claude-sonnet-4-20250514'

        if not api_key:
            print("Error: ANTHROPIC_API_KEY environment variable or --api-key required")
            sys.exit(1)

        success = test_anthropic_api(api_key, model)

    print()
    print("="*60)
    if success:
        print("✓ Connection test passed")
        sys.exit(0)
    else:
        print("✗ Connection test failed")
        print()
        print("Troubleshooting tips:")
        if args.models_corp:
            print("- Verify USER_KEY is correct")
            print("- Check MODEL_API endpoint URL")
            print("- Ensure you're on Red Hat VPN if required")
            print("- Check model ID format (e.g., claude-sonnet-4@20250514)")
        else:
            print("- Verify ANTHROPIC_API_KEY is correct")
            print("- Check https://console.anthropic.com/settings/keys")
            print("- Ensure API key has proper permissions")
        sys.exit(1)


if __name__ == "__main__":
    main()
