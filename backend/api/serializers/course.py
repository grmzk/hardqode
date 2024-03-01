from rest_framework import serializers

from courses.models import Course
from users.models import Author


class CourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    start_date = serializers.DateTimeField()
    cost = serializers.IntegerField(min_value=0)
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    min_group_students = serializers.IntegerField(min_value=0)
    max_group_students = serializers.IntegerField(min_value=1)
    lessons_count = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ['id', 'name', 'start_date', 'cost', 'author',
                  'min_group_students', 'max_group_students', 'lessons_count']
        model = Course

    def validate(self, attrs):
        if attrs['min_group_students'] > attrs['max_group_students']:
            raise serializers.ValidationError(
                'max_group_students must be greater '
                'than or equal to min_group_students'
            )
        return attrs
