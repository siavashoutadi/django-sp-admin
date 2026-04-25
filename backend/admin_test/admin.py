from django.contrib import admin
from django.forms import RadioSelect

from admin_test.models import (
    Author,
    BooleanTestModel,
    Category,
    ChoiceTestModel,
    Comment,
    DateTimeComprehensiveModel,
    EventLog,
    EventSchedule,
    IdentifierModel,
    NumberTestModel,
    Poll,
    Post,
    RelationshipTestModel,
    Tag,
    TextFieldsModel,
    URLEmailFileModel,
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
    readonly_fields = ["created_at", "updated_at"]
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
        (
            "Additional Date/Time Fields",
            {
                "fields": (
                    "log_datetime",
                    "scheduled_date",
                    "scheduled_time",
                    "start_datetime",
                    "end_datetime",
                    "duration",
                ),
                "classes": ("collapse",),
            },
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "log_level":
            kwargs["widget"] = RadioSelect()
        return super().formfield_for_choice_field(db_field, request, **kwargs)


@admin.register(NumberTestModel)
class NumberTestModelAdmin(admin.ModelAdmin):
    """Admin interface for NumberTestModel with numeric field widgets."""

    list_display = [
        "title",
        "integer_field",
        "decimal_field",
        "float_field",
    ]
    list_filter = ["positive_integer"]
    search_fields = ["title"]
    ordering = ["-id"]

    fieldsets = (
        ("Basic Information", {"fields": ("title",)}),
        (
            "Integer Fields",
            {
                "fields": (
                    "integer_field",
                    "positive_integer",
                    "big_integer",
                    "small_integer",
                )
            },
        ),
        (
            "Decimal & Float Fields",
            {"fields": ("decimal_field", "float_field")},
        ),
    )


@admin.register(BooleanTestModel)
class BooleanTestModelAdmin(admin.ModelAdmin):
    """Admin interface for BooleanTestModel with boolean field widgets."""

    list_display = [
        "title",
        "is_active",
        "is_published",
        "is_verified",
        "requires_approval",
        "is_archived",
    ]
    list_filter = ["is_active", "is_published", "is_verified", "requires_approval"]
    search_fields = ["title"]
    ordering = ["-id"]


@admin.register(URLEmailFileModel)
class URLEmailFileModelAdmin(admin.ModelAdmin):
    """Admin interface for URLEmailFileModel with URL, email, and file widgets."""

    list_display = ["title", "email", "website_url"]
    list_filter = []
    search_fields = ["title", "email"]
    ordering = ["-id"]

    fieldsets = (
        ("Basic Information", {"fields": ("title",)}),
        (
            "Contact Information",
            {"fields": ("email", "backup_email", "website_url")},
        ),
        (
            "File Uploads",
            {"fields": ("document", "image", "thumbnail")},
        ),
    )


@admin.register(ChoiceTestModel)
class ChoiceTestModelAdmin(admin.ModelAdmin):
    """Admin interface for ChoiceTestModel with choice field widgets."""

    list_display = ["title", "priority", "status", "difficulty"]
    list_filter = ["priority", "status", "difficulty"]
    search_fields = ["title"]
    ordering = ["-id"]

    fieldsets = (
        ("Basic Information", {"fields": ("title",)}),
        (
            "Selection Fields",
            {"fields": ("priority", "status", "difficulty")},
        ),
    )

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        """Use RadioSelect for all choice fields."""
        if db_field.name in ["priority", "status", "difficulty"]:
            kwargs["widget"] = RadioSelect()
        return super().formfield_for_choice_field(db_field, request, **kwargs)


@admin.register(DateTimeComprehensiveModel)
class DateTimeComprehensiveModelAdmin(admin.ModelAdmin):
    """Admin interface for DateTimeComprehensiveModel with all date/time field types."""

    list_display = ["title", "date_field", "time_field", "datetime_field"]
    list_filter = ["date_field"]
    date_hierarchy = "date_field"
    search_fields = ["title"]
    readonly_fields = ["auto_now_field", "auto_now_add_field"]
    ordering = ["-id"]

    fieldsets = (
        ("Basic Information", {"fields": ("title",)}),
        (
            "Required Date/Time Fields",
            {
                "fields": (
                    "date_field",
                    "time_field",
                    "datetime_field",
                )
            },
        ),
        (
            "Optional Date/Time Fields",
            {
                "fields": (
                    "optional_date",
                    "optional_time",
                    "optional_datetime",
                    "duration_field",
                )
            },
        ),
        (
            "Auto Fields",
            {
                "fields": ("auto_now_add_field", "auto_now_field"),
                "description": "These fields are automatically managed by Django",
            },
        ),
    )


@admin.register(IdentifierModel)
class IdentifierModelAdmin(admin.ModelAdmin):
    """Admin interface for IdentifierModel with UUID, slug, and other identifiers."""

    list_display = ["title", "slug_field", "code", "uuid_field"]
    list_filter = []
    search_fields = ["title", "slug_field", "code"]
    readonly_fields = ["uuid_field"]
    prepopulated_fields = {"slug_field": ("title",)}
    ordering = ["-id"]

    fieldsets = (
        ("Basic Information", {"fields": ("title",)}),
        (
            "Identifiers",
            {"fields": ("uuid_field", "slug_field", "code", "identifier")},
        ),
    )


@admin.register(TextFieldsModel)
class TextFieldsModelAdmin(admin.ModelAdmin):
    """Admin interface for TextFieldsModel with various text field types."""

    list_display = ["title", "short_text"]
    list_filter = []
    search_fields = ["title", "description", "short_text"]
    ordering = ["-id"]

    fieldsets = (
        ("Basic Information", {"fields": ("title",)}),
        (
            "Text Fields",
            {
                "fields": (
                    "short_text",
                    "medium_text",
                    "description",
                    "long_text",
                    "richtext_content",
                )
            },
        ),
    )


@admin.register(RelationshipTestModel)
class RelationshipTestModelAdmin(admin.ModelAdmin):
    """Admin interface for RelationshipTestModel with relationship fields."""

    list_display = ["title", "author"]
    list_filter = ["author", "categories", "tags"]
    search_fields = ["title", "author__name"]
    filter_horizontal = ["categories", "tags"]
    ordering = ["-id"]

    fieldsets = (
        ("Basic Information", {"fields": ("title", "author")}),
        (
            "Relationships",
            {"fields": ("categories", "tags")},
        ),
    )
