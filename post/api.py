from django.db.models import Q
from django.http import JsonResponse
from collections import Counter
from datetime import timedelta
from django.utils import timezone


from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)

from account.models import User, FollowerRequest
from .models import Post, Like, Comment, Trend

from account.serializers import UserSerializer
from .serializers import (
    PostSerializer,
    PostDetailSerializer,
    CommentSerializer,
    TrendSerializer,
)

from .forms import PostForm, AttachmentForm

from notification.utils import create_notification
from utils.text_helpers import extract_hashtags


# Create your views here.
@api_view(["GET"])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.followers.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get("trend", "")

    if trend:
        posts = posts.filter(body__icontains="#" + trend).filter(is_private=False)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    # if ur a follower see all posts
    # if ur not a follower, only see public posts
    if not request.user in user.followers.all():
        print("Enter here!?!?")
        posts = posts.filter(is_private=False)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    can_send_follower_request = True

    if request.user in user.followers.all():
        can_send_follower_request = False

    followerReqMade = FollowerRequest.objects.filter(created_for=request.user).filter(
        created_by=user
    )
    alreadyAFollower = FollowerRequest.objects.filter(created_for=user).filter(
        created_by=request.user
    )

    if followerReqMade or alreadyAFollower:
        can_send_follower_request = False

    return JsonResponse(
        {
            "posts": posts_serializer.data,
            "user": user_serializer.data,
            "can_send_follower_request": can_send_follower_request,
        },
        safe=False,
    )


@api_view(["POST"])
def post_create(request):
    form = PostForm(request.POST)
    attachment = None
    print(request.POST)
    print(request.FILES)
    attachment_form = AttachmentForm(request.POST, request.FILES)

    if attachment_form.is_valid():
        attachment = attachment_form.save(commit=False)
        attachment.created_by = request.user
        attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        if attachment:
            post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)

    else:
        return JsonResponse({"error": "Error here!"})


@api_view(["POST"])
def post_like(request, pk):
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        notification = create_notification(request, "post_like", post_id=post.id)

        return JsonResponse({"message": "like created"})
    else:
        return JsonResponse({"message": "Post already liked!"})


@api_view(["GET"])
def post_detail(request, pk):
    user_ids = [request.user.id]

    for user in request.user.followers.all():
        user_ids.append(user.id)

    post = Post.objects.filter(
        Q(created_by_id__in=list(user_ids)) | Q(is_private=False)
    ).get(pk=pk)

    return JsonResponse({"post": PostDetailSerializer(post).data})


@api_view(["POST"])
def post_create_comment(request, pk):
    comment = Comment.objects.create(
        body=request.data.get("body"), created_by=request.user
    )

    post = Post.objects.get(pk=pk)
    post.comments.add(comment)
    post.comments_count += 1
    post.save()

    notification = create_notification(request, "post_comment", post_id=post.id)

    serializer = CommentSerializer(comment)

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def get_trends(request):
    serializer = TrendSerializer(Trend.objects.all(), many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
@authentication_classes([])
@permission_classes([])
def generate_trends(request):
    for trend in Trend.objects.all():
        trend.delete()

    this_hour = timezone.now().replace(minute=0, second=0, microsecond=0)
    twenty_four_hours = this_hour - timedelta(hours=24)

    for post in Post.objects.filter(created_at__gte=twenty_four_hours).filter(
        is_private=False
    ):
        trends = extract_hashtags(post.body)

    for trend in Counter(trends).most_common(10):
        Trend.objects.create(hashtag=trend[0], occurrences=trend[1])

    return JsonResponse({"message": "Trends generated!", "status": "success"})


@api_view(["DELETE"])
def delete_post(request, pk):
    post = Post.objects.filter(created_by=request.user).get(pk=pk)
    post.delete()

    return JsonResponse({"message": "Post deleted!", "status": "success"})


@api_view(["POST"])
def report_post(request, pk):
    post = Post.objects.get(pk=pk)
    post.reported_by_users.add(request.user)
    post.save()

    return JsonResponse({"message": "Post reported!", "status": "success"})
