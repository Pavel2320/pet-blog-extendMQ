import logging
from smtplib import SMTPException

from django.db import models
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)


class Blog(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.get_username()


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    posted = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=10000)

    class Meta:
        ordering = ['-posted']

    def save(self, *args, **kwargs):
        super(Post, self).save(*args, **kwargs)
        subscriptions = Subscription.objects.filter(blog=self.blog)
        for subscription in subscriptions:
            subscriber = subscription.user
            feed = Feed(user=subscriber, post=self, subscription=subscription)
            feed.save()

            try:
                send_mail(
                    'New post',
                    'You have a new post in your feed.',
                    'from@pet-blog.com',
                    [subscriber.email],
                    fail_silently=False,
                )
            except SMTPException as e:
                logger.error(f"Unable to send email to {subscriber}: {e}")

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'blog']

    def __str__(self):
        return self.blog.author.get_username()


class Feed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-post__posted']
        unique_together = ['user', 'post', 'subscription']

    def __str__(self):
        return self.post.title
