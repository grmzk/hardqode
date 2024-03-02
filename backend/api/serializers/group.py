from rest_framework import serializers

from courses.models import Course, Group
from users.models import Student


class GroupSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    students = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), many=True
    )

    class Meta:
        fields = ['id', 'name', 'course', 'students']
        model = Group

    @staticmethod
    def validate_name(name):
        if Group.objects.filter(name=name).count():
            raise serializers.ValidationError(
                'This name is already exists.'
            )
        return name
