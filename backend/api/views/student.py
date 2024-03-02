from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from users.models import Student

from ..serializers import GroupSerializer, LessonSerializer, StudentSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all students'),
    create=extend_schema(summary='Add a new student'),
    retrieve=extend_schema(summary='Get student by id'),
    partial_update=extend_schema(
        summary='Change student fields by student id'
    ),
    destroy=extend_schema(summary='Delete student by id'),
    get_course_lessons=extend_schema(
        summary='Get course lessons that the student has access to'
    ),
    add_to_course=extend_schema(summary='Add student to course', request=None),
)
class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Student.objects.all()

    @action(detail=True, methods=['get'],
            url_path=r'get_course_lessons/(?P<course_id>[^/.]+)')
    def get_course_lessons(self, request, pk=None, course_id=None):
        course = get_object_or_404(Course, id=course_id)
        student = get_object_or_404(Student, id=pk)
        if not student.is_course_student(course):
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                            data={'message': f'Student with id {pk} '
                                             'does not have access to course '
                                             f'with id {course_id}!'})
        serializer = LessonSerializer(instance=course.lessons.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(detail=True, methods=['post'],
            url_path=r'add_to_course/(?P<course_id>[^/.]+)')
    def add_to_course(self, request, pk=None, course_id=None):
        course = get_object_or_404(Course, id=course_id)
        student = get_object_or_404(Student, id=pk)
        if student.is_course_student(course):
            return Response(status=status.HTTP_409_CONFLICT,
                            data={'message': f'Student with id {pk} '
                                             'already added to course '
                                             f'with id {course_id}!'})
        course_students_max = (
            course.max_group_students * course.study_groups.count()
        )
        course_students_count = 0
        for group in course.study_groups.all():
            course_students_count += group.students.count()
        if course_students_count >= course_students_max:
            return Response(status=status.HTTP_409_CONFLICT,
                            data={'message': 'All groups for the course '
                                             f'with id {course_id} '
                                             'are filled in. '
                                             'You need to add a new group.'})
        course.add_student(student)
        serializer = GroupSerializer(instance=student.study_groups.all(),
                                     many=True)
        return Response(status=status.HTTP_201_CREATED, data=serializer.data)
