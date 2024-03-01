from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from users.models import Author

from ..serializers import AuthorSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all authors'),
    create=extend_schema(summary='Add a new author'),
    retrieve=extend_schema(summary='Get author by id'),
    partial_update=extend_schema(summary='Change author fields by author id'),
    destroy=extend_schema(summary='Delete author by id'),
)
class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Author.objects.all()
