from django.urls import path
from .views import PostListView, MyPostsView, PostDetailView, BlogsView, SubscriptionsView, FeedView

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('my-posts/', MyPostsView.as_view(), name='my-posts'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('subscriptions/', SubscriptionsView.as_view(), name='subscriptions')
]
