from django.contrib import admin
from django.forms import RadioSelect

from admin_test.models import (
    Author,
    Category,
    Comment,
    EventLog,
    EventSchedule,
    Poll,
    Post,
    Tag,
)


# Inline configurations
class CommentInline(admin.TabularInline):
    """Tabular inline display for comments."""

    model = Comment
    extra = 1
    fields = ["author", "content", "is_approved", "created_at"]
    readonly_fields = ["created_at"]


class CategoryInline(admin.StackedInline):
    """Stacked inline display for categories."""

    model = Post.categories.through
    extra = 1
    verbose_name = "Category"
    verbose_name_plural = "Categories"


class TagInline(admin.StackedInline):
    """Stacked inline display for tags."""

    model = Post.tags.through
    extra = 1
    verbose_name = "Tag"
    verbose_name_plural = "Tags"


# Model Admin classes
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface for Author model."""

    list_display = ["name", "email", "created_at"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
    search_fields = ["name", "email"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""

    list_display = ["name", "slug", "created_at"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model."""

    list_display = ["name", "slug", "created_at"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model."""

    list_display = ["title", "author", "is_published", "created_at"]
    list_filter = ["is_published", "created_at", "author", "categories"]
    date_hierarchy = "created_at"
    search_fields = ["title", "content", "author__name"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]
    inlines = [CommentInline, CategoryInline, TagInline]

    fieldsets = (
        ("Post Information", {"fields": ("title", "slug", "author")}),
        ("Content", {"fields": ("content", "excerpt")}),
        ("Publishing", {"fields": ("is_published", "created_at", "updated_at")}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model."""

    list_display = ["author", "post", "is_approved", "created_at"]
    list_filter = ["is_approved", "created_at", "post__author"]
    date_hierarchy = "created_at"
    search_fields = ["content", "author__name", "post__title"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(EventSchedule)
class EventScheduleAdmin(admin.ModelAdmin):
    """Admin interface for EventSchedule model with radio widget for event type."""

    list_display = ["title", "event_type", "event_date", "event_time", "location"]
    list_filter = ["event_type", "event_date"]
    date_hierarchy = "event_date"
    search_fields = ["title", "location"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-event_date", "-event_time"]

    fieldsets = (
        ("Event Information", {"fields": ("title", "location", "description")}),
        (
            "Event Details",
            {
                "fields": ("event_type", "event_date", "event_time"),
                "description": "Select event type using radio buttons below",
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "event_type":
            kwargs["widget"] = RadioSelect()
        return super().formfield_for_choice_field(db_field, request, **kwargs)


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    """Admin interface for Poll model with radio widget for status."""

    list_display = ["title", "status", "allow_multiple_votes", "created_at"]
    list_filter = ["status", "allow_multiple_votes", "created_at"]
    date_hierarchy = "created_at"
    search_fields = ["title", "question"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Poll Information", {"fields": ("title", "question")}),
        (
            "Settings",
            {
                "fields": ("status", "allow_multiple_votes"),
                "description": "Select poll status using radio buttons below",
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "status":
            kwargs["widget"] = RadioSelect()
        return super().formfield_for_choice_field(db_field, request, **kwargs)


@admin.register(EventLog)
class EventLogAdmin(admin.ModelAdmin):
    """Admin interface for EventLog model with date and time fields."""

    list_display = ["event_name", "log_level", "log_date", "log_time", "user"]
    list_filter = ["log_level", "log_date"]
    date_hierarchy = "log_date"
    search_fields = ["event_name", "message", "user"]
    readonly_fields = ["created_at"]
    ordering = ["-log_date", "-log_time"]

    fieldsets = (
        ("Log Information", {"fields": ("event_name", "message", "user")}),
        (
            "Log Details",
            {
                "fields": ("log_level", "log_date", "log_time"),
                "description": "Select log level using radio buttons below",
            },
        ),
        ("Timestamps", {"fields": ("created_at",)}),
    )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "log_level":
            kwargs["widget"] = RadioSelect()
        return super().formfield_for_choice_field(db_field, request, **kwargs)

