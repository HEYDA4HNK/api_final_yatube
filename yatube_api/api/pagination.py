"""Кастомные пагинации."""

from rest_framework.pagination import LimitOffsetPagination


class PostPagination(LimitOffsetPagination):
    """Пагинация."""

    default_limit = 10
