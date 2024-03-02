from rest_framework import serializers

from courses.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    url = serializers.URLField(max_length=1000)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        fields = ['id', 'name', 'url', 'course']
        model = Lesson

    @staticmethod
    def validate_name(name):
        if Lesson.objects.filter(name=name).count():
            raise serializers.ValidationError(
                'This name is already exists.'
            )
        return name
