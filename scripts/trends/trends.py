# create a script to generate trends to follow
from http.server import BaseHTTPRequestHandler
import os
import sys
from collections import Counter
from datetime import timedelta
from django.utils import timezone

# Setting up Django environment
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django

django.setup()

from post.models import Post, Trend


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.generate_trends()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("Trends generated successfully.".encode())

    def extract_hashtags(self, text, trends):
        for word in text.split():
            if word.startswith("#"):
                trends.append(word[1:])

    def generate_trends(self):
        Trend.objects.all().delete()
        trends = []

        this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
        twenty_four_hours_ago = this_hour - timedelta(hours=24)
        posts = Post.objects.filter(
            created_at__gte=twenty_four_hours_ago, is_private=False
        )

        for post in posts:
            self.extract_hashtags(post.body, trends)

        for trend, count in Counter(trends).most_common(10):
            Trend.objects.create(hashtag=trend, occurrences=count)
