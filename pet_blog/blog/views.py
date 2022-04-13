from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from django.db import transaction

from .forms import PostForm, SubscriptionForm, UnSubscriptionForm, FeedForm
from .models import Blog, Post, Feed, Subscription


class PostListView(ListView):
    model = Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'


@method_decorator(login_required(login_url=reverse_lazy('admin:index')), name='dispatch')
class MyPostsView(CreateView):
    model = Post
    template_name = 'blog/my_posts.html'
    form_class = PostForm
    success_url = reverse_lazy('blog:my-posts')

    def get_context_data(self, **kwargs):
        user = self.request.user
        kwargs['posts'] = Post.objects.filter(blog__author=user)
        return super(MyPostsView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.blog = Blog.objects.get(author=self.request.user)
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('admin:index')), name='dispatch')
class FeedView(FormView):
    template_name = 'blog/feed.html'
    form_class = FeedForm
    success_url = reverse_lazy('blog:feed')

    def get_form(self):
        form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        feeds = form.cleaned_data['feeds']
        for feed in feeds:
            feed.is_read = True
        Feed.objects.bulk_update(feeds, ['is_read'])
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('admin:index')), name='dispatch')
class BlogsView(FormView):
    template_name = 'blog/blogs.html'
    form_class = SubscriptionForm
    success_url = reverse_lazy('blog:blogs')

    def get_form(self):
        form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())

    @transaction.atomic
    def form_valid(self, form):
        user = self.request.user
        blogs = form.cleaned_data['blogs']

        for blog in blogs:
            subscription = Subscription(user=user, blog=blog)
            subscription.save()

            posts = Post.objects.filter(blog=blog)
            Feed.objects.bulk_create(
                [Feed(user=user, post=post, subscription=subscription) for post in posts])
        return super().form_valid(form)


@method_decorator(login_required(login_url=reverse_lazy('admin:index')), name='dispatch')
class SubscriptionsView(FormView):
    template_name = 'blog/subscriptions.html'
    form_class = UnSubscriptionForm
    success_url = reverse_lazy('blog:subscriptions')

    def get_form(self):
        form_class = self.get_form_class()
        return form_class(self.request.user, **self.get_form_kwargs())

    def form_valid(self, form):
        subscriptions = form.cleaned_data['subscriptions']
        subscriptions.delete()
        return super().form_valid(form)
