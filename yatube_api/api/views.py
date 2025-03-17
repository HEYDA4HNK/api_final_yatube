"""Вьювсы."""
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from django.shortcuts import get_object_or_404
from .serializers import (PostSerializer,
                          CommentSerializer,
                          GroupSerializer,
                          FollowSerializer)
from .pagination import PostPagination
from posts.models import Post, Comment, Group, Follow
from rest_framework import status, permissions, filters
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class FollowViewSet(ModelViewSet):
    """Подписки."""

    queryset = Follow
    serializer_class = FollowSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ('following__username',)
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request):
        """Получение подписок."""
        queryset = self.get_queryset().objects.filter(user=request.user)
        queryset = self.filter_queryset(queryset)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Создание подписки."""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid() and 'following' in dict(request.data):
            user = get_user_model()
            following = get_object_or_404(user,
                                          username=request.data["following"])
            user = Follow.objects.filter(following=following,
                                         user=request.user).all()
            if len(user) == 0 and following != request.user:
                serializer.save(user=request.user, following=following)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(ReadOnlyModelViewSet):
    """Группы."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]


class PostList(ModelViewSet):
    """Посты."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    pagination_class = PostPagination

    def list(self, request):
        """Получение постов."""
        queryset = self.get_queryset()
        if (request.GET.get('offset') or request.GET.get('limit')):
            paginator = self.pagination_class()
            page = paginator.paginate_queryset(queryset, request)
            serializer = self.serializer_class(page, many=True)
            response_data = {
                'count': paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': serializer.data,
            }
        else:
            serializer = self.serializer_class(queryset, many=True)
            response_data = serializer.data
        return Response(response_data)

    def create(self, request):
        """Создание поста."""
        serializer = self.serializer_class(data=request.data)
        if (serializer.is_valid()):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        """Обновление поста."""
        post = get_object_or_404(self.get_queryset(), pk=pk)
        if (request.user != post.author):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(post, data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk):
        """Частичное обновление поста."""
        post = get_object_or_404(self.get_queryset(), pk=pk)
        if (request.user != post.author):
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(post,
                                           data=request.data,
                                           partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk):
        """Удаление поста."""
        post = get_object_or_404(self.get_queryset(), pk=pk)
        if (request.user != post.author):
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(ModelViewSet):
    """комментарии."""

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def list(self, request, post_id):
        """Список комментариев."""
        page = self.get_queryset().filter(post=post_id)
        serializer = self.serializer_class(page, many=True)
        return Response(serializer.data)

    def create(self, request, post_id):
        """Создание коммента."""
        get_object_or_404(Post.objects.all(), pk=post_id)
        data = request.POST.copy()
        data['post'] = post_id
        serializer = self.serializer_class(data=data)
        if (serializer.is_valid()):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, post_id, comment_id):
        """Получения коммента."""
        post = get_object_or_404(Post.objects.all(), pk=post_id)
        comment = get_object_or_404(self.get_queryset(), pk=comment_id)
        if (comment.post.pk == post.pk):
            serializer = self.serializer_class(comment)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def update(self, request, post_id, comment_id):
        """Обновление коммента."""
        post = get_object_or_404(Post.objects.all(), pk=post_id)
        comment = get_object_or_404(self.get_queryset(), pk=comment_id)
        if (comment.post.pk != post.pk):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if (request.user != comment.author):
            return Response(status=status.HTTP_403_FORBIDDEN)
        data = request.POST.copy()
        data['post'] = post_id
        serializer = self.serializer_class(comment, data=data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, post_id, comment_id):
        """Частичное обновление коммента."""
        post = get_object_or_404(Post.objects.all(), pk=post_id)
        comment = get_object_or_404(self.get_queryset(), pk=comment_id)
        if (comment.post.pk != post.pk):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if (request.user != comment.author):
            return Response(status=status.HTTP_403_FORBIDDEN)
        data = request.POST.copy()
        data['post'] = post_id
        serializer = self.serializer_class(comment, data=data, partial=True)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, post_id, comment_id):
        """Удаление коммента."""
        post = get_object_or_404(Post.objects.all(), pk=post_id)
        comment = get_object_or_404(self.get_queryset(), pk=comment_id)
        if (comment.post.pk != post.pk):
            return Response(status=status.HTTP_404_NOT_FOUND)
        if (request.user != comment.author):
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
