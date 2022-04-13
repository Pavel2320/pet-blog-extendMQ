from django.test import TestCase
from django.db import models
from django.core import mail
from django.contrib.auth import get_user_model

from ..models import Blog, Post, Subscription, Feed


class BlogModelTest(TestCase):
    fixtures = ['initial_data.json']

    def test_author_label(self):
        blog = Blog.objects.get(id=1)
        field_label = blog._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'author')

    def test_author_field_related_model(self):
        blog = Blog.objects.get(id=1)
        related_model = blog._meta.get_field('author').related_model
        self.assertEqual(related_model, get_user_model())

    def test_author_field_on_detele(self):
        blog = Blog.objects.get(id=1)
        on_detele = blog._meta.get_field(
            'author').remote_field.on_delete
        self.assertEqual(on_detele, models.CASCADE)

    def test_object_name_is_author_username(self):
        blog = Blog.objects.get(id=1)
        expected_object_name = blog.author.get_username()
        self.assertEqual(str(blog), expected_object_name)


class PostModelTest(TestCase):
    fixtures = ['initial_data.json']

    def test_title_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_name_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 255)

    def test_blog_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('blog').verbose_name
        self.assertEqual(field_label, 'blog')

    def test_blog_field_related_model(self):
        post = Post.objects.get(id=1)
        related_model = post._meta.get_field('blog').related_model
        self.assertEqual(related_model, Blog)

    def test_blog_field_on_detele(self):
        post = Post.objects.get(id=1)
        on_detele = post._meta.get_field(
            'blog').remote_field.on_delete
        self.assertEqual(on_detele, models.CASCADE)

    def test_date_posted_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('posted').verbose_name
        self.assertEqual(field_label, 'posted')

    def test_date_added_auto_now_add(self):
        post = Post.objects.get(id=1)
        auto_now_add = post._meta.get_field('posted').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_content_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

    def test_content_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('content').max_length
        self.assertEqual(max_length, 10000)

    def test_ordering(self):
        post = Post.objects.get(id=1)
        ordering = post._meta.ordering
        self.assertEqual(ordering, ['-posted'])

    def test_save_method(self):
        blog = Blog.objects.get(id=2)
        subscriber = get_user_model().objects.get(pk=1)
        subscription = Subscription.objects.get(pk=1)
        post = Post.objects.create(title='Test title', blog=blog)
        feed = Feed.objects.get(pk=7)

        self.assertEqual(feed.user, subscriber)
        self.assertEqual(feed.subscription, subscription)
        self.assertEqual(feed.post.id, post.id)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'New post')

    def test_object_name_is_title(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.title
        self.assertEqual(str(post), expected_object_name)


class SubscriptionModelTest(TestCase):
    fixtures = ['initial_data.json']

    def test_user_label(self):
        subscription = Subscription.objects.get(id=1)
        field_label = subscription._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_user_field_related_model(self):
        subscription = Subscription.objects.get(id=1)
        related_model = subscription._meta.get_field('user').related_model
        self.assertEqual(related_model, get_user_model())

    def test_user_field_on_detele(self):
        subscription = Subscription.objects.get(id=1)
        on_detele = subscription._meta.get_field(
            'user').remote_field.on_delete
        self.assertEqual(on_detele, models.CASCADE)

    def test_blog_label(self):
        subscription = Subscription.objects.get(id=1)
        field_label = subscription._meta.get_field('blog').verbose_name
        self.assertEqual(field_label, 'blog')

    def test_blog_field_related_model(self):
        subscription = Subscription.objects.get(id=1)
        related_model = subscription._meta.get_field('blog').related_model
        self.assertEqual(related_model, Blog)

    def test_blog_field_on_detele(self):
        subscription = Subscription.objects.get(id=1)
        on_detele = subscription._meta.get_field(
            'blog').remote_field.on_delete
        self.assertEqual(on_detele, models.CASCADE)

    def test_unique_together(self):
        subscription = Subscription.objects.get(id=1)
        unique_together = subscription._meta.unique_together
        self.assertEqual(unique_together, (('user', 'blog'),))

    def test_object_name_is_blog_author_username(self):
        subscription = Subscription.objects.get(id=1)
        expected_object_name = subscription.blog.author.username
        self.assertEqual(str(subscription), expected_object_name)


class FeedModelTest(TestCase):
    fixtures = ['initial_data.json']

    def test_user_label(self):
        feed = Feed.objects.get(id=1)
        field_label = feed._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')

    def test_user_field_related_model(self):
        feed = Feed.objects.get(id=1)
        related_model = feed._meta.get_field('user').related_model
        self.assertEqual(related_model, get_user_model())

    def test_user_field_on_detele(self):
        feed = Feed.objects.get(id=1)
        on_detele = feed._meta.get_field(
            'user').remote_field.on_delete
        self.assertEqual(on_detele, models.CASCADE)

    def test_post_label(self):
        feed = Feed.objects.get(id=1)
        field_label = feed._meta.get_field('post').verbose_name
        self.assertEqual(field_label, 'post')

    def test_post_field_related_model(self):
        feed = Feed.objects.get(id=1)
        related_model = feed._meta.get_field('post').related_model
        self.assertEqual(related_model, Post)

    def test_post_field_on_detele(self):
        feed = Feed.objects.get(id=1)
        on_detele = feed._meta.get_field(
            'post').remote_field.on_delete
        self.assertEqual(on_detele, models.CASCADE)

    def test_subscription_label(self):
        feed = Feed.objects.get(id=1)
        field_label = feed._meta.get_field('subscription').verbose_name
        self.assertEqual(field_label, 'subscription')

    def test_subscription_field_related_model(self):
        feed = Feed.objects.get(id=1)
        related_model = feed._meta.get_field('subscription').related_model
        self.assertEqual(related_model, Subscription)

    def test_subscription_field_on_detele(self):
        feed = Feed.objects.get(id=1)
        on_detele = feed._meta.get_field(
            'subscription').remote_field.on_delete
        self.assertEqual(on_detele, models.CASCADE)

    def test_is_read_label(self):
        feed = Feed.objects.get(id=1)
        field_label = feed._meta.get_field('is_read').verbose_name
        self.assertEqual(field_label, 'is read')

    def test_is_read_default(self):
        feed = Feed.objects.get(id=1)
        default = feed._meta.get_field('is_read').default
        self.assertEqual(default, False)

    def test_ordering(self):
        feed = Feed.objects.get(id=1)
        ordering = feed._meta.ordering
        self.assertEqual(ordering, ['-post__posted'])

    def test_unique_together(self):
        feed = Feed.objects.get(id=1)
        unique_together = feed._meta.unique_together
        self.assertEqual(unique_together, (('user', 'post', 'subscription'),))

    def test_object_name_is_post_title(self):
        feed = Feed.objects.get(id=1)
        expected_object_name = feed.post.title
        self.assertEqual(str(feed), expected_object_name)
