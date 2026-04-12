from typing import Annotated

import typer
from django_typer.management import TyperCommand, command

from admin_test.factories import (
    AuthorFactory,
    CategoryFactory,
    CommentFactory,
    PostFactory,
    TagFactory,
)
from admin_test.models import Author, Category, Comment, Post, Tag


class Command(TyperCommand):
    """
    Manage blog models
    """

    @command()
    def seed(
        self,
        posts: Annotated[
            int,
            typer.Option(
                "--posts",
                help="The number of posts to create (1-1000)",
            ),
        ] = 30,
        authors: Annotated[
            int,
            typer.Option(
                "--authors",
                help="The number of authors to create",
            ),
        ] = 8,
        categories: Annotated[
            int,
            typer.Option(
                "--categories",
                help="The number of categories to create",
            ),
        ] = 10,
        tags: Annotated[
            int,
            typer.Option(
                "--tags",
                help="The number of tags to create",
            ),
        ] = 18,
        comments_per_post: Annotated[
            int,
            typer.Option(
                "--comments-per-post",
                help="Average number of comments per post (2-8)",
            ),
        ] = 4,
        clear: Annotated[
            bool,
            typer.Option(
                "--clear",
                help="Clear existing data before seeding",
            ),
        ] = False,
    ):
        """
        Seed blog database with dummy data.
        Creates authors, categories, tags, posts (with categories and tags),
        and comments for each post.
        """
        # Clear existing data if requested
        if clear:
            typer.echo("🗑️  Clearing existing data...")
            Post.objects.all().delete()
            Comment.objects.all().delete()
            Author.objects.all().delete()
            Category.objects.all().delete()
            Tag.objects.all().delete()
            typer.echo("✓ Data cleared")
            typer.echo("")

        # Validate inputs
        if posts < 1 or posts > 1000:
            typer.echo("❌ Posts count must be between 1 and 1000")
            raise typer.Exit(1)

        if comments_per_post < 1 or comments_per_post > 20:
            typer.echo("❌ Comments per post must be between 1 and 20")
            raise typer.Exit(1)

        typer.echo("🌱 Starting blog data seeding...")
        typer.echo("")

        # Create Authors
        typer.echo(f"👤 Creating {authors} authors...")
        author_list = AuthorFactory.create_batch(authors)
        typer.echo(f"✓ Created {len(author_list)} authors")

        # Create Categories
        typer.echo(f"📁 Creating {categories} categories...")
        category_list = CategoryFactory.create_batch(categories)
        typer.echo(f"✓ Created {len(category_list)} categories")

        # Create Tags
        typer.echo(f"🏷️  Creating {tags} tags...")
        tag_list = TagFactory.create_batch(tags)
        typer.echo(f"✓ Created {len(tag_list)} tags")

        # Create Posts with related comments
        typer.echo(f"📝 Creating {posts} posts with comments...")
        created_comments = 0

        for i in range(posts):
            # Show progress every 10 posts
            if (i + 1) % 10 == 0:
                typer.echo(f"   ... {i + 1}/{posts} posts created")

            # Create post
            post = PostFactory.create()

            # Create comments for this post
            num_comments = max(
                1,
                min(
                    comments_per_post + (i % 3 - 1),
                    8,
                ),  # Vary between 1-8
            )
            for _ in range(num_comments):
                CommentFactory.create(post=post)
                created_comments += 1

        total_posts = Post.objects.count()
        typer.echo(f"✓ Created {total_posts} posts total")
        typer.echo(f"✓ Created {created_comments} comments total")

        # Print summary statistics
        typer.echo("")
        typer.echo("📊 Summary:")
        typer.echo(f"   Authors: {Author.objects.count()}")
        typer.echo(f"   Categories: {Category.objects.count()}")
        typer.echo(f"   Tags: {Tag.objects.count()}")
        typer.echo(f"   Posts: {Post.objects.count()}")
        typer.echo(f"   Comments: {Comment.objects.count()}")

        # Calculate relationships
        posts_with_comments = (
            Post.objects.filter(comments__isnull=False).distinct().count()
        )
        posts_with_categories = (
            Post.objects.filter(categories__isnull=False).distinct().count()
        )
        posts_with_tags = Post.objects.filter(tags__isnull=False).distinct().count()

        typer.echo(f"   Posts with comments: {posts_with_comments}")
        typer.echo(f"   Posts with categories: {posts_with_categories}")
        typer.echo(f"   Posts with tags: {posts_with_tags}")

        typer.echo("")
        typer.echo("✨ Blog data seeding complete!")

    @command()
    def clean(
        self,
        confirm: Annotated[
            bool,
            typer.Option(
                "--confirm",
                help="Confirm deletion without prompt",
            ),
        ] = False,
    ):
        """
        Delete all blog data (posts, comments, authors, categories, tags).
        """
        if not confirm:
            if not typer.confirm(
                "⚠️  This will delete all blog data. Continue?", default=False
            ):
                typer.echo("Cancelled.")
                raise typer.Exit()

        typer.echo("🗑️  Deleting all blog data...")
        Post.objects.all().delete()
        Comment.objects.all().delete()
        Author.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        typer.echo("✓ All blog data deleted.")
