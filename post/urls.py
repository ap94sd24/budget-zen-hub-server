from django.urls import path

from  . import api 

urlpatterns = [
    path('', api.post_list, name='post_list'),
    path('<uuid:pk>/like/', api.post_like, name='post_like'),
    path('<uuid:pk>/comment/', api.post_create_comment, name='post_create_comment'),
    path('<uuid:pk>/delete/', api.delete_post, name='delete_post'),
    path('<uuid:pk>/report/', api.report_post, name='report_post'),
    path('profile/<uuid:id>/', api.post_list_profile, name='post_list_profile'),
    path('create/', api.post_create, name='post_create'),
    path('<uuid:pk>/', api.post_detail, name='post_detail'),
    path('trends/', api.get_trends, name='get_trends'),
]
