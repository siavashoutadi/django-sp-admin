import uuid
from functools import cached_property

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Author(models.Model):
    """Blog and e-commerce author/user model."""

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, default="")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, default="")
    follower_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    """Category model for both blog posts and products."""

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, default="")
    icon = models.ImageField(upload_to="category_icons/", blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["display_order", "name"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Tag model for posts and products."""

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Blog post model with comprehensive fields."""

    class StatusChoices(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"

    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="posts/featured/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="posts/thumbnails/", blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT
    )
    featured = models.BooleanField(default=False, help_text="Display on homepage")
    allow_comments = models.BooleanField(default=True)

    published_at = models.DateTimeField(blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)

    categories = models.ManyToManyField(Category, related_name="posts", blank=True)
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True)

    meta_description = models.CharField(max_length=300, blank=True, default="")
    meta_keywords = models.CharField(max_length=300, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status", "-published_at"]),
            models.Index(fields=["author"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Blog post comment with nested reply support."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )
    content = models.TextField()
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["post", "is_approved"]),
        ]

    def __str__(self):
        return f"Comment by {self.author.name} on {self.post.title}"


class PostAnalytics(models.Model):
    """Analytics for posts - OneToOne relationship."""

    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="analytics")
    views_today = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Post Analytics"
        verbose_name_plural = "Post Analytics"

    def __str__(self):
        return f"Analytics for {self.post.title}"


class PostVersion(models.Model):
    """Version history for posts."""

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveIntegerField()
    content_snapshot = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Post Version"
        verbose_name_plural = "Post Versions"
        ordering = ["-version_number"]
        unique_together = [["post", "version_number"]]

    def __str__(self):
        return f"{self.post.title} - Version {self.version_number}"



# ============================================================================
# E-COMMERCE MODELS
# ============================================================================


class Product(models.Model):
    """E-commerce product model with comprehensive fields."""

    name = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True, default="")

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="products"
    )
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Product identifiers
    sku = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=100, blank=True, default="")

    # Status and inventory
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)
    reorder_level = models.PositiveIntegerField(default=10)

    # Dimensions and weight
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    length = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    width = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    # Media
    product_image = models.ImageField(upload_to="products/", blank=True, null=True)

    # SEO
    meta_description = models.CharField(max_length=300, blank=True, default="")
    meta_keywords = models.CharField(max_length=300, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["is_active", "-created_at"]),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Additional product images."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=300, blank=True, default="")
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
        ordering = ["sort_order"]

    def __str__(self):
        return f"Image for {self.product.name}"


class ProductAttribute(models.Model):
    """Product attributes for M2M through model."""

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Product Attribute"
        verbose_name_plural = "Product Attributes"

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """M2M through model connecting products and attributes."""

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attribute_values"
    )
    attribute = models.ForeignKey(
        ProductAttribute, on_delete=models.CASCADE, related_name="values"
    )
    value = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Product Attribute Value"
        verbose_name_plural = "Product Attribute Values"
        unique_together = [["product", "attribute"]]

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"


class ProductReview(models.Model):
    """Customer reviews for products."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="product_reviews")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    helpful_count = models.PositiveIntegerField(default=0)
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Reviews"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["product", "rating"]),
        ]

    def __str__(self):
        return f"Review by {self.author.name} for {self.product.name}"


class Order(models.Model):
    """Customer order model."""

    class StatusChoices(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    order_number = models.CharField(max_length=100, unique=True)
    customer = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="orders")

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    shipping_address = models.TextField()
    billing_address = models.TextField()

    notes = models.TextField(blank=True, default="")
    tracking_number = models.CharField(max_length=200, blank=True, default="")
    expected_delivery = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["status", "-created_at"]),
        ]

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    """Items in an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def __str__(self):
        return f"{self.product.name} in Order {self.order.order_number}"


class Coupon(models.Model):
    """Discount coupons."""

    class DiscountTypeChoices(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage (%)"
        FIXED = "fixed", "Fixed Amount ($)"

    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default="")
    discount_type = models.CharField(
        max_length=20,
        choices=DiscountTypeChoices.choices,
        default=DiscountTypeChoices.PERCENTAGE
    )
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_uses = models.PositiveIntegerField(blank=True, null=True)
    times_used = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    products = models.ManyToManyField(Product, blank=True, related_name="coupons")

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
        ordering = ["-valid_until"]

    def __str__(self):
        return self.code


class Wishlist(models.Model):
    """User wishlist for products."""

    user = models.OneToOneField(
        Author, on_delete=models.CASCADE, related_name="wishlist"
    )
    products = models.ManyToManyField(Product, related_name="wishlists")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return f"Wishlist for {self.user.name}"


# ============================================================================
# CROSS-DOMAIN MODELS
# ============================================================================


class ContentFile(models.Model):
    """Generic file attachment using GenericForeignKey."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    file = models.FileField(upload_to="content_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Content File"
        verbose_name_plural = "Content Files"

    def __str__(self):
        return f"File for {self.content_object}"


class Rating(models.Model):
    """Generic rating model using GenericForeignKey."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")

    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="ratings")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        unique_together = [["content_type", "object_id", "user"]]

    def __str__(self):
        return f"{self.rating}★ by {self.user.name}"


class SocialLink(models.Model):
    """Social media links for authors."""

    class PlatformChoices(models.TextChoices):
        TWITTER = "twitter", "Twitter"
        FACEBOOK = "facebook", "Facebook"
        LINKEDIN = "linkedin", "LinkedIn"
        INSTAGRAM = "instagram", "Instagram"
        YOUTUBE = "youtube", "YouTube"
        GITHUB = "github", "GitHub"

    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="social_links")
    platform = models.CharField(max_length=20, choices=PlatformChoices.choices)
    url = models.URLField()
    follower_count = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"
        unique_together = [["author", "platform"]]

    def __str__(self):
        return f"{self.author.name} - {self.get_platform_display()}"


class Subscription(models.Model):
    """Category subscription for digest emails."""

    class FrequencyChoices(models.TextChoices):
        DAILY = "daily", "Daily"
        WEEKLY = "weekly", "Weekly"
        MONTHLY = "monthly", "Monthly"

    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="subscriptions")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    receive_digest = models.BooleanField(default=True)
    digest_frequency = models.CharField(
        max_length=20,
        choices=FrequencyChoices.choices,
        default=FrequencyChoices.WEEKLY
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        unique_together = [["user", "category"]]

    def __str__(self):
        return f"{self.user.name} subscribed to {self.category.name}"


class Notification(models.Model):
    """User notifications."""

    class TypeChoices(models.TextChoices):
        ORDER_CONFIRMATION = "order_confirmation", "Order Confirmation"
        SHIPMENT_UPDATE = "shipment_update", "Shipment Update"
        COMMENT_REPLY = "comment_reply", "Comment Reply"
        NEW_POST = "new_post", "New Post"
        PRODUCT_AVAILABLE = "product_available", "Product Available"

    user = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="notifications")
    notification_type = models.CharField(
        max_length=50,
        choices=TypeChoices.choices
    )
    message = models.TextField()
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "read_at"]),
        ]

    def __str__(self):
        return f"Notification for {self.user.name}"
