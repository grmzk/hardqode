from rest_framework import serializers

from users.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)

    class Meta:
        fields = ['id', 'username']
        model = Author
