from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from .views import (AuthorViewSet, CourseViewSet, GroupViewSet, LessonViewSet,
                    StudentViewSet)

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='user')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'groups', GroupViewSet, basename='group')


urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='docs'),
]
