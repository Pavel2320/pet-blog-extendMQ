from django.test import TestCase
from django.urls import reverse

from ..forms import PostForm, FeedForm, UnSubscriptionForm, SubscriptionForm
from ..models import Post, Feed, Subscription
from ..views import PostListView, PostDetailView, MyPostsView, FeedView, BlogsView, SubscriptionsView


class PostsViewTest(TestCase):
    fixtures = ['initial_data.json']

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('blog:posts'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('blog:posts'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/posts.html')

    def test_view_lists_all_posts(self):
        resp = self.client.get(reverse('blog:posts'))
        self.assertEqual(len(resp.context['posts']), 10)

    def test_post_list_view_model_is_post(self):
        post_list_view = PostListView()
        self.assertEqual(post_list_view.model, Post)


class PostDetailViewTest(TestCase):
    fixtures = ['initial_data.json']

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/post/1/')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('blog:post-detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/post_detail.html')

    def test_post_detail_view_model_is_post(self):
        post_detail_view = PostDetailView()
        self.assertEqual(post_detail_view.model, Post)


class MyPostsViewTest(TestCase):
    fixtures = ['initial_data.json']

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('blog:my-posts'))
        self.assertRedirects(resp, '/admin/?next=/my-posts/', target_status_code=302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.get('/my-posts/')
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.get(reverse('blog:my-posts'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/my_posts.html')

    def test_lists_only_users_posts(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.get(reverse('blog:my-posts'))
        self.assertEqual(len(resp.context['posts']), 3)
        self.assertEqual(resp.context['posts'].first().blog.author.username, 'User1')

    def test_my_posts_view_model_is_post(self):
        my_posts_view = MyPostsView()
        self.assertEqual(my_posts_view.model, Post)

    def test_my_posts_view_form_class_is_post_form(self):
        my_posts_view = MyPostsView()
        self.assertEqual(my_posts_view.form_class, PostForm)

    def test_my_posts_view_success_url(self):
        my_posts_view = MyPostsView()
        self.assertEqual(my_posts_view.success_url, reverse('blog:my-posts'))

    def test_successful_post(self):
        self.client.login(username='User1', password='pass')
        self.client.post(reverse('blog:my-posts'),
                         {'title': 'Test post', 'content': 'Test content'})

        first_post = Post.objects.first()
        self.assertEqual(first_post.blog.author.username, 'User1')
        self.assertEqual(first_post.title, 'Test post')
        self.assertEqual(first_post.content, 'Test content')


class FeedViewTest(TestCase):
    fixtures = ['initial_data.json']

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('blog:feed'))
        self.assertRedirects(resp, '/admin/?next=/feed/', target_status_code=302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.get('/feed/')
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.get(reverse('blog:feed'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/feed.html')

    def test_feed_view_form_class_is_feed_form(self):
        feed_view = FeedView()
        self.assertEqual(feed_view.form_class, FeedForm)

    def test_feed_view_success_url(self):
        feed_view = FeedView()
        self.assertEqual(feed_view.success_url, reverse('blog:feed'))

    def test_successful_mark_post_is_read(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.post(reverse('blog:feed'), {'feeds': [4]})

        feed = Feed.objects.get(pk=4)
        self.assertTrue(feed.is_read)
        self.assertRedirects(resp, reverse('blog:feed'))


class BlogsViewTest(TestCase):
    fixtures = ['initial_data.json']

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('blog:blogs'))
        self.assertRedirects(resp, '/admin/?next=/blogs/', target_status_code=302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.get('/blogs/')
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.get(reverse('blog:blogs'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/blogs.html')

    def test_blogs_view_form_class_is_feed_form(self):
        blogs_view = BlogsView()
        self.assertEqual(blogs_view.form_class, SubscriptionForm)

    def test_blogs_view_success_url(self):
        blogs_view = BlogsView()
        self.assertEqual(blogs_view.success_url, reverse('blog:blogs'))

    def test_successful_subscription(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.post(reverse('blog:blogs'), {'blogs': [4]})

        subscriptions = Subscription.objects.all()
        self.assertEqual(len(subscriptions), 3)
        self.assertEqual(subscriptions.last().blog.author.username, 'User4')

        feed = Feed.objects.all()
        self.assertEqual(len(feed), 7)
        self.assertEqual(feed.first().post.title, 'Test post 10')
        self.assertRedirects(resp, reverse('blog:blogs'))


class SubscriptionsViewTest(TestCase):
    fixtures = ['initial_data.json']

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('blog:subscriptions'))
        self.assertRedirects(resp, '/admin/?next=/subscriptions/', target_status_code=302)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.get('/subscriptions/')
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.get(reverse('blog:subscriptions'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'blog/subscriptions.html')

    def test_subscriptions_view_form_class_is_feed_form(self):
        subscriptions_view = SubscriptionsView()
        self.assertEqual(subscriptions_view.form_class, UnSubscriptionForm)

    def test_subscriptions_view_success_url(self):
        subscriptions_view = SubscriptionsView()
        self.assertEqual(subscriptions_view.success_url, reverse('blog:subscriptions'))

    def test_successful_unsubscription(self):
        self.client.login(username='User1', password='pass')
        resp = self.client.post(reverse('blog:subscriptions'),
                                {'subscriptions': [1]})

        subscriptions = Subscription.objects.all()
        self.assertEqual(len(subscriptions), 1)
        self.assertEqual(subscriptions.first().blog.author.username, 'User3')
        self.assertRedirects(resp, reverse('blog:subscriptions'))
