"""
XSS Test Case: Flask with Jinja2 Autoescaping
CWE-79: Cross-Site Scripting
Expected: SAFE (False Positive Test)
"""

from flask import Flask, render_template_string, request

app = Flask(__name__)

@app.route('/search')
def search():
    """
    Display search results.
    SAFE: Jinja2 autoescaping enabled by default in Flask.
    """
    query = request.args.get('q', '')

    # SAFE: Jinja2 autoescapes {{ }} by default
    template = """
    <html>
        <body>
            <h1>Search Results for: {{ search_query }}</h1>
        </body>
    </html>
    """

    return render_template_string(template, search_query=query)

if __name__ == '__main__':
    app.run()
