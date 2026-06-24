"""
XSS Test Case: Django mark_safe with User Input
CWE-79: Cross-Site Scripting
Expected: VULNERABLE (True Positive)
"""

from django.http import HttpResponse
from django.utils.safestring import mark_safe

def profile_view(request):
    """
    Display user profile with bio.
    VULNERABILITY: mark_safe() used on user-controlled content.
    """
    bio = request.GET.get('bio', '')

    # VULNERABLE: mark_safe bypasses Django's auto-escaping
    html = f"<div class='bio'>{bio}</div>"
    safe_html = mark_safe(html)

    return HttpResponse(f"<html><body><h1>Profile</h1>{safe_html}</body></html>")
