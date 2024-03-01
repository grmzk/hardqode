from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from users.models import Student

from ..serializers import StudentSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all students'),
    create=extend_schema(summary='Add a new student'),
    retrieve=extend_schema(summary='Get student by id'),
    partial_update=extend_schema(
        summary='Change student fields by student id'
    ),
    destroy=extend_schema(summary='Delete student by id'),
)
class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Student.objects.all()
