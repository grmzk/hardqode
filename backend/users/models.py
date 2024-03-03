from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Username',
        max_length=150,
        unique=True,
        blank=False,
    )

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['username']

    def __str__(self):
        return f'Student[{self.username}]'

    def is_course_student(self, course) -> bool:
        return bool(set(course.study_groups.all())
                    .intersection(self.study_groups.all()))
