from django import forms


class FeedWidget(forms.CheckboxSelectMultiple):
    option_template_name = 'blog/widgets/feed_option.html'
