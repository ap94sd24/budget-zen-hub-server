from rest_framework import serializers

from .models import User, FollowerRequest

class UserSerializer(serializers.ModelSerializer):
  class Meta: 
    model = User
    fields = ('id', 'name', 'email', 'followers_count', 'posts_count', 'get_avatar',)
    

class FollowerRequestSerializer(serializers.ModelSerializer):
  created_by = UserSerializer(read_only=True)
  class Meta: 
    model = FollowerRequest
    fields = ('id', 'created_by',)
    