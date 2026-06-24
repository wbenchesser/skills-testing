"""
XSS Test Case: Flask f-string HTML Response
CWE-79: Cross-Site Scripting
Expected: VULNERABLE (True Positive)
"""

from flask import Flask, request

app = Flask(__name__)

@app.route('/greet')
def greet():
    """
    Display greeting with user's name.
    VULNERABILITY: User input directly embedded in HTML via f-string.
    """
    name = request.args.get('name', 'Guest')

    # VULNERABLE: Unescaped user input in HTML
    return f"<h1>Hello, {name}!</h1>"

if __name__ == '__main__':
    app.run()
