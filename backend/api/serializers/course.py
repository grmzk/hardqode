from rest_framework import serializers

from courses.models import Course
from users.models import Author


class CourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    start_date = serializers.DateTimeField()
    cost = serializers.IntegerField(min_value=0)
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ['id', 'name', 'start_date', 'cost', 'author',
                  'lessons_count']
        model = Course
