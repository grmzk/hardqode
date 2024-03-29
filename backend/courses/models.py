from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(
        verbose_name='Course Name',
        max_length=200,
        unique=True,
        blank=False,
    )
    start_date = models.DateTimeField(
        verbose_name='Start Date'
    )
    cost = models.PositiveIntegerField(
        verbose_name='Cost'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Author',
        related_name='courses',
        on_delete=models.CASCADE,
        blank=False,
    )
    min_group_students = models.PositiveIntegerField(
        verbose_name='Min Students In Group',
        blank=False,
    )
    max_group_students = models.PositiveIntegerField(
        verbose_name='Max Students In Group',
        blank=False,
    )

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['id']

    def __str__(self):
        return f'Course[{self.name}]'

    def add_student(self, student: User):
        groups = list(self.study_groups.all())
        for i in range(len(groups)):
            if groups[i].students.count() < self.min_group_students:
                groups[i].students.add(student)
                break
        else:
            for i in range(len(groups)):
                if (groups[i - 1].students.count()
                        > groups[i].students.count()):
                    groups[i].students.add(student)
                    break
            else:
                groups[0].students.add(student)


class Lesson(models.Model):
    name = models.CharField(
        verbose_name='Lesson Name',
        max_length=200,
        unique=True,
        blank=False,
    )
    url = models.URLField(
        verbose_name='URL',
        max_length=1000,
    )
    course = models.ForeignKey(
        Course,
        verbose_name='Course',
        related_name='lessons',
        on_delete=models.CASCADE,
        blank=False,
    )

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['id']

    def __str__(self):
        return f'Lesson[{self.name}]'


class Group(models.Model):
    name = models.CharField(
        verbose_name='Group Name',
        max_length=200,
        unique=True,
        blank=False,
    )
    course = models.ForeignKey(
        Course,
        verbose_name='Course',
        related_name='study_groups',
        on_delete=models.CASCADE,
        blank=False,
    )
    students = models.ManyToManyField(
        User,
        verbose_name='Students',
        related_name='study_groups',
        blank=True,
    )

    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['id']

    def __str__(self):
        return f'Group[{self.name}]'
