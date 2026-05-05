from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
from django.forms import RadioSelect, CheckboxSelectMultiple
from django.utils.html import format_html, mark_safe
from django.urls import reverse
from django.db.models import Count

from admin_test.models import (
    Author,
    Category,
    Tag,
    Post,
    Comment,
    PostAnalytics,
    PostVersion,
    Product,
    ProductImage,
    ProductAttribute,
    ProductAttributeValue,
    ProductReview,
    Order,
    OrderItem,
    Coupon,
    Wishlist,
    ContentFile,
    Rating,
    SocialLink,
    Subscription,
    Notification,
)


# ============================================================================
# INLINES - Nested model displays
# ============================================================================


class CommentInline(admin.TabularInline):
    """Tabular inline for nested comments in posts."""
    model = Comment
    extra = 0
    fields = ["author", "rating", "is_approved", "created_at"]
    readonly_fields = ["created_at"]
    can_delete = True


class PostVersionInline(admin.TabularInline):
    """Tabular inline for post version history."""
    model = PostVersion
    extra = 0
    fields = ["version_number", "author", "created_at"]
    readonly_fields = ["version_number", "created_at"]
    can_delete = False


class ProductImageInline(admin.StackedInline):
    """Stacked inline for product gallery images."""
    model = ProductImage
    extra = 1
    fields = ["image", "alt_text", "sort_order"]


class ProductAttributeValueInline(admin.TabularInline):
    """Tabular inline for product attributes."""
    model = ProductAttributeValue
    extra = 1
    fields = ["attribute", "value"]


class ProductReviewInline(admin.TabularInline):
    """Tabular inline for product reviews."""
    model = ProductReview
    extra = 0
    fields = ["author", "rating", "title", "is_verified_purchase", "created_at"]
    readonly_fields = ["created_at"]
    can_delete = False


class OrderItemInline(admin.TabularInline):
    """Tabular inline for order items."""
    model = OrderItem
    extra = 0
    fields = ["product", "quantity", "unit_price", "discount_percent"]
    readonly_fields = []


class SocialLinkInline(admin.TabularInline):
    """Tabular inline for author social links."""
    model = SocialLink
    extra = 1
    fields = ["platform", "url", "follower_count"]


class ContentFileInline(GenericStackedInline):
    """Stacked inline for content file attachments."""
    model = ContentFile
    extra = 1
    fields = ["file"]
    can_delete = True


# ============================================================================
# ADMIN CLASSES - Blog Domain
# ============================================================================


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin interface for Author model."""
    list_display = ["name", "email", "follower_count", "post_count", "created_at"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
    search_fields = ["name", "email", "phone"]
    readonly_fields = ["created_at", "updated_at"]
    inlines = [SocialLinkInline]

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "email", "phone", "bio")
        }),
        ("Profile", {
            "fields": ("avatar", "follower_count")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def post_count(self, obj):
        count = obj.posts.count()
        return format_html(
            '<span style="background-color: #ddd; padding: 3px 8px; border-radius: 3px;">{}</span>',
            count
        )
    post_count.short_description = "Posts"

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(post_count=Count('posts'))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin interface for Category model."""
    list_display = ["name", "slug", "display_order", "post_count", "created_at"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["display_order", "name"]

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "slug", "description")
        }),
        ("Presentation", {
            "fields": ("icon", "display_order")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = "Posts"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin interface for Tag model."""
    list_display = ["name", "slug", "created_at"]
    list_filter = ["created_at"]
    date_hierarchy = "created_at"
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at"]
    ordering = ["name"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Admin interface for Post model with comprehensive configuration."""
    list_display = ["title", "author", "status_badge", "featured", "published_at", "view_count"]
    list_filter = ["status", "featured", "allow_comments", "published_at", "author", "categories"]
    date_hierarchy = "published_at"
    search_fields = ["title", "content", "excerpt", "author__name"]
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ["created_at", "updated_at", "view_count"]
    inlines = [CommentInline, PostVersionInline, ContentFileInline]
    filter_horizontal = ["categories", "tags"]

    fieldsets = (
        ("Post Information", {
            "fields": ("title", "slug", "author", "status")
        }),
        ("Content", {
            "fields": ("excerpt", "content", "featured", "allow_comments")
        }),
        ("Media", {
            "fields": ("featured_image", "thumbnail")
        }),
        ("Publishing", {
            "fields": ("published_at", "view_count")
        }),
        ("Categories & Tags", {
            "fields": ("categories", "tags")
        }),
        ("SEO", {
            "fields": ("meta_description", "meta_keywords"),
            "classes": ("collapse",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    actions = ["mark_published", "mark_draft", "feature_posts"]

    def status_badge(self, obj):
        colors = {
            "draft": "#999",
            "published": "#28a745",
            "archived": "#6c757d"
        }
        color = colors.get(obj.status, "#999")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"

    @admin.action(description="Mark selected posts as published")
    def mark_published(self, request, queryset):
        count = queryset.update(status="published")
        self.message_user(request, f"{count} posts marked as published.")

    @admin.action(description="Mark selected posts as draft")
    def mark_draft(self, request, queryset):
        count = queryset.update(status="draft")
        self.message_user(request, f"{count} posts marked as draft.")

    @admin.action(description="Feature selected posts")
    def feature_posts(self, request, queryset):
        count = queryset.update(featured=True)
        self.message_user(request, f"{count} posts featured.")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface for Comment model."""
    list_display = ["author", "post", "rating_stars", "is_approved", "created_at"]
    list_filter = ["is_approved", "rating", "created_at", "post__author"]
    date_hierarchy = "created_at"
    search_fields = ["content", "author__name", "post__title"]
    readonly_fields = ["created_at", "updated_at"]
    actions = ["approve_comments", "reject_comments"]

    fieldsets = (
        ("Comment Content", {
            "fields": ("post", "parent", "author", "content")
        }),
        ("Rating & Approval", {
            "fields": ("rating", "is_approved")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def rating_stars(self, obj):
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)
        return format_html(
            '<span style="color: #ffc107; font-size: 14px;">{}</span>',
            stars
        )
    rating_stars.short_description = "Rating"

    @admin.action(description="Approve selected comments")
    def approve_comments(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f"{count} comments approved.")

    @admin.action(description="Reject selected comments")
    def reject_comments(self, request, queryset):
        count = queryset.update(is_approved=False)
        self.message_user(request, f"{count} comments rejected.")


@admin.register(PostAnalytics)
class PostAnalyticsAdmin(admin.ModelAdmin):
    """Admin interface for PostAnalytics model."""
    list_display = ["post", "views_today", "likes", "shares", "last_updated"]
    list_filter = ["last_updated"]
    search_fields = ["post__title"]
    readonly_fields = ["post", "last_updated"]
    date_hierarchy = "last_updated"


@admin.register(PostVersion)
class PostVersionAdmin(admin.ModelAdmin):
    """Admin interface for PostVersion model."""
    list_display = ["post", "version_number", "author", "created_at"]
    list_filter = ["created_at", "post"]
    search_fields = ["post__title"]
    readonly_fields = ["post", "version_number", "content_snapshot", "author", "created_at"]
    date_hierarchy = "created_at"


# ============================================================================
# ADMIN CLASSES - E-Commerce Domain
# ============================================================================


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    list_display = ["name", "sku", "price_display", "stock_status", "is_featured", "created_at"]
    list_filter = ["is_active", "is_featured", "category", "created_at"]
    date_hierarchy = "created_at"
    search_fields = ["name", "sku", "barcode", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]
    inlines = [ProductImageInline, ProductAttributeValueInline, ProductReviewInline, ContentFileInline]
    filter_horizontal = ["tags"]
    actions = ["feature_products", "activate_products", "deactivate_products"]

    fieldsets = (
        ("Product Information", {
            "fields": ("name", "slug", "category", "description", "short_description")
        }),
        ("Identifiers", {
            "fields": ("sku", "barcode")
        }),
        ("Pricing", {
            "fields": ("price", "sale_price", "cost")
        }),
        ("Inventory", {
            "fields": ("stock", "reorder_level")
        }),
        ("Dimensions & Weight", {
            "fields": ("weight", "length", "width", "height"),
            "classes": ("collapse",)
        }),
        ("Media", {
            "fields": ("product_image",)
        }),
        ("Status", {
            "fields": ("is_active", "is_featured")
        }),
        ("Tags", {
            "fields": ("tags",)
        }),
        ("SEO", {
            "fields": ("meta_description", "meta_keywords"),
            "classes": ("collapse",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def price_display(self, obj):
        if obj.sale_price:
            return format_html(
                '<span style="text-decoration: line-through;">${}</span> <span style="color: #28a745; font-weight: bold;">${}</span>',
                obj.price,
                obj.sale_price
            )
        return f"${obj.price}"
    price_display.short_description = "Price"

    def stock_status(self, obj):
        if obj.stock == 0:
            return mark_safe('<span style="color: #dc3545;">Out of Stock</span>')
        elif obj.stock < obj.reorder_level:
            return format_html('<span style="color: #ffc107;">Low Stock ({})</span>', obj.stock)
        return format_html('<span style="color: #28a745;">In Stock ({})</span>', obj.stock)
    stock_status.short_description = "Stock Status"

    @admin.action(description="Feature selected products")
    def feature_products(self, request, queryset):
        count = queryset.update(is_featured=True)
        self.message_user(request, f"{count} products featured.")

    @admin.action(description="Activate selected products")
    def activate_products(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} products activated.")

    @admin.action(description="Deactivate selected products")
    def deactivate_products(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} products deactivated.")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin interface for ProductImage model."""
    list_display = ["product", "image_thumbnail", "alt_text", "sort_order"]
    list_filter = ["product", "sort_order"]
    search_fields = ["product__name", "alt_text"]
    ordering = ["product", "sort_order"]

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.image.url
            )
        return "No image"
    image_thumbnail.short_description = "Image"


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """Admin interface for ProductAttribute model."""
    list_display = ["name", "value_count"]
    search_fields = ["name", "description"]

    def value_count(self, obj):
        return obj.values.count()
    value_count.short_description = "Values"


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    """Admin interface for ProductAttributeValue model."""
    list_display = ["product", "attribute", "value"]
    list_filter = ["attribute", "product"]
    search_fields = ["product__name", "attribute__name", "value"]


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """Admin interface for ProductReview model."""
    list_display = ["product", "author", "rating_stars", "is_verified_purchase", "created_at"]
    list_filter = ["rating", "is_verified_purchase", "created_at"]
    date_hierarchy = "created_at"
    search_fields = ["product__name", "author__name", "title", "content"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("Review Information", {
            "fields": ("product", "author", "rating")
        }),
        ("Content", {
            "fields": ("title", "content")
        }),
        ("Engagement", {
            "fields": ("helpful_count", "is_verified_purchase")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def rating_stars(self, obj):
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)
        return format_html(
            '<span style="color: #ffc107; font-size: 14px;">{}</span> ({})',
            stars,
            obj.rating
        )
    rating_stars.short_description = "Rating"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    list_display = ["order_number", "customer", "status_badge", "total_amount", "created_at"]
    list_filter = ["status", "created_at", "customer"]
    date_hierarchy = "created_at"
    search_fields = ["order_number", "customer__name", "tracking_number"]
    readonly_fields = ["created_at", "updated_at", "order_number"]
    inlines = [OrderItemInline]
    actions = ["mark_shipped", "mark_delivered", "mark_cancelled"]

    fieldsets = (
        ("Order Information", {
            "fields": ("order_number", "customer", "status")
        }),
        ("Amounts", {
            "fields": ("total_amount", "shipping_cost", "discount_amount")
        }),
        ("Shipping", {
            "fields": ("shipping_address", "billing_address", "tracking_number", "expected_delivery")
        }),
        ("Notes", {
            "fields": ("notes",)
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    def status_badge(self, obj):
        colors = {
            "pending": "#ffc107",
            "confirmed": "#17a2b8",
            "shipped": "#007bff",
            "delivered": "#28a745",
            "cancelled": "#dc3545"
        }
        color = colors.get(obj.status, "#999")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"

    @admin.action(description="Mark selected orders as shipped")
    def mark_shipped(self, request, queryset):
        count = queryset.update(status="shipped")
        self.message_user(request, f"{count} orders marked as shipped.")

    @admin.action(description="Mark selected orders as delivered")
    def mark_delivered(self, request, queryset):
        count = queryset.update(status="delivered")
        self.message_user(request, f"{count} orders marked as delivered.")

    @admin.action(description="Mark selected orders as cancelled")
    def mark_cancelled(self, request, queryset):
        count = queryset.update(status="cancelled")
        self.message_user(request, f"{count} orders marked as cancelled.")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin interface for OrderItem model."""
    list_display = ["order", "product", "quantity", "unit_price", "discount_percent"]
    list_filter = ["order", "product"]
    search_fields = ["order__order_number", "product__name"]
    readonly_fields = ["order", "product"]


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    """Admin interface for Coupon model."""
    list_display = ["code", "discount_display", "times_used", "max_uses", "valid_status"]
    list_filter = ["discount_type", "valid_from", "valid_until"]
    date_hierarchy = "valid_until"
    search_fields = ["code", "description"]
    filter_horizontal = ["products"]
    readonly_fields = ["times_used"]

    fieldsets = (
        ("Coupon Information", {
            "fields": ("code", "description")
        }),
        ("Discount", {
            "fields": ("discount_type", "discount_value")
        }),
        ("Usage", {
            "fields": ("max_uses", "times_used")
        }),
        ("Validity", {
            "fields": ("valid_from", "valid_until")
        }),
        ("Products", {
            "fields": ("products",),
            "classes": ("collapse",)
        }),
    )

    def discount_display(self, obj):
        if obj.discount_type == "percentage":
            return f"{obj.discount_value}%"
        return f"${obj.discount_value}"
    discount_display.short_description = "Discount"

    def valid_status(self, obj):
        from django.utils import timezone
        now = timezone.now()
        if now < obj.valid_from:
            return mark_safe('<span style="color: #999;">Upcoming</span>')
        elif now > obj.valid_until:
            return mark_safe('<span style="color: #dc3545;">Expired</span>')
        return mark_safe('<span style="color: #28a745;">Active</span>')
    valid_status.short_description = "Status"


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Admin interface for Wishlist model."""
    list_display = ["user", "product_count", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["user__name"]
    filter_horizontal = ["products"]

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = "Products"


# ============================================================================
# ADMIN CLASSES - Cross-Domain Models
# ============================================================================


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Admin interface for Rating model."""
    list_display = ["user", "content_object", "rating_stars", "created_at"]
    list_filter = ["rating", "content_type", "created_at"]
    search_fields = ["user__name"]
    readonly_fields = ["content_type", "object_id", "user", "created_at"]
    date_hierarchy = "created_at"

    def rating_stars(self, obj):
        stars = "★" * obj.rating + "☆" * (5 - obj.rating)
        return format_html(
            '<span style="color: #ffc107; font-size: 14px;">{}</span>',
            stars
        )
    rating_stars.short_description = "Rating"


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """Admin interface for SocialLink model."""
    list_display = ["author", "platform", "follower_count", "url_link"]
    list_filter = ["platform", "author"]
    search_fields = ["author__name", "url"]

    def url_link(self, obj):
        return format_html('<a href="{}" target="_blank">View</a>', obj.url)
    url_link.short_description = "Link"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin interface for Subscription model."""
    list_display = ["user", "category", "digest_frequency", "receive_digest", "created_at"]
    list_filter = ["digest_frequency", "receive_digest", "category", "created_at"]
    search_fields = ["user__name", "category__name"]
    date_hierarchy = "created_at"


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""
    list_display = ["user", "notification_type", "read_status", "created_at"]
    list_filter = ["notification_type", "read_at", "created_at"]
    search_fields = ["user__name", "message"]
    readonly_fields = ["created_at"]
    date_hierarchy = "created_at"
    actions = ["mark_as_read", "mark_as_unread"]

    fieldsets = (
        ("Notification", {
            "fields": ("user", "notification_type", "message")
        }),
        ("Status", {
            "fields": ("read_at",)
        }),
        ("Timestamp", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )

    def read_status(self, obj):
        if obj.read_at:
            return mark_safe('<span style="color: #999;">Read</span>')
        return mark_safe('<span style="color: #28a745; font-weight: bold;">Unread</span>')
    read_status.short_description = "Status"

    @admin.action(description="Mark selected as read")
    def mark_as_read(self, request, queryset):
        from django.utils import timezone
        count = queryset.update(read_at=timezone.now())
        self.message_user(request, f"{count} notifications marked as read.")

    @admin.action(description="Mark selected as unread")
    def mark_as_unread(self, request, queryset):
        count = queryset.update(read_at=None)
        self.message_user(request, f"{count} notifications marked as unread.")
