# create a script to generate follower suggestions
from http.server import BaseHTTPRequestHandler
import os
import sys
from collections import Counter
from datetime import timedelta
from django.utils import timezone

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
import django

django.setup()

from account.models import User


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        users = User.objects.all()
        response = []
        for user in users:
            user.people_you_may_know.clear()
            user_info = f"Find follower for: {user}\n"
            response.append(user_info)
            for follower in user.followers.all():
                follower_info = f"Is follower with: {follower}\n"
                response.append(follower_info)
                for followersfollower in follower.followers.all():
                    if (
                        followersfollower not in user.followers.all()
                        and followersfollower != user
                    ):
                        user.people_you_may_know.add(followersfollower)
                        added_info = f"Added: {followersfollower}\n"
                        response.append(added_info)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("\n".join(response).encode())
