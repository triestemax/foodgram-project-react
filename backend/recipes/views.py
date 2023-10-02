from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from recipes.models import Ingredients, Tag, Recipes
from .serializers import (
    IngredientsSerializer,
    TagsSerializer,
    RecipesReadSerializer,
    RecipesCreateSerializer,
    )
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = PageNumberPagination


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrReadOnly, IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)
    #filterset_class = RecipesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipesReadSerializer
        return RecipesCreateSerializer
