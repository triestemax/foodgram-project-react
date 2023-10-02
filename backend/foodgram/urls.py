from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter


from recipes.views import IngredientsViewSet, TagsViewSet, RecipesViewSet
from users.views import CustomUserViewSet

router = DefaultRouter()

router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)
router.register('tags', TagsViewSet)
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
