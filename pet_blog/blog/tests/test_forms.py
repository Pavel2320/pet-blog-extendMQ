from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model

from ..forms import PostForm, SubscriptionForm, UnSubscriptionForm, FeedForm
from ..models import Post
from ..widgets import FeedWidget


class PostFormTest(TestCase):
    def test_post_form_model(self):
        form = PostForm()
        model = form._meta.model
        self.assertEqual(model, Post)

    def test_post_form_title_field_label(self):
        form = PostForm()
        self.assertEqual(form.fields['title'].label, '')

    def test_post_form_content_field_label(self):
        form = PostForm()
        self.assertEqual(form.fields['content'].label, '')

    def test_post_form_fields(self):
        form = PostForm()
        fields = form._meta.fields
        self.assertEqual(fields, ('title', 'content'))

    def test_post_form_title_widget(self):
        form = PostForm()
        title_widget = form._meta.widgets['title']
        self.assertIsInstance(title_widget, forms.TextInput)
        self.assertEqual(title_widget.attrs, {'class': 'form-control', 'placeholder': 'Title...'})

    def test_post_form_content_widget(self):
        form = PostForm()
        content_widget = form._meta.widgets['content']
        self.assertIsInstance(content_widget, forms.Textarea)
        self.assertEqual(content_widget.attrs['class'], 'form-control')
        self.assertEqual(content_widget.attrs['placeholder'], 'Text...')


class SubscriptionFormTest(TestCase):
    fixtures = ['initial_data.json']

    def test_subscription_form_authors_field_is_model_multiple_choice_field(self):
        user = get_user_model().objects.get(pk=1)
        form = SubscriptionForm(user)
        self.assertIsInstance(form.fields['blogs'], forms.ModelMultipleChoiceField)

    def test_subscription_form_authors_field_widget(self):
        user = get_user_model().objects.get(pk=1)
        form = SubscriptionForm(user)
        widget = form.fields['blogs'].widget
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)
        self.assertEqual(widget.attrs, {'class': 'form-check-input'})

    def test_subscription_form_blogs_field_queryset(self):
        user = get_user_model().objects.get(pk=1)
        form = SubscriptionForm(user)
        self.assertEqual(len(form.fields['blogs'].queryset), 1)
        self.assertEqual(form.fields['blogs'].queryset[0].author.username, 'User4')


class UnSubscriptionFormTest(TestCase):
    fixtures = ['initial_data.json']

    def test_unsubscription_form_subscriptions_field_is_model_multiple_choice_field(self):
        user = get_user_model().objects.get(pk=1)
        form = UnSubscriptionForm(user)
        self.assertIsInstance(form.fields['subscriptions'], forms.ModelMultipleChoiceField)

    def test_unsubscription_form_subscriptions_field_widget(self):
        user = get_user_model().objects.get(pk=1)
        form = UnSubscriptionForm(user)
        widget = form.fields['subscriptions'].widget
        self.assertIsInstance(widget, forms.CheckboxSelectMultiple)
        self.assertEqual(widget.attrs, {'class': 'form-check-input'})

    def test_unsubscription_form_subscriptions_field_queryset(self):
        user = get_user_model().objects.get(pk=1)
        form = UnSubscriptionForm(user)
        self.assertEqual(len(form.fields['subscriptions'].queryset), 2)
        self.assertEqual(form.fields['subscriptions'].queryset[0].blog.author.username, 'User2')


class FeedFormTest(TestCase):
    fixtures = ['initial_data.json']

    def test_feed_form_feeds_field_is_model_multiple_choice_field(self):
        user = get_user_model().objects.get(pk=1)
        form = FeedForm(user)
        self.assertIsInstance(form.fields['feeds'], forms.ModelMultipleChoiceField)

    def test_feed_form_feeds_field_widget(self):
        user = get_user_model().objects.get(pk=1)
        form = FeedForm(user)
        widget = form.fields['feeds'].widget
        self.assertIsInstance(widget, FeedWidget)
        self.assertEqual(widget.attrs, {'class': 'form-check-input'})

    def test_feed_form_feeds_field_queryset(self):
        user = get_user_model().objects.get(pk=1)
        form = FeedForm(user)
        self.assertEqual(len(form.fields['feeds'].queryset), 5)
        self.assertEqual(form.fields['feeds'].queryset.first().post.title, 'Test post 9')
