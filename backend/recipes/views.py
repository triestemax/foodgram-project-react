from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import (
    Favourite,
    Ingredients,
    IngredientsInRecipe,
    Recipes,
    Shopping_cart,
    Tag
)
from .filters import RecipesFilter
from .serializers import (
    IngredientsSerializer,
    TagsSerializer,
    RecipesSerializer,
    RecipesReadSerializer,
    RecipesCreateSerializer
)
from .pagination import CustomPaginator
from .permissions import (
    IsAuthorOrAdminOrReadOnly,
)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name', )


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    pagination_class = CustomPaginator
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return (RecipesReadSerializer)
        return (RecipesCreateSerializer)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, **kwargs):
        try:
            recipe = get_object_or_404(Recipes, id=kwargs['pk'])
            if request.method == 'POST':
                serializer = RecipesSerializer(
                    recipe, data=request.data,
                    context={'request': request}
                )
                serializer.is_valid(raise_exception=True)
                if not Favourite.objects.filter(
                    user=request.user,
                    recipe=recipe
                ).exists():
                    Favourite.objects.create(user=request.user, recipe=recipe)
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                return Response(
                    {'detail': 'Рецепт уже был добавлен в избранное.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if request.method == 'DELETE':
                get_object_or_404(
                    Favourite, user=request.user,
                    recipe=recipe
                ).delete()
                return Response(
                    {'detail': 'Рецепт удален из избранного.'},
                    status=status.HTTP_204_NO_CONTENT
                )
        except Exception:
            raise exceptions.ValidationError(
                {'detail': 'Невозможно выполнить!'},
                code=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,),
        pagination_class=None
    )
    def shopping_cart(self, request, **kwargs):
        try:
            recipe = get_object_or_404(Recipes, id=kwargs['pk'])
            if request.method == 'POST':
                serializer = RecipesSerializer(
                    recipe, data=request.data,
                    context={'request': request}
                )
                serializer.is_valid(raise_exception=True)
                if not Shopping_cart.objects.filter(
                    user=request.user,
                    recipe=recipe
                ).exists():
                    Shopping_cart.objects.create(
                        user=request.user,
                        recipe=recipe
                    )
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED)
                return Response(
                    {'detail': 'Рецепт уже есть в спике покупок.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if request.method == 'DELETE':
                get_object_or_404(
                    Shopping_cart,
                    user=request.user,
                    recipe=recipe
                ).delete()
                return Response(
                    {'detail': 'Рецепт успешно удален из списка покупок.'},
                    status=status.HTTP_204_NO_CONTENT
                )
        except Exception:
            raise exceptions.ValidationError(
                {'detail': 'Невозможно выполнить!'},
                code=status.HTTP_400_BAD_REQUEST
            )

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def download_shopping_cart(self, request, **kwargs):
        ingredients = IngredientsInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_list = 'Список покупок:\n'
        shopping_list += '\n'.join([
            f'- {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        filename = f'{request.user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
