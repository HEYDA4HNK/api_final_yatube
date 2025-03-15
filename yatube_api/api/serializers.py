"""Сериализеры."""
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Post, Group, Follow


class FollowSerializer(serializers.ModelSerializer):
    """Подписки сериализер."""

    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """Мета."""

        fields = ('user', 'following',)
        model = Follow


class GroupSerializer(serializers.ModelSerializer):
    """Групп сериализер."""

    class Meta:
        """Мета."""

        fields = '__all__'
        model = Group


class PostSerializer(serializers.ModelSerializer):
    """Пост сериализер."""

    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        """Мета."""

        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    """Коммент сериализер."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        """Мета."""

        fields = '__all__'
        model = Comment
