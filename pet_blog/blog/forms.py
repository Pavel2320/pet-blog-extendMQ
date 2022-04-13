from django import forms

from .models import Post, Blog
from .widgets import FeedWidget


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        labels = {
            'title': '',
            'content': '',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text...'}),
        }


class SubscriptionForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(SubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['blogs'].queryset = Blog.objects.exclude(author=user).exclude(
            author__in=user.subscription_set.all().values('blog__author'))

    blogs = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        queryset=None
    )


class UnSubscriptionForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(UnSubscriptionForm, self).__init__(*args, **kwargs)
        self.fields['subscriptions'].queryset = user.subscription_set.all()

    subscriptions = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        queryset=None
    )


class FeedForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(FeedForm, self).__init__(*args, **kwargs)
        self.fields['feeds'].queryset = user.feed_set.filter(is_read=False)

    feeds = forms.ModelMultipleChoiceField(
        widget=FeedWidget(attrs={'class': 'form-check-input'}),
        queryset=None
    )
