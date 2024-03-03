from datetime import datetime

import pytz
from rest_framework import status
from rest_framework.test import APITestCase

from courses.models import Course, Group, Lesson
from users.models import User


class StudentsGetCourseLessonsTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='author')
        cls.student = User.objects.create_user(username='student')
        cls.course = Course.objects.create(
            name='course',
            start_date=datetime.now(tz=pytz.UTC),
            cost=10,
            author=cls.author,
            min_group_students=1,
            max_group_students=5,
        )

    def test_student_404(self):
        response = self.client.get(f'/api/users/{self.student.id + 1}'
                                   f'/get_course_lessons/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_course_404(self):
        response = self.client.get(
            f'/api/users/{self.student.id}'
            f'/get_course_lessons/{self.course.id + 1}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_alien_student(self):
        response = self.client.get(f'/api/users/{self.student.id}'
                                   f'/get_course_lessons/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_200(self):
        group = Group.objects.create(
            name='group',
            course=self.course,
        )
        group.students.add(self.student)
        response = self.client.get(f'/api/users/{self.student.id}'
                                   f'/get_course_lessons/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
        lessons_count = 3
        for i in range(lessons_count):
            Lesson.objects.create(
                name=f'lesson_{i}',
                url=f'https://example.com/lesson_{i}',
                course=self.course
            )
        response = self.client.get(f'/api/users/{self.student.id}'
                                   f'/get_course_lessons/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), lessons_count)


class StudentsAddToCourseTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(username='author')
        cls.student = User.objects.create_user(username='student')
        cls.course = Course.objects.create(
            name='course',
            start_date=datetime.now(tz=pytz.UTC),
            cost=10,
            author=cls.author,
            min_group_students=1,
            max_group_students=5,
        )

    def test_student_404(self):
        response = self.client.get(f'/api/users/{self.student.id + 1}'
                                   f'/get_course_lessons/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_course_404(self):
        response = self.client.get(
            f'/api/users/{self.student.id}'
            f'/get_course_lessons/{self.course.id + 1}/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_one_student(self):
        group = Group.objects.create(
            name='group',
            course=self.course,
        )
        response = self.client.post(f'/api/users/{self.student.id}'
                                    f'/add_to_course/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertListEqual(list(self.student.study_groups.all()), [group])

    def test_add_many_students(self):
        groups_count = 5
        for i in range(groups_count):
            Group.objects.create(
                name=f'group_{i}',
                course=self.course,
            )
        for i in range(groups_count * self.course.max_group_students):
            student = User.objects.create(username=f'student_{i}')
            response = self.client.post(f'/api/users/{student.id}'
                                        f'/add_to_course/{self.course.id}/')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        extra_student = User.objects.create(username='extra_student')
        response = self.client.post(f'/api/users/{extra_student.id}'
                                    f'/add_to_course/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
