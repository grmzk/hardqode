from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# from .views import (IngredientViewSet, RecipeViewSet, TagViewSet,
#                     TokenCreateResponse201View, UserViewSet)

router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='docs'),
]
