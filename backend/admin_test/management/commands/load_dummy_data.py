from typing import Annotated

import typer
from django_typer.management import TyperCommand, command

from admin_test.factories import (
    AuthorFactory,
    BooleanTestModelFactory,
    CategoryFactory,
    ChoiceTestModelFactory,
    CommentFactory,
    DateTimeComprehensiveModelFactory,
    EventLogFactory,
    EventScheduleFactory,
    IdentifierModelFactory,
    NumberTestModelFactory,
    PollFactory,
    PostFactory,
    RelationshipTestModelFactory,
    TagFactory,
    TextFieldsModelFactory,
    URLEmailFileModelFactory,
)
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


class Command(TyperCommand):
    """
    Load dummy data for admin test app
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
        events: Annotated[
            int,
            typer.Option(
                "--events",
                help="The number of events to create",
            ),
        ] = 15,
        polls: Annotated[
            int,
            typer.Option(
                "--polls",
                help="The number of polls to create",
            ),
        ] = 10,
        event_logs: Annotated[
            int,
            typer.Option(
                "--event-logs",
                help="The number of event logs to create",
            ),
        ] = 50,
        clear: Annotated[
            bool,
            typer.Option(
                "--clear",
                help="Clear existing data before seeding",
            ),
        ] = False,
    ):
        """
        Seed database with dummy data for all models.
        Creates authors, categories, tags, posts, comments, events, polls, and event logs.
        """
        # Clear existing data if requested
        if clear:
            typer.echo("🗑️  Clearing existing data...")
            # New models
            NumberTestModel.objects.all().delete()
            BooleanTestModel.objects.all().delete()
            URLEmailFileModel.objects.all().delete()
            ChoiceTestModel.objects.all().delete()
            DateTimeComprehensiveModel.objects.all().delete()
            IdentifierModel.objects.all().delete()
            TextFieldsModel.objects.all().delete()
            RelationshipTestModel.objects.all().delete()
            # Existing models
            Post.objects.all().delete()
            Comment.objects.all().delete()
            Author.objects.all().delete()
            Category.objects.all().delete()
            Tag.objects.all().delete()
            EventSchedule.objects.all().delete()
            Poll.objects.all().delete()
            EventLog.objects.all().delete()
            typer.echo("✓ Data cleared")
            typer.echo("")
        # New models seeding
        typer.echo("🔢 Creating NumberTestModel records...")
        number_test_objs = NumberTestModelFactory.create_batch(10)
        typer.echo(f"✓ Created {len(number_test_objs)} NumberTestModel records")

        typer.echo("✅ Creating BooleanTestModel records...")
        boolean_test_objs = BooleanTestModelFactory.create_batch(10)
        typer.echo(f"✓ Created {len(boolean_test_objs)} BooleanTestModel records")

        typer.echo("🌐 Creating URLEmailFileModel records...")
        url_email_file_objs = URLEmailFileModelFactory.create_batch(5)
        typer.echo(f"✓ Created {len(url_email_file_objs)} URLEmailFileModel records")

        typer.echo("🎚️  Creating ChoiceTestModel records...")
        choice_test_objs = ChoiceTestModelFactory.create_batch(8)
        typer.echo(f"✓ Created {len(choice_test_objs)} ChoiceTestModel records")

        typer.echo("⏰ Creating DateTimeComprehensiveModel records...")
        datetime_comprehensive_objs = DateTimeComprehensiveModelFactory.create_batch(6)
        typer.echo(
            f"✓ Created {len(datetime_comprehensive_objs)} DateTimeComprehensiveModel records"
        )

        typer.echo("🆔 Creating IdentifierModel records...")
        identifier_objs = IdentifierModelFactory.create_batch(7)
        typer.echo(f"✓ Created {len(identifier_objs)} IdentifierModel records")

        typer.echo("📝 Creating TextFieldsModel records...")
        textfields_objs = TextFieldsModelFactory.create_batch(10)
        typer.echo(f"✓ Created {len(textfields_objs)} TextFieldsModel records")

        typer.echo("🔗 Creating RelationshipTestModel records...")
        # For relationships, assign random authors, categories, tags
        import random

        for _ in range(8):
            obj = RelationshipTestModelFactory()
            # Assign random author, categories, tags if available
            if Author.objects.exists():
                obj.author = random.choice(list(Author.objects.all()))
                obj.save()
            if Category.objects.exists():
                obj.categories.set(
                    random.sample(
                        list(Category.objects.all()), min(2, Category.objects.count())
                    )
                )
            if Tag.objects.exists():
                obj.tags.set(
                    random.sample(list(Tag.objects.all()), min(2, Tag.objects.count()))
                )
        typer.echo(f"✓ Created 8 RelationshipTestModel records")

        # Validate inputs
        if posts < 1 or posts > 1000:
            typer.echo("❌ Posts count must be between 1 and 1000")
            raise typer.Exit(1)

        if comments_per_post < 1 or comments_per_post > 20:
            typer.echo("❌ Comments per post must be between 1 and 20")
            raise typer.Exit(1)

        typer.echo("🌱 Starting data seeding...")
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

        # Create Event Schedules
        typer.echo(f"📅 Creating {events} event schedules...")
        event_list = EventScheduleFactory.create_batch(events)
        typer.echo(f"✓ Created {len(event_list)} events")

        # Create Polls
        typer.echo(f"🗳️  Creating {polls} polls...")
        poll_list = PollFactory.create_batch(polls)
        typer.echo(f"✓ Created {len(poll_list)} polls")

        # Create Event Logs
        typer.echo(f"📋 Creating {event_logs} event logs...")
        log_list = EventLogFactory.create_batch(event_logs)
        typer.echo(f"✓ Created {len(log_list)} event logs")

        # Print summary statistics
        typer.echo("")
        typer.echo("📊 Summary:")
        typer.echo(f"   Authors: {Author.objects.count()}")
        typer.echo(f"   Categories: {Category.objects.count()}")
        typer.echo(f"   Tags: {Tag.objects.count()}")
        typer.echo(f"   Posts: {Post.objects.count()}")
        typer.echo(f"   Comments: {Comment.objects.count()}")
        typer.echo(f"   Event Schedules: {EventSchedule.objects.count()}")
        typer.echo(f"   Polls: {Poll.objects.count()}")
        typer.echo(f"   Event Logs: {EventLog.objects.count()}")
        typer.echo(f"   NumberTestModels: {NumberTestModel.objects.count()}")
        typer.echo(f"   BooleanTestModels: {BooleanTestModel.objects.count()}")
        typer.echo(f"   URLEmailFileModels: {URLEmailFileModel.objects.count()}")
        typer.echo(f"   ChoiceTestModels: {ChoiceTestModel.objects.count()}")
        typer.echo(
            f"   DateTimeComprehensiveModels: {DateTimeComprehensiveModel.objects.count()}"
        )
        typer.echo(f"   IdentifierModels: {IdentifierModel.objects.count()}")
        typer.echo(f"   TextFieldsModels: {TextFieldsModel.objects.count()}")
        typer.echo(
            f"   RelationshipTestModels: {RelationshipTestModel.objects.count()}"
        )

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
        typer.echo("✨ Data seeding complete!")

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
        Delete all data (posts, comments, authors, categories, tags, events, polls, logs).
        """
        if not confirm:
            if not typer.confirm(
                "⚠️  This will delete all data. Continue?", default=False
            ):
                typer.echo("Cancelled.")
                raise typer.Exit()

        typer.echo("🗑️  Deleting all data...")
        NumberTestModel.objects.all().delete()
        BooleanTestModel.objects.all().delete()
        URLEmailFileModel.objects.all().delete()
        ChoiceTestModel.objects.all().delete()
        DateTimeComprehensiveModel.objects.all().delete()
        IdentifierModel.objects.all().delete()
        TextFieldsModel.objects.all().delete()
        RelationshipTestModel.objects.all().delete()
        Post.objects.all().delete()
        Comment.objects.all().delete()
        Author.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()
        EventSchedule.objects.all().delete()
        Poll.objects.all().delete()
        EventLog.objects.all().delete()
        typer.echo("✓ All data deleted.")
