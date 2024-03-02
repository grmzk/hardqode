from rest_framework import serializers

from users.models import Author, User


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)

    class Meta:
        fields = ['id', 'username']
        model = Author

    @staticmethod
    def validate_username(username):
        if User.objects.filter(username=username).count():
            raise serializers.ValidationError(
                'This username is already exists.'
            )
        return username
