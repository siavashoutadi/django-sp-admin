import re
import sys
from datetime import datetime

import django
from django import template
from django.conf import settings
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


@register.simple_tag
def django_version():
    """Return Django version"""
    return django.get_version()


@register.simple_tag
def python_version():
    """Return Python version"""
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


@register.simple_tag
def debug_mode():
    """Return DEBUG setting"""
    return settings.DEBUG


@register.simple_tag
def database_engine():
    """Return database backend name"""
    engine = settings.DATABASES["default"]["ENGINE"]
    return engine.split(".")[-1]


@register.simple_tag
def current_year():
    """Return current year"""
    return datetime.now().year


@register.filter
def count_total_models(app_list):
    """Count total number of models across all apps"""
    if not app_list:
        return 0
    return sum(len(app.get("models", [])) for app in app_list)


@register.filter
def count_accessible_models(app_list):
    """Count total number of models user has access to"""
    count = 0
    if app_list:
        for app in app_list:
            for model in app.get("models", []):
                perms = model.get("perms", {})
                if any(perms.values()):  # Has at least one permission
                    count += 1
    return count


@register.filter
def action_type_display(action_flag):
    """Convert action flag to readable text"""
    action_map = {
        1: "Added",
        2: "Changed",
        3: "Deleted",
    }
    return action_map.get(action_flag, "Unknown")


@register.filter
def action_type_badge_class(action_flag):
    """Return badge class for action type"""
    if action_flag == 1:  # Addition
        return "bg-green-500/10 text-green-600"
    elif action_flag == 2:  # Change
        return "bg-blue-500/10 text-blue-600"
    elif action_flag == 3:  # Deletion
        return "bg-red-500/10 text-red-600"
    return ""


@register.filter
def action_type_icon(action_flag):
    """Return icon for action type"""
    if action_flag == 1:  # Addition
        return "ri-add-circle-line"
    elif action_flag == 2:  # Change
        return "ri-edit-2-line"
    elif action_flag == 3:  # Deletion
        return "ri-delete-bin-line"
    return "ri-history-line"


@register.filter
def time_since(timestamp):
    """Return human-readable time difference"""
    if not timestamp:
        return "Unknown"

    from django.utils.timezone import now

    diff = now() - timestamp

    seconds = diff.total_seconds()

    if seconds < 60:
        return "just now"
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f"{minutes}m ago"
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f"{hours}h ago"
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f"{days}d ago"
    else:
        weeks = int(seconds / 604800)
        return f"{weeks}w ago"


@register.inclusion_tag("admin/_user_app_list.html")
def user_app_list(user):
    """
    Get user's accessible apps and models with permissions.
    Works on all admin pages regardless of view context.
    """
    from django.apps import apps
    from django.contrib import admin

    app_list = []
    admin_site = admin.site

    for model, admin_class in admin_site._registry.items():
        app_label = model._meta.app_label

        # Check if user has any permission for this model
        has_add = user.has_perm(f"{app_label}.add_{model._meta.model_name}")
        has_change = user.has_perm(f"{app_label}.change_{model._meta.model_name}")
        has_delete = user.has_perm(f"{app_label}.delete_{model._meta.model_name}")
        has_view = user.has_perm(f"{app_label}.view_{model._meta.model_name}")

        if not any([has_add, has_change, has_delete, has_view]):
            continue

        # Find or create app entry
        app_entry = next(
            (app for app in app_list if app["app_label"] == app_label), None
        )

        if app_entry is None:
            # Get app config
            app_config = apps.get_app_config(app_label)
            app_entry = {
                "app_label": app_label,
                "name": app_config.verbose_name,
                "models": [],
            }
            app_list.append(app_entry)

        # Add model to app entry
        app_entry["models"].append(
            {
                "name": model._meta.verbose_name_plural.title(),
                "perms": {
                    "add": has_add,
                    "change": has_change,
                    "delete": has_delete,
                    "view": has_view,
                },
                "admin_url": admin_class.get_urls()[0].pattern
                if admin_class.get_urls()
                else "#",
            }
        )

    return {"app_list": app_list}
