import re
import sys
from datetime import datetime, timedelta

import django
from django import template
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.utils.safestring import mark_safe
from django.utils.timezone import now

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


@register.simple_tag
def app_model_stats(app_label, app_list):
    """
    Get model statistics for a specific app.
    Returns dict with: total_models, accessible_models
    """
    if not app_list:
        return {
            "total_models": 0,
            "accessible_models": 0,
        }

    # Find the app in app_list
    app_entry = next(
        (app for app in app_list if app.get("app_label") == app_label), None
    )

    if not app_entry:
        return {
            "total_models": 0,
            "accessible_models": 0,
        }

    models = app_entry.get("models", [])
    total = len(models)
    accessible = sum(1 for m in models if any(m.get("perms", {}).values()))

    return {
        "total_models": total,
        "accessible_models": accessible,
    }


@register.simple_tag
def app_activity_summary(app_label):
    """
    Get activity summary for an app over the last 7 days.
    Returns dict with: recent_changes, total_additions, total_deletions
    """
    from django.apps import apps as django_apps
    from django.contrib.contenttypes.models import ContentType

    try:
        # Get all content types for this app
        app_config = django_apps.get_app_config(app_label)
        models_in_app = [model for model in app_config.get_models()]

        if not models_in_app:
            return {
                "recent_changes": 0,
                "total_additions": 0,
                "total_deletions": 0,
                "total_activity": 0,
            }

        # Get content types for all models in this app
        content_types = ContentType.objects.filter(app_label=app_label).values_list(
            "id", flat=True
        )

        # Get log entries from last 7 days
        seven_days_ago = now() - timedelta(days=7)
        logs = LogEntry.objects.filter(
            content_type_id__in=content_types, action_time__gte=seven_days_ago
        )

        total_changes = logs.count()
        total_additions = logs.filter(action_flag=1).count()
        total_deletions = logs.filter(action_flag=3).count()

        return {
            "recent_changes": total_changes,
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "total_activity": total_changes,
        }
    except Exception:
        return {
            "recent_changes": 0,
            "total_additions": 0,
            "total_deletions": 0,
            "total_activity": 0,
        }


@register.simple_tag
def app_model_health(app_label, app_list):
    """
    Get record count statistics for each model in the app.
    Returns list of dicts with: name, object_name, count, perms, admin_url
    Sorted by record count (descending).
    """
    if not app_list:
        return []

    # Find the app in app_list
    app_entry = next(
        (app for app in app_list if app.get("app_label") == app_label), None
    )

    if not app_entry:
        return []

    models = app_entry.get("models", [])
    model_stats = []

    for model_info in models:
        try:
            # Get the actual Django model class
            model_class = model_info.get("model")
            if model_class:
                count = model_class.objects.count()
                model_stats.append(
                    {
                        "name": model_info.get("name", ""),
                        "object_name": model_info.get("object_name", ""),
                        "count": count,
                        "perms": model_info.get("perms", {}),
                        "admin_url": model_info.get("admin_url", ""),
                    }
                )
        except Exception:
            # If we can't count, skip this model
            pass

    # Sort by count descending, limit to top 5
    model_stats.sort(key=lambda x: x["count"], reverse=True)
    return model_stats[:5]


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


@register.filter
def group_deleted_objects(deleted_objects):
    """
    Flatten and group Django's nested deleted_objects list by model type.

    Each item in the list is a string like "ModelName: <a href>obj</a>"
    or a nested list of related objects. Returns an ordered list of
    (model_name, [object_html, ...]) tuples preserving first-seen order.
    """
    from collections import OrderedDict

    groups = OrderedDict()

    def _flatten(items):
        for item in items:
            if isinstance(item, (list, tuple)):
                _flatten(item)
            else:
                # item is a string/SafeData like "ModelName: <a ...>Name</a>"
                text = str(item)
                if ": " in text:
                    model_name, _, obj_html = text.partition(": ")
                    model_name = model_name.strip()
                else:
                    model_name = "Other"
                    obj_html = text
                groups.setdefault(model_name, []).append(mark_safe(obj_html))

    _flatten(deleted_objects)
    return list(groups.items())
