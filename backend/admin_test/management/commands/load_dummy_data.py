from typing import Annotated
import random

import typer
from django_typer.management import TyperCommand, command
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify

from admin_test.factories import (
    AuthorFactory,
    CategoryFactory,
    TagFactory,
    PostFactory,
    CommentFactory,
    PostAnalyticsFactory,
    PostVersionFactory,
    ProductFactory,
    ProductImageFactory,
    ProductAttributeFactory,
    ProductAttributeValueFactory,
    ProductReviewFactory,
    OrderFactory,
    OrderItemFactory,
    CouponFactory,
    WishlistFactory,
    RatingFactory,
    SocialLinkFactory,
    SubscriptionFactory,
    NotificationFactory,
)
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


class Command(TyperCommand):
    """Load dummy data for admin test app - Blog + E-Commerce scenario"""

    @command()
    def seed(
        self,
        authors: Annotated[
            int,
            typer.Option("--authors", help="The number of authors to create"),
        ] = 5,
        categories: Annotated[
            int,
            typer.Option("--categories", help="The number of categories to create"),
        ] = 8,
        tags: Annotated[
            int,
            typer.Option("--tags", help="The number of tags to create"),
        ] = 15,
        posts: Annotated[
            int,
            typer.Option("--posts", help="The number of posts to create (1-500)"),
        ] = 20,
        comments_per_post: Annotated[
            int,
            typer.Option("--comments-per-post", help="Average number of comments per post"),
        ] = 3,
        products: Annotated[
            int,
            typer.Option("--products", help="The number of products to create"),
        ] = 25,
        orders: Annotated[
            int,
            typer.Option("--orders", help="The number of orders to create"),
        ] = 10,
        coupons: Annotated[
            int,
            typer.Option("--coupons", help="The number of coupons to create"),
        ] = 5,
        clear: Annotated[
            bool,
            typer.Option("--clear", help="Clear existing data before seeding"),
        ] = False,
    ):
        """
        Seed database with dummy data for Blog + E-Commerce models.
        """
        # Validate inputs
        if posts < 1 or posts > 500:
            typer.echo("❌ Posts count must be between 1 and 500")
            raise typer.Exit(1)

        if comments_per_post < 1 or comments_per_post > 20:
            typer.echo("❌ Comments per post must be between 1 and 20")
            raise typer.Exit(1)

        # Clear existing data if requested
        if clear:
            typer.echo("🗑️  Clearing existing data...")
            ContentFile.objects.all().delete()
            Notification.objects.all().delete()
            Subscription.objects.all().delete()
            SocialLink.objects.all().delete()
            Rating.objects.all().delete()
            Wishlist.objects.all().delete()
            Coupon.objects.all().delete()
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            ProductReview.objects.all().delete()
            ProductAttributeValue.objects.all().delete()
            ProductAttribute.objects.all().delete()
            ProductImage.objects.all().delete()
            Product.objects.all().delete()
            PostVersion.objects.all().delete()
            PostAnalytics.objects.all().delete()
            Comment.objects.all().delete()
            Post.objects.all().delete()
            Author.objects.all().delete()
            Category.objects.all().delete()
            Tag.objects.all().delete()
            typer.echo("✓ Data cleared\n")

        typer.echo("🌱 Starting data seeding...\n")

        # ====================================================================
        # BLOG DOMAIN
        # ====================================================================

        # Create Authors from predefined list
        typer.echo(f"👤 Creating authors...")
        from admin_test.factories import AUTHOR_NAMES, AUTHOR_EMAILS, AUTHOR_BIOS
        author_list = []
        for i, name in enumerate(AUTHOR_NAMES[:authors]):
            author, created = Author.objects.get_or_create(
                email=AUTHOR_EMAILS[i] if i < len(AUTHOR_EMAILS) else f"author{i}@example.com",
                defaults={
                    "name": name,
                    "bio": AUTHOR_BIOS[i % len(AUTHOR_BIOS)],
                }
            )
            if created:
                author_list.append(author)
        typer.echo(f"✓ Created {len(author_list)} new authors")

        # Create Categories from predefined list
        typer.echo(f"📁 Creating categories...")
        from admin_test.factories import CATEGORY_NAMES, CATEGORY_DESCRIPTIONS
        category_list = []
        for cat_name in CATEGORY_NAMES[:categories]:
            cat, created = Category.objects.get_or_create(
                name=cat_name,
                defaults={
                    "slug": slugify(cat_name),
                    "description": CATEGORY_DESCRIPTIONS.get(cat_name, ""),
                }
            )
            if created:
                category_list.append(cat)
        typer.echo(f"✓ Created {len(category_list)} new categories")

        # Create Tags from predefined list
        typer.echo(f"🏷️  Creating tags...")
        from admin_test.factories import TAG_NAMES, POST_TITLES, PRODUCT_NAMES
        tag_list = []
        for tag_name in TAG_NAMES[:tags]:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={"slug": slugify(tag_name)}
            )
            if created:
                tag_list.append(tag)
        typer.echo(f"✓ Created {len(tag_list)} new tags")

        # Create Posts with analytics, versions, and comments
        typer.echo(f"\n📝 Creating {posts} posts with nested data...")
        created_comments = 0
        created_analytics = 0
        created_versions = 0

        for i in range(posts):
            if (i + 1) % max(1, posts // 5) == 0:
                typer.echo(f"   ... {i + 1}/{posts} posts created")

            # Create post with existing author and unique slug
            author = random.choice(author_list)
            base_slug = slugify(random.choice(POST_TITLES))[:45]  # Leave room for counter
            unique_slug = f"{base_slug}-{i}"[:50]
            post = PostFactory.create(author=author, slug=unique_slug)

            # Create post analytics (OneToOne)
            try:
                PostAnalyticsFactory.create(post=post)
                created_analytics += 1
            except Exception:
                pass

            # Create post versions (history)
            num_versions = random.randint(1, 3)
            for v in range(num_versions):
                try:
                    PostVersionFactory.create(post=post, version_number=v + 1)
                    created_versions += 1
                except Exception:
                    pass

            # Create comments with nested replies
            num_comments = max(1, min(comments_per_post + (i % 3 - 1), 8))
            for c in range(num_comments):
                comment_author = random.choice(author_list)
                comment = CommentFactory.create(post=post, author=comment_author)
                created_comments += 1

                # Add nested replies (50% chance)
                if random.random() < 0.5 and c > 0:
                    for _ in range(random.randint(1, 2)):
                        try:
                            reply_author = random.choice(author_list)
                            CommentFactory.create(post=post, parent=comment, author=reply_author)
                            created_comments += 1
                        except Exception:
                            pass

        typer.echo(f"✓ Created {Post.objects.count()} posts total")
        typer.echo(f"✓ Created {created_comments} comments total (with nested replies)")
        typer.echo(f"✓ Created {created_analytics} post analytics")
        typer.echo(f"✓ Created {created_versions} post versions")

        # ====================================================================
        # E-COMMERCE DOMAIN
        # ====================================================================

        # Create Product Attributes
        typer.echo(f"\n🏷️  Creating product attributes...")
        attributes = []
        attr_names = ["Size", "Color", "Material", "Brand", "Warranty"]
        for attr_name in attr_names:
            try:
                attr = ProductAttributeFactory.create(name=attr_name)
                attributes.append(attr)
            except Exception:
                pass
        typer.echo(f"✓ Created {len(attributes)} product attributes")

        # Create Products with images, attributes, and reviews
        typer.echo(f"\n🛍️  Creating {products} products with related data...")
        created_images = 0
        created_attribute_values = 0
        created_reviews = 0

        for i in range(products):
            if (i + 1) % max(1, products // 5) == 0:
                typer.echo(f"   ... {i + 1}/{products} products created")

            # Create product with unique slug
            base_slug = slugify(random.choice(PRODUCT_NAMES))[:45]  # Leave room for counter
            unique_slug = f"{base_slug}-{i}"[:50]
            product = ProductFactory.create(slug=unique_slug)

            # Create product images (1-3 per product)
            num_images = random.randint(1, 3)
            for img_num in range(num_images):
                try:
                    ProductImageFactory.create(product=product, sort_order=img_num)
                    created_images += 1
                except Exception:
                    pass

            # Create attribute values for this product
            for attr in random.sample(attributes, min(2, len(attributes))):
                try:
                    ProductAttributeValueFactory.create(product=product, attribute=attr)
                    created_attribute_values += 1
                except Exception:
                    pass

            # Create product reviews (2-5 per product)
            num_reviews = random.randint(2, 5)
            for _ in range(num_reviews):
                try:
                    review_author = random.choice(author_list)
                    ProductReviewFactory.create(product=product, author=review_author)
                    created_reviews += 1
                except Exception:
                    pass

        typer.echo(f"✓ Created {Product.objects.count()} products total")
        typer.echo(f"✓ Created {created_images} product images")
        typer.echo(f"✓ Created {created_attribute_values} product attribute values")
        typer.echo(f"✓ Created {created_reviews} product reviews")

        # Create Orders with items
        typer.echo(f"\n📦 Creating {orders} orders with items...")
        created_order_items = 0

        for i in range(orders):
            order_customer = random.choice(author_list)
            order = OrderFactory.create(customer=order_customer)

            # Create order items (2-8 per order)
            num_items = random.randint(2, 8)
            for _ in range(num_items):
                try:
                    OrderItemFactory.create(order=order)
                    created_order_items += 1
                except Exception:
                    pass

        typer.echo(f"✓ Created {Order.objects.count()} orders total")
        typer.echo(f"✓ Created {created_order_items} order items")

        # Create Coupons
        typer.echo(f"\n🎟️  Creating {coupons} coupons...")
        coupon_list = CouponFactory.create_batch(coupons)
        typer.echo(f"✓ Created {len(coupon_list)} coupons")

        # ====================================================================
        # CROSS-DOMAIN & ENGAGEMENT
        # ====================================================================

        # Create Wishlists for authors
        typer.echo(f"\n❤️  Creating author wishlists...")
        created_wishlists = 0
        for author in Author.objects.all():
            try:
                wishlist = WishlistFactory.create(user=author)
                created_wishlists += 1
            except Exception:
                pass
        typer.echo(f"✓ Created {created_wishlists} wishlists")

        # Create Social Links for authors
        typer.echo(f"\n📱 Creating author social links...")
        social_links = 0
        for author in Author.objects.all():
            num_links = random.randint(1, 3)
            for _ in range(num_links):
                try:
                    SocialLinkFactory.create(author=author)
                    social_links += 1
                except Exception:
                    pass
        typer.echo(f"✓ Created {social_links} social links")

        # Create Subscriptions
        typer.echo(f"\n📧 Creating category subscriptions...")
        subscriptions = 0
        for author in Author.objects.all():
            for category in random.sample(list(Category.objects.all()), min(2, Category.objects.count())):
                try:
                    SubscriptionFactory.create(user=author, category=category)
                    subscriptions += 1
                except Exception:
                    pass
        typer.echo(f"✓ Created {subscriptions} subscriptions")

        # Create Notifications
        typer.echo(f"\n🔔 Creating notifications...")
        notifications = 0
        for author in Author.objects.all():
            num_notifs = random.randint(3, 8)
            for _ in range(num_notifs):
                try:
                    NotificationFactory.create(user=author)
                    notifications += 1
                except Exception:
                    pass
        typer.echo(f"✓ Created {notifications} notifications")

        # Create generic Ratings (for both posts and products)
        typer.echo(f"\n⭐ Creating generic ratings...")
        ratings = 0

        # Rate posts
        for post in Post.objects.order_by("?")[: max(1, Post.objects.count() // 3)]:
            num_ratings = random.randint(2, 5)
            for author in random.sample(list(Author.objects.all()), min(num_ratings, Author.objects.count())):
                try:
                    post_ct = ContentType.objects.get_for_model(Post)
                    Rating.objects.get_or_create(
                        content_type=post_ct,
                        object_id=post.id,
                        user=author,
                        defaults={"rating": random.randint(1, 5)}
                    )
                    ratings += 1
                except Exception:
                    pass

        # Rate products
        for product in Product.objects.order_by("?")[: max(1, Product.objects.count() // 3)]:
            num_ratings = random.randint(2, 5)
            for author in random.sample(list(Author.objects.all()), min(num_ratings, Author.objects.count())):
                try:
                    product_ct = ContentType.objects.get_for_model(Product)
                    Rating.objects.get_or_create(
                        content_type=product_ct,
                        object_id=product.id,
                        user=author,
                        defaults={"rating": random.randint(1, 5)}
                    )
                    ratings += 1
                except Exception:
                    pass

        typer.echo(f"✓ Created {ratings} generic ratings")

        # ====================================================================
        # SUMMARY STATISTICS
        # ====================================================================

        typer.echo("\n" + "=" * 60)
        typer.echo("📊 SEEDING SUMMARY")
        typer.echo("=" * 60)

        typer.echo("\n📚 BLOG DOMAIN:")
        typer.echo(f"   Authors: {Author.objects.count()}")
        typer.echo(f"   Categories: {Category.objects.count()}")
        typer.echo(f"   Tags: {Tag.objects.count()}")
        typer.echo(f"   Posts: {Post.objects.count()}")
        typer.echo(f"   - with analytics: {PostAnalytics.objects.count()}")
        typer.echo(f"   - with versions: {PostVersion.objects.count()}")
        typer.echo(f"   Comments: {Comment.objects.count()}")

        typer.echo("\n🛒 E-COMMERCE DOMAIN:")
        typer.echo(f"   Products: {Product.objects.count()}")
        typer.echo(f"   - with images: {ProductImage.objects.count()}")
        typer.echo(f"   Product Attributes: {ProductAttribute.objects.count()}")
        typer.echo(f"   - attribute values: {ProductAttributeValue.objects.count()}")
        typer.echo(f"   Reviews: {ProductReview.objects.count()}")
        typer.echo(f"   Orders: {Order.objects.count()}")
        typer.echo(f"   - order items: {OrderItem.objects.count()}")
        typer.echo(f"   Coupons: {Coupon.objects.count()}")

        typer.echo("\n🤝 ENGAGEMENT & CROSS-DOMAIN:")
        typer.echo(f"   Wishlists: {Wishlist.objects.count()}")
        typer.echo(f"   Social Links: {SocialLink.objects.count()}")
        typer.echo(f"   Subscriptions: {Subscription.objects.count()}")
        typer.echo(f"   Notifications: {Notification.objects.count()}")
        typer.echo(f"   Ratings (generic): {Rating.objects.count()}")

        typer.echo("\n" + "=" * 60)
        typer.echo("✨ Data seeding complete!")
        typer.echo("=" * 60)

    @command()
    def clean(
        self,
        confirm: Annotated[
            bool,
            typer.Option("--confirm", help="Confirm deletion without prompt"),
        ] = False,
    ):
        """Delete all test data."""
        if not confirm:
            if not typer.confirm(
                "⚠️  This will delete ALL admin_test data. Continue?", default=False
            ):
                typer.echo("Cancelled.")
                raise typer.Exit()

        typer.echo("🗑️  Deleting all data...")
        models = [
            ContentFile,
            Notification,
            Subscription,
            SocialLink,
            Rating,
            Wishlist,
            Coupon,
            OrderItem,
            Order,
            ProductReview,
            ProductAttributeValue,
            ProductAttribute,
            ProductImage,
            Product,
            PostVersion,
            PostAnalytics,
            Comment,
            Post,
            Author,
            Category,
            Tag,
        ]
        for model in models:
            count = model.objects.count()
            if count > 0:
                model.objects.all().delete()
                typer.echo(f"   ✓ Deleted {count} {model.__name__} records")
        typer.echo("✓ All data deleted.")
