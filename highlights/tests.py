from django.test import TestCase
from django.contrib.auth import get_user_model

from . import models
from .utils import slugify

User = get_user_model()


def create_user(**overwrites):
    return User.objects.create(
        username="testuser",
        password="abc123",
        **overwrites,
    )


class AuthorTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.author = models.Author.objects.create(
            user=self.user,
            name="Test Author",
        )

    def test_slug_is_created(self):
        self.assertEqual(self.author.slug, "test-author")

    def test_slug_is_unique(self):
        new_author = models.Author.objects.create(user=self.user, name="Test Author***")

        self.assertNotEqual(self.author.slug, new_author.slug)
        self.assertEqual(len(new_author.slug), 16)
        self.assertTrue(new_author.slug.startswith("test-author-"))


class BookTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        author = models.Author.objects.create(
            user=self.user,
            name="Test Author",
        )
        self.book = models.Book.objects.create(
            user=self.user,
            title="Test Book",
            author=author,
            book_no=1,
        )

    def test_slug_is_created(self):
        self.assertEqual(self.book.slug, "test-book")

    def test_slug_is_unique(self):
        new_book = models.Book.objects.create(
            user=self.user,
            title="Test Book***",
            book_no=1,
            author=self.book.author,
        )

        self.assertNotEqual(self.book.slug, new_book.slug)
        self.assertEqual(len(new_book.slug), 14)
        self.assertTrue(new_book.slug.startswith("test-book-"))


class TagTestCase(TestCase):
    def setUp(self):
        self.user = create_user()
        self.tag = models.Tag.objects.create(
            user=self.user,
            tag="Test Tag",
        )

    def test_slug_is_created(self):
        self.assertEqual(self.tag.slug, "test-tag")

    def test_slug_is_unique(self):
        new_tag = models.Tag.objects.create(
            user=self.user,
            tag="Test Tag***",
        )

        self.assertNotEqual(self.tag.slug, new_tag.slug)
        self.assertEqual(len(new_tag.slug), 13)
        self.assertTrue(new_tag.slug.startswith("test-tag-"))

    def test_slugify_instance(self):
        duplicate = models.Tag(
            user=self.user,
            tag="Test Tag**",
        )
        new_slugs = []
        for i in range(0, 5):
            instance = slugify.slugify_instance(duplicate, "tag")
            new_slugs.append(instance.slug)

        print("NEW SLUGS", new_slugs)
        unique_slugs = list(set(new_slugs))
        self.assertEqual(len(new_slugs), len(unique_slugs))
