"""Unit tests for the post model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from microblogs.models import Post

class PostModelTestCase(TestCase):
    """Unit tests for the post model."""

    def create_author(self):
        author = User.objects.create_user(
            '@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='The quick brown fox jumps over the lazy dog.'
        )
        return author

    def setUp(self):
        self.post = Post.objects.create(
            author = self.create_author(),
            text = 'random text for post cluck'
        )

    def test_text_must_not_be_blank(self):
        self.post.text = ''
        self._assert_post_is_valid()

    def test_text_need_not_be_unique(self):
        second_user = self._create_second_post()
        self.post.text = second_user.post
        self._assert_post_is_valid()

    def test_text_may_contain_280_characters(self):
        self.post.text = 'x' * 280
        self._assert_poost_is_valid()

    def test_text_must_not_contain_more_than_280_characters(self):
        self.post.text = 'x' * 281
        self._assert_post_is_invalid()

    def _create_second_post(self):
        post = Post.objects.create_user(
            '@janedoe',
            text = 'today is friday',
            created_at = Default)
        return post
