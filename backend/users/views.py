from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.response import Response


from recipes.pagination import CustomPaginator
from .models import Subscribe, User
from .serializers import SubscriptionSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPaginator

    @action(
        detail=False,
        methods=('get',),
        serializer_class=SubscriptionSerializer,
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(subscribing__user=user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=('post', 'delete',),
    )
    def subscribe(self, request, **kwargs):
        user = request.user
        if request.method == 'POST':
            author_id = self.kwargs.get('id')
            author = get_object_or_404(User, id=author_id)
            if user == author:
                raise exceptions.ValidationError(
                    {'detail': 'Подписаться на самого себя нельзя!'},
                    code=status.HTTP_400_BAD_REQUEST
                )
            elif Subscribe.objects.filter(
                user=user,
                author=author
            ).exists():
                raise exceptions.ValidationError(
                    {'detail': 'Вы уже подписаны на этого автора!'},
                    code=status.HTTP_400_BAD_REQUEST
                )
            Subscribe.objects.create(user=user, author=author)
            serializer = SubscriptionSerializer(
                author,
                context={"request": request}
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            try:
                author_id = self.kwargs.get('id')
                author = get_object_or_404(User, id=author_id)
                subscription = get_object_or_404(
                    Subscribe,
                    user=user,
                    author=author
                )
            except Exception:
                raise exceptions.ValidationError(
                    {'detail': 'Невозможно выполнить!'},
                    code=status.HTTP_400_BAD_REQUEST
                )
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
