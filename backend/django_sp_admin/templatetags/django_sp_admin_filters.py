import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def add_cell_classes(html, classes):
    """Add classes to <td> and <th> tags in rendered HTML"""
    # Add to <td> tags
    html = re.sub(r'<td([^>]*)class="([^"]*)"', rf'<td\1class="\2 {classes}"', html)
    # Add to <th> tags
    html = re.sub(
        r'<th([^>]*)class="([^"]*)"', rf'<th\1class="\2 underline {classes}"', html
    )
    # Replace checkbox class
    html = re.sub(
        r'<input([^>]*)type="checkbox"([^>]*)class="[^"]*"',
        r'<input\1type="checkbox"\2class="checkbox"',
        html,
    )
    return mark_safe(html)
