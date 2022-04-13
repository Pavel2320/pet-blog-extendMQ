from django.test import TestCase

from ..widgets import FeedWidget


class FeedWidgetTest(TestCase):
    def test_feed_widget_option_template_name(self):
        widget = FeedWidget()
        self.assertEqual(widget.option_template_name, 'blog/widgets/feed_option.html')
