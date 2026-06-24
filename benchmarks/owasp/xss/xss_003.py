"""
XSS Test Case: Jinja2 |safe Filter
CWE-79: Cross-Site Scripting
Expected: VULNERABLE (True Positive)
"""

from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/comment')
def show_comment():
    """
    Display user comment.
    VULNERABILITY: |safe filter disables autoescaping on user input.
    """
    comment = request.args.get('comment', '')

    # VULNERABLE: |safe filter on user-controlled variable
    template = """
    <html>
        <body>
            <h2>Your Comment:</h2>
            <div>{{ user_comment|safe }}</div>
        </body>
    </html>
    """

    return render_template_string(template, user_comment=comment)

if __name__ == '__main__':
    app.run()
