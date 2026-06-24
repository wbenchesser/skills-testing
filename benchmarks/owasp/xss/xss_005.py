"""
XSS Test Case: Django Template Autoescaping
CWE-79: Cross-Site Scripting
Expected: SAFE (False Positive Test)
"""

from django.http import HttpResponse
from django.template import Template, Context

def display_message(request):
    """
    Display user message.
    SAFE: Django templates autoescape by default.
    """
    message = request.GET.get('msg', '')

    # SAFE: Django template autoescaping is on by default
    template = Template("""
        <html>
            <body>
                <h1>Message:</h1>
                <p>{{ user_message }}</p>
            </body>
        </html>
    """)

    context = Context({'user_message': message})
    html = template.render(context)

    return HttpResponse(html)
