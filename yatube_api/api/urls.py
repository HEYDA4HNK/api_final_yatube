"""УРЛы."""
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from api import views

router = SimpleRouter()
router.register(r'v1/posts', views.PostList, basename='posts')
router.register(r'v1/groups', views.GroupViewSet, basename='groups')
urlpatterns = [
    path('v1/follow/', views.FollowViewSet.as_view({'get': 'list',
                                                    'post': 'create'})),
    path('v1/posts/<int:post_id>/comments/<int:comment_id>/',
         views.CommentViewSet.as_view({'get': 'retrieve',
                                       'put': 'update',
                                       'patch': 'partial_update',
                                       'delete': 'destroy'})),
    path('v1/posts/<int:post_id>/comments/',
         views.CommentViewSet.as_view({'get': 'list',
                                       'post': 'create'})),
    path('', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]
