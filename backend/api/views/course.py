from django.db.models import Count
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from courses.models import Course

from ..serializers import CourseSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all courses'),
    create=extend_schema(summary='Add a new course'),
    retrieve=extend_schema(summary='Get course by id'),
    partial_update=extend_schema(
        summary='Change course fields by course id'
    ),
    destroy=extend_schema(summary='Delete course by id'),
)
class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Course.objects.all().annotate(lessons_count=Count('lessons'))
