from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import api
from . import views

urlpatterns = [
    path("me/", api.me, name="me"),
    path(
        "cron/generate_follower_suggestions/",
        api.generate_follower_suggestions,
        name="generate_follower_suggestions",
    ),
    path(
        "cron/generate_all_cron_data/",
        api.generate_all_cron_jobs_data,
        name="generate_all_cron_jobs_data",
    ),
    path("signup/", api.signup, name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        "followers/<uuid:pk>/request/",
        api.send_follower_request,
        name="send_follower_request",
    ),
    path("followers/<uuid:pk>/", api.followers, name="followers"),
    path(
        "followers/<uuid:pk>/<str:status>/", api.handle_request, name="handle_request"
    ),
    path("editprofile/", api.edit_profile, name="edit_profile"),
    path("editpassword/", api.edit_password, name="edit_password"),
    path(
        "followers/suggestions/",
        api.my_suggested_followers,
        name="my_suggested_followers",
    ),
]
