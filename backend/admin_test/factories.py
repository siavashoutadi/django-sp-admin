import factory
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime, timedelta
import random

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
    Rating,
    SocialLink,
    Subscription,
    Notification,
    ContentFile,
)

# Meaningful data pools
AUTHOR_NAMES = [
    "Sarah Johnson", "Michael Chen", "Emma Williams", "David Brown", "Lisa Anderson",
    "James Thompson", "Rachel Green", "Chris Martinez", "Sophie Taylor", "Tom Miller"
]

AUTHOR_EMAILS = [
    "sarah@example.com", "mchen@example.com", "emma.w@example.com", "dbrown@example.com",
    "lisa.a@example.com", "jthompson@example.com", "rachel@example.com", "cmartinez@example.com",
    "sophie@example.com", "tmiller@example.com"
]

AUTHOR_BIOS = [
    "Technology writer and digital innovator passionate about web development.",
    "Full-stack developer with 10+ years of experience in building scalable applications.",
    "Product strategist focused on user experience and business growth.",
    "Marketing specialist helping brands tell their story through content.",
    "Entrepreneur and startup founder with multiple successful exits.",
    "UX researcher dedicated to understanding user behavior and needs.",
    "Data scientist turning insights into actionable business strategies.",
    "Content creator producing high-quality technical tutorials and guides.",
]

CATEGORY_NAMES = [
    "Technology", "Business", "Lifestyle", "Design", "Marketing", "Development",
    "Productivity", "Innovation"
]

CATEGORY_DESCRIPTIONS = {
    "Technology": "Latest trends in tech, gadgets, and digital innovation",
    "Business": "Business strategies, entrepreneurship, and market insights",
    "Lifestyle": "Personal growth, wellness, and daily life optimization",
    "Design": "UI/UX design, visual design, and creative thinking",
    "Marketing": "Digital marketing strategies, growth tactics, and campaigns",
    "Development": "Software development, coding tutorials, and best practices",
    "Productivity": "Tools, techniques, and systems for increased productivity",
    "Innovation": "Emerging technologies and disruptive business models",
}

TAG_NAMES = [
    "ai", "machine-learning", "python", "javascript", "react", "django",
    "startup", "growth-hacking", "seo", "content-marketing", "web-design",
    "mobile-app", "cloud-computing", "agile", "devops", "cryptocurrency"
]

POST_TITLES = [
    "Getting Started with Django REST Framework",
    "10 Essential JavaScript Patterns Every Developer Should Know",
    "The Complete Guide to Building Scalable Microservices",
    "How to Launch Your First Product in 30 Days",
    "Machine Learning for Beginners: A Practical Guide",
    "Best Practices for Team Communication in Remote Environments",
    "Understanding React Hooks: useContext and useReducer",
    "SEO Tips That Actually Work in 2026",
    "Building a Successful SaaS Business from Scratch",
    "The Future of Web Development: Web3 and Beyond",
    "Data Privacy Best Practices for Your Application",
    "Creating Accessible Websites: A Developer's Guide",
    "Scaling PostgreSQL: Tips and Tricks from Experience",
    "The Psychology Behind User Interface Design",
    "Mastering Git: Advanced Workflows for Teams",
]

PRODUCT_NAMES = [
    "Pro Developer Keyboard - Mechanical RGB", "Wireless Gaming Mouse Ultra",
    "4K Webcam with AI Background Removal", "USB-C Hub with 7-in-1 Connectivity",
    "Noise-Canceling Bluetooth Headphones", "27-inch QHD Monitor - USB-C",
    "Laptop Stand - Adjustable Aluminum", "Mechanical Keyboard Blue Switch",
    "Premium Office Chair - Ergonomic Design", "Docking Station - 15-Port",
    "MacBook Pro 16\" - M3 Max", "iPad Pro 12.9\" WiFi + Cellular",
    "Apple AirPods Pro Gen 2", "Magic Keyboard for iPad", "Studio Display",
]

PRODUCT_CATEGORIES = {
    "Technology": "Electronics & Computers",
    "Business": "Office Equipment",
    "Lifestyle": "Home & Living",
    "Design": "Creative Tools",
}

PRODUCT_DESCRIPTIONS = [
    "Premium quality product designed for professional use with exceptional performance.",
    "High-end device featuring the latest technology and innovative design.",
    "Reliable and durable product backed by comprehensive warranty.",
    "Top-rated product with excellent customer reviews and support.",
    "Professional-grade equipment trusted by industry experts worldwide.",
]

COMPANY_NAMES = ["Tech Corp Inc", "Digital Solutions Ltd", "Blue Mountain Software", "Cloud Nine Systems"]

NOTIFICATION_MESSAGES = {
    "order_confirmation": "Your order #{order_id} has been confirmed and will ship soon.",
    "shipment_update": "Your order #{order_id} has been shipped! Track it with: {tracking}",
    "comment_reply": "{author} replied to your comment on '{post_title}'",
    "new_post": "New article by {author}: {post_title}",
    "product_available": "'{product_name}' is back in stock!",
}

SOCIAL_PLATFORMS_FALLBACK = ["twitter", "facebook", "linkedin", "instagram", "youtube", "github"]


# ============================================================================
# BLOG DOMAIN FACTORIES
# ============================================================================


class AuthorFactory(factory.django.DjangoModelFactory):
    """Factory for creating Author objects with meaningful data."""

    class Meta:
        model = Author

    name = factory.LazyAttribute(lambda obj: random.choice(AUTHOR_NAMES))
    email = factory.LazyAttribute(lambda obj: random.choice(AUTHOR_EMAILS))
    bio = factory.LazyAttribute(lambda obj: random.choice(AUTHOR_BIOS))
    avatar = factory.django.ImageField(color="blue")
    phone = factory.LazyAttribute(lambda obj: f"+1-555-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}")
    follower_count = factory.LazyAttribute(lambda obj: random.randint(100, 50000))
    created_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(1, 365))
    )
    updated_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(0, 30))
    )


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory for creating Category objects with meaningful data."""

    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda obj: random.choice(CATEGORY_NAMES))
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))
    description = factory.LazyAttribute(lambda obj: CATEGORY_DESCRIPTIONS.get(obj.name, ""))
    icon = factory.django.ImageField(color="green")
    display_order = factory.Sequence(lambda n: n)
    created_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(30, 365))
    )
    updated_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(0, 30))
    )


class TagFactory(factory.django.DjangoModelFactory):
    """Factory for creating Tag objects with meaningful data."""

    class Meta:
        model = Tag

    name = factory.LazyAttribute(lambda obj: random.choice(TAG_NAMES))
    slug = factory.LazyAttribute(lambda obj: obj.name)
    created_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(30, 365))
    )


class PostFactory(factory.django.DjangoModelFactory):
    """Factory for creating Post objects with meaningful data."""

    class Meta:
        model = Post

    title = factory.LazyAttribute(lambda obj: random.choice(POST_TITLES))
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title)[:50])
    author = factory.SubFactory(AuthorFactory)
    excerpt = factory.LazyAttribute(
        lambda obj: "Read this comprehensive guide covering the essential concepts, best practices, "
                   "and practical examples to help you master this topic."
    )
    content = factory.LazyAttribute(
        lambda obj:
        """
        ## Introduction
        This comprehensive guide covers everything you need to know about this topic.

        ## Key Concepts
        Learn the fundamental principles and best practices that professionals use.

        ## Implementation
        Follow step-by-step instructions with practical examples.

        ## Conclusion
        Master these techniques and apply them to your projects immediately.
        """
    )
    featured_image = factory.django.ImageField(color="red")
    thumbnail = factory.django.ImageField(color="yellow")
    status = factory.LazyAttribute(lambda obj: random.choice(["draft", "published", "published"]))
    featured = factory.LazyAttribute(lambda obj: random.choice([True, False, False, False]))
    allow_comments = True
    published_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(0, 90)) if obj.status == "published" else None
    )
    view_count = factory.LazyAttribute(lambda obj: random.randint(100, 5000))
    meta_description = factory.LazyAttribute(
        lambda obj: f"Learn about {obj.title.lower()} with this comprehensive guide"
    )
    meta_keywords = factory.LazyAttribute(lambda obj: ", ".join(random.sample(TAG_NAMES, 3)))
    created_at = factory.LazyAttribute(
        lambda obj: obj.published_at - timedelta(days=random.randint(1, 30)) if obj.published_at else timezone.now() - timedelta(days=random.randint(1, 90))
    )
    updated_at = factory.LazyAttribute(
        lambda obj: obj.published_at + timedelta(days=random.randint(0, 30)) if obj.published_at else timezone.now()
    )

    @factory.post_generation
    def categories(obj, create, extracted, **kwargs):
        """Add random categories to the post."""
        if not create:
            return
        if extracted:
            for category in extracted:
                obj.categories.add(category)
        else:
            categories = Category.objects.order_by("?")[: random.randint(1, 3)]
            for category in categories:
                obj.categories.add(category)

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Add random tags to the post."""
        if not create:
            return
        if extracted:
            for tag in extracted:
                obj.tags.add(tag)
        else:
            tags = Tag.objects.order_by("?")[: random.randint(2, 5)]
            for tag in tags:
                obj.tags.add(tag)


COMMENT_TEXTS = [
    "This is exactly what I needed! Thanks for sharing.",
    "Great article, very helpful and well written.",
    "I disagree with some points, but overall good content.",
    "Can you elaborate more on the advanced concepts?",
    "Bookmarking this for later reference.",
    "This helped me solve my problem. Appreciate it!",
    "Well explained with good examples.",
    "Would love to see more articles like this.",
]


class CommentFactory(factory.django.DjangoModelFactory):
    """Factory for creating Comment objects with meaningful data."""

    class Meta:
        model = Comment

    post = factory.SubFactory(PostFactory)
    author = factory.SubFactory(AuthorFactory)
    parent = None
    content = factory.LazyAttribute(lambda obj: random.choice(COMMENT_TEXTS))
    rating = factory.LazyAttribute(lambda obj: random.choice([5, 5, 5, 4, 4, 3]))
    is_approved = True
    created_at = factory.LazyAttribute(
        lambda obj: obj.post.created_at + timedelta(days=random.randint(1, 30))
    )
    updated_at = factory.LazyAttribute(
        lambda obj: obj.created_at + timedelta(hours=random.randint(0, 72))
    )


class PostAnalyticsFactory(factory.django.DjangoModelFactory):
    """Factory for creating PostAnalytics objects (OneToOne)."""

    class Meta:
        model = PostAnalytics

    post = factory.SubFactory(PostFactory)
    views_today = factory.LazyAttribute(lambda obj: obj.post.view_count // random.randint(5, 20))
    likes = factory.LazyAttribute(lambda obj: int(obj.post.view_count * random.uniform(0.02, 0.08)))
    shares = factory.LazyAttribute(lambda obj: int(obj.post.view_count * random.uniform(0.005, 0.02)))
    last_updated = factory.LazyAttribute(lambda obj: timezone.now())


class PostVersionFactory(factory.django.DjangoModelFactory):
    """Factory for creating PostVersion objects."""

    class Meta:
        model = PostVersion

    post = factory.SubFactory(PostFactory)
    version_number = factory.Sequence(lambda n: n + 1)
    content_snapshot = factory.LazyAttribute(
        lambda obj: "Initial version" if obj.version_number == 1 else "Updated with improved content and examples."
    )
    author = factory.SubFactory(AuthorFactory)
    created_at = factory.LazyAttribute(
        lambda obj: obj.post.created_at + timedelta(days=obj.version_number * 5)
    )


# ============================================================================
# E-COMMERCE DOMAIN FACTORIES
# ============================================================================


class ProductFactory(factory.django.DjangoModelFactory):
    """Factory for creating Product objects with meaningful data."""

    class Meta:
        model = Product

    name = factory.LazyAttribute(lambda obj: random.choice(PRODUCT_NAMES))
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name)[:50])
    description = factory.LazyAttribute(lambda obj: random.choice(PRODUCT_DESCRIPTIONS))
    short_description = factory.LazyAttribute(
        lambda obj: "Premium quality product with excellent features and durability."
    )
    category = factory.LazyAttribute(lambda obj: Category.objects.first())
    price = factory.LazyAttribute(lambda obj: float(random.randint(49, 2000)))
    sale_price = factory.LazyAttribute(
        lambda obj: obj.price * 0.85 if random.choice([True, False, False]) else None
    )
    cost = factory.LazyAttribute(lambda obj: obj.price * 0.4)
    sku = factory.LazyAttribute(lambda obj: f"SKU{random.randint(100000, 999999)}")
    barcode = factory.LazyAttribute(lambda obj: f"{random.randint(1000000000000, 9999999999999)}")
    is_active = True
    is_featured = factory.LazyAttribute(lambda obj: random.choice([True, False, False, False]))
    stock = factory.LazyAttribute(lambda obj: random.randint(5, 500))
    reorder_level = factory.LazyAttribute(lambda obj: random.randint(5, 50))
    weight = factory.LazyAttribute(lambda obj: float(random.randint(1, 50)))
    length = factory.LazyAttribute(lambda obj: float(random.randint(10, 100)))
    width = factory.LazyAttribute(lambda obj: float(random.randint(5, 50)))
    height = factory.LazyAttribute(lambda obj: float(random.randint(5, 50)))
    product_image = factory.django.ImageField(color="purple")
    meta_description = factory.LazyAttribute(
        lambda obj: f"{obj.name} - Premium quality at best price"
    )
    meta_keywords = factory.LazyAttribute(
        lambda obj: "electronics, gadget, technology, professional"
    )
    created_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(1, 365))
    )
    updated_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(0, 30))
    )

    @factory.post_generation
    def tags(obj, create, extracted, **kwargs):
        """Add random tags to the product."""
        if not create:
            return
        if extracted:
            for tag in extracted:
                obj.tags.add(tag)
        else:
            tags = Tag.objects.order_by("?")[: random.randint(1, 4)]
            for tag in tags:
                obj.tags.add(tag)


class ProductImageFactory(factory.django.DjangoModelFactory):
    """Factory for creating ProductImage objects."""

    class Meta:
        model = ProductImage

    product = factory.SubFactory(ProductFactory)
    image = factory.django.ImageField(color="orange")
    alt_text = factory.LazyAttribute(lambda obj: f"{obj.product.name} - Product Image")
    sort_order = factory.Sequence(lambda n: n)


ATTRIBUTE_NAMES = ["Size", "Color", "Material", "Warranty", "Connectivity"]
ATTRIBUTE_VALUES = {
    "Size": ["Small", "Medium", "Large", "XL", "13\"", "15\"", "17\""],
    "Color": ["Black", "White", "Silver", "Gold", "Space Gray", "Blue"],
    "Material": ["Aluminum", "Plastic", "Metal", "Carbon Fiber", "Stainless Steel"],
    "Warranty": ["1 Year", "2 Years", "3 Years", "Lifetime"],
    "Connectivity": ["USB-C", "Wireless", "Bluetooth", "USB 3.0"],
}


class ProductAttributeFactory(factory.django.DjangoModelFactory):
    """Factory for creating ProductAttribute objects."""

    class Meta:
        model = ProductAttribute

    name = factory.LazyAttribute(lambda obj: random.choice(ATTRIBUTE_NAMES))
    description = factory.LazyAttribute(
        lambda obj: f"Select the {obj.name.lower()} for your product"
    )


class ProductAttributeValueFactory(factory.django.DjangoModelFactory):
    """Factory for creating ProductAttributeValue objects (M2M through)."""

    class Meta:
        model = ProductAttributeValue

    product = factory.SubFactory(ProductFactory)
    attribute = factory.SubFactory(ProductAttributeFactory)
    value = factory.LazyAttribute(
        lambda obj: random.choice(ATTRIBUTE_VALUES.get(obj.attribute.name, ["Standard"]))
    )


REVIEW_TITLES = [
    "Excellent product, highly recommended",
    "Great quality at this price point",
    "Works as described, very satisfied",
    "Good value for money",
    "Perfect for my needs",
    "Fast shipping and great customer service",
]

REVIEW_TEXTS = [
    "I'm very happy with this purchase. It arrived quickly and works perfectly.",
    "Great product! Exceeded my expectations in terms of quality and performance.",
    "Exactly what I was looking for. Would definitely buy again.",
    "Good quality and reasonable price. Recommended!",
    "Fast delivery and excellent packaging. The product is fantastic.",
]


class ProductReviewFactory(factory.django.DjangoModelFactory):
    """Factory for creating ProductReview objects."""

    class Meta:
        model = ProductReview

    product = factory.SubFactory(ProductFactory)
    author = factory.SubFactory(AuthorFactory)
    rating = factory.LazyAttribute(lambda obj: random.choice([5, 5, 5, 4, 4, 3]))
    title = factory.LazyAttribute(lambda obj: random.choice(REVIEW_TITLES))
    content = factory.LazyAttribute(lambda obj: random.choice(REVIEW_TEXTS))
    helpful_count = factory.LazyAttribute(lambda obj: random.randint(0, 50))
    is_verified_purchase = factory.LazyAttribute(lambda obj: random.choice([True, True, False]))
    created_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(1, 180))
    )
    updated_at = factory.LazyAttribute(
        lambda obj: obj.created_at + timedelta(days=random.randint(0, 30))
    )


class OrderFactory(factory.django.DjangoModelFactory):
    """Factory for creating Order objects."""

    class Meta:
        model = Order

    order_number = factory.LazyAttribute(lambda obj: f"ORD-{random.randint(100000, 999999)}")
    customer = factory.SubFactory(AuthorFactory)
    status = factory.LazyAttribute(
        lambda obj: random.choice(["pending", "pending", "confirmed", "confirmed", "shipped", "delivered"])
    )
    total_amount = factory.LazyAttribute(lambda obj: float(random.randint(50, 5000)))
    shipping_cost = factory.LazyAttribute(lambda obj: float(random.choice([0, 5.99, 9.99, 15.99])))
    discount_amount = factory.LazyAttribute(
        lambda obj: float(random.randint(0, int(obj.total_amount * 0.2)))
    )
    shipping_address = factory.LazyAttribute(
        lambda obj: f"{random.randint(1, 9999)} Main Street, New York, NY 10001"
    )
    billing_address = factory.LazyAttribute(
        lambda obj: f"{random.randint(1, 9999)} Oak Avenue, Los Angeles, CA 90001"
    )
    notes = factory.LazyAttribute(
        lambda obj: random.choice([
            "Please leave at front door",
            "Handle with care",
            "Signature required",
            "",
            "Please wrap as gift",
        ])
    )
    tracking_number = factory.LazyAttribute(
        lambda obj: f"TRK{random.randint(1000000, 9999999)}"
    )
    expected_delivery = factory.LazyAttribute(
        lambda obj: timezone.now().date() + timedelta(days=random.randint(3, 14))
    )
    created_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(0, 60))
    )
    updated_at = factory.LazyAttribute(
        lambda obj: obj.created_at + timedelta(days=random.randint(0, 10))
    )


class OrderItemFactory(factory.django.DjangoModelFactory):
    """Factory for creating OrderItem objects."""

    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.LazyAttribute(lambda obj: random.randint(1, 5))
    unit_price = factory.LazyAttribute(
        lambda obj: float(random.randint(20, 1000))
    )
    discount_percent = factory.LazyAttribute(lambda obj: float(random.choice([0, 0, 5, 10, 15])))


class CouponFactory(factory.django.DjangoModelFactory):
    """Factory for creating Coupon objects."""

    class Meta:
        model = Coupon

    code = factory.LazyAttribute(lambda obj: f"SAVE{random.randint(10, 50)}")
    description = factory.LazyAttribute(
        lambda obj: random.choice([
            "Get discount on all products",
            "Limited time offer",
            "Winter sale coupon",
            "First-time buyer discount",
        ])
    )
    discount_type = factory.LazyAttribute(lambda obj: random.choice(["percentage", "percentage", "fixed"]))
    discount_value = factory.LazyAttribute(lambda obj: float(random.choice([5, 10, 15, 20, 25, 50])))
    max_uses = factory.LazyAttribute(lambda obj: random.randint(10, 1000))
    times_used = factory.LazyAttribute(lambda obj: random.randint(0, 100))
    valid_from = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(0, 30))
    )
    valid_until = factory.LazyAttribute(
        lambda obj: timezone.now() + timedelta(days=random.randint(10, 90))
    )

    @factory.post_generation
    def products(obj, create, extracted, **kwargs):
        """Add random products to the coupon."""
        if not create:
            return
        if extracted:
            for product in extracted:
                obj.products.add(product)
        else:
            if random.choice([True, False, False]):
                products = Product.objects.order_by("?")[: random.randint(1, 3)]
                for product in products:
                    obj.products.add(product)


class WishlistFactory(factory.django.DjangoModelFactory):
    """Factory for creating Wishlist objects (OneToOne)."""

    class Meta:
        model = Wishlist

    user = factory.SubFactory(AuthorFactory)
    created_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(1, 365))
    )
    updated_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(0, 30))
    )

    @factory.post_generation
    def products(obj, create, extracted, **kwargs):
        """Add random products to the wishlist."""
        if not create:
            return
        if extracted:
            for product in extracted:
                obj.products.add(product)
        else:
            products = Product.objects.order_by("?")[: random.randint(3, 10)]
            for product in products:
                obj.products.add(product)


# ============================================================================
# CROSS-DOMAIN FACTORIES
# ============================================================================


class RatingFactory(factory.django.DjangoModelFactory):
    """Factory for creating Rating objects (using GenericForeignKey)."""

    class Meta:
        model = Rating

    user = factory.SubFactory(AuthorFactory)
    rating = factory.LazyAttribute(lambda obj: random.choice([5, 5, 4, 4, 3]))
    created_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(1, 90))
    )


SOCIAL_URLS = {
    "twitter": "https://twitter.com/{handle}",
    "facebook": "https://facebook.com/{handle}",
    "linkedin": "https://linkedin.com/in/{handle}",
    "instagram": "https://instagram.com/{handle}",
    "youtube": "https://youtube.com/@{handle}",
    "github": "https://github.com/{handle}",
}


class SocialLinkFactory(factory.django.DjangoModelFactory):
    """Factory for creating SocialLink objects."""

    class Meta:
        model = SocialLink

    author = factory.SubFactory(AuthorFactory)
    platform = factory.LazyAttribute(
        lambda obj: random.choice(SOCIAL_PLATFORMS_FALLBACK)
    )
    url = factory.LazyAttribute(
        lambda obj: SOCIAL_URLS.get(obj.platform, "https://example.com").format(
            handle=obj.author.name.lower().replace(" ", "")
        )
    )
    follower_count = factory.LazyAttribute(lambda obj: random.randint(100, 100000))


class SubscriptionFactory(factory.django.DjangoModelFactory):
    """Factory for creating Subscription objects."""

    class Meta:
        model = Subscription

    user = factory.SubFactory(AuthorFactory)
    category = factory.SubFactory(CategoryFactory)
    receive_digest = factory.LazyAttribute(lambda obj: random.choice([True, True, False]))
    digest_frequency = factory.LazyAttribute(
        lambda obj: random.choice(["daily", "weekly", "monthly"])
    )
    created_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(1, 180))
    )


class NotificationFactory(factory.django.DjangoModelFactory):
    """Factory for creating Notification objects."""

    class Meta:
        model = Notification

    user = factory.SubFactory(AuthorFactory)
    notification_type = factory.LazyAttribute(
        lambda obj: random.choice([
            "order_confirmation", "shipment_update", "comment_reply", "new_post"
        ])
    )
    message = factory.LazyAttribute(
        lambda obj: random.choice([
            "Your order has been confirmed!",
            "Your shipment is on the way.",
            "Someone replied to your comment.",
            "Check out the latest article.",
            "Your product is back in stock!",
        ])
    )
    read_at = factory.LazyAttribute(
        lambda obj: timezone.now() if random.choice([True, False, False]) else None
    )
    created_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(0, 30))
    )


class ContentFileFactory(factory.django.DjangoModelFactory):
    """Factory for creating ContentFile objects (using GenericForeignKey)."""

    class Meta:
        model = ContentFile

    file = factory.django.FileField()
    uploaded_at = factory.LazyAttribute(
        lambda obj: timezone.now() - timedelta(days=random.randint(0, 90))
    )
