from .models import Notification

from post.models import Post
from account.models import FollowerRequest

def create_notification(request, type_of_notification, post_id=None, followerrequest_id=None):
  created_for = None
  
  if type_of_notification == 'post_like':
    body = f'{request.user.name} liked one of your posts!'
    post = Post.objects.get(pk=post_id)
    created_for = post.created_by
  elif type_of_notification == 'post_comment':
    body = f'{request.user.name} commented one of your posts!'
    post = Post.objects.get(pk=post_id)
    created_for = post.created_by
  elif type_of_notification == 'new_followerrequest':
    followerrequest = FollowerRequest.objects.get(pk=followerrequest_id)
    created_for = followerrequest.created_for
    body = f'{request.user.name} send you a follower request!'
  elif type_of_notification == 'accepted_followerrequest':
    followerrequest = FollowerRequest.objects.get(pk=followerrequest_id)
    created_for = followerrequest.created_for
    body = f'{request.user.name} accepted your follower request!'
  elif type_of_notification == 'rejected_followerrequest':
    followerrequest = FollowerRequest.objects.get(pk=followerrequest_id)
    created_for = followerrequest.created_for
    body = f'{request.user.name} rejected your follower request!'
    
  notification = Notification.objects.create(
    body = body,
    type_of_notification = type_of_notification,
    created_by = request.user,
    post_id=post_id,
    created_for = created_for
  )
  
  return notification
  
  
  """
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  body = models.TextField()
  is_read = models.BooleanField(default=False)
  type_of_notification = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_NOTIFICATION)
  post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
  created_by = models.ForeignKey(User, related_name='created_notification', on_delete=models.CASCADE)
  created_for = models.ForeignKey(User, related_name='received_notification', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  """