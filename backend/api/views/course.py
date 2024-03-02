from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from courses.models import Course

from ..serializers import CourseSerializer, GroupSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all courses'),
    create=extend_schema(summary='Add a new course'),
    retrieve=extend_schema(summary='Get course by id'),
    partial_update=extend_schema(
        summary='Change course fields by course id'
    ),
    destroy=extend_schema(summary='Delete course by id'),
    rebalance_groups=extend_schema(summary='Rebalance students in groups',
                                   request=None),
)
class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Course.objects.all().annotate(lessons_count=Count('lessons'))

    @action(detail=True, methods=['post'], url_path='rebalance_groups')
    def rebalance_groups(self, request, pk=None):
        course = get_object_or_404(Course, id=pk)
        students = list()
        for group in course.study_groups.all():
            students.extend(group.students.all())
            group.students.clear()
        for student in students:
            course.add_student(student)
        serializer = GroupSerializer(instance=course.study_groups.all(),
                                     many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)
