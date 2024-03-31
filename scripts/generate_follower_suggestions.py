# create a script to generate follower suggestions 
import django
import os
import sys

from collections import Counter
from datetime import timedelta
from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from account.models import User

users = User.objects.all()

for user in users:
  user.people_you_may_know.clear()
  print('Find follower for: ' , user)
  
  for follower in user.followers.all():
    print('Is follower with: ' , follower)
    
    for followersfollower in follower.followers.all():
      if followersfollower not in user.followers.all()  and followersfollower != user:
        user.people_you_may_know.add(followersfollower)
        
        
  print()
        
  
  
  
  
