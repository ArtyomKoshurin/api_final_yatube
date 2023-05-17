from rest_framework import viewsets, filters
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404

from posts.models import Post, Group, Comment, User
from .permissions import PostAuthorOnly
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о всех постах и позволяющий
    создать, отредактировать или удалить пост."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostAuthorOnly, IsAuthenticatedOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет, отображающий информацию о всех группах."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о комментариях поста и позволяющий
    создать, отредактировать или удалить комментарий."""
    serializer_class = CommentSerializer
    permission_classes = [PostAuthorOnly, IsAuthenticatedOrReadOnly]

    def post_finding(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return Comment.objects.filter(post=self.post_finding())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=self.post_finding())


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет, отображающий информацию о подписках и позволяющий подписаться
    на автора."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        queryset = get_object_or_404(User, username=self.request.user)
        return queryset.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
