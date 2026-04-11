from django.contrib import admin

from admin_test.models import Author, Category, Comment, Post, Tag


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
    search_fields = ["name", "email"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""

    list_display = ["name", "slug", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model."""

    list_display = ["name", "slug", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model."""

    list_display = ["title", "author", "is_published", "created_at"]
    list_filter = ["is_published", "created_at", "author", "categories"]
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
    search_fields = ["content", "author__name", "post__title"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        ("Comment Information", {"fields": ("post", "author", "content")}),
        ("Moderation", {"fields": ("is_approved", "created_at", "updated_at")}),
    )
