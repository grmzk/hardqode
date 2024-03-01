from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from courses.models import Lesson

from ..serializers import LessonSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all lessons'),
    create=extend_schema(summary='Add a new lesson'),
    retrieve=extend_schema(summary='Get lesson by id'),
    partial_update=extend_schema(
        summary='Change lesson fields by lesson id'
    ),
    destroy=extend_schema(summary='Delete lesson by id'),
)
class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Lesson.objects.all()
