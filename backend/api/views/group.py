from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from courses.models import Group

from ..serializers import GroupSerializer


@extend_schema_view(
    list=extend_schema(summary='Get all groups'),
    create=extend_schema(summary='Add a new group'),
    retrieve=extend_schema(summary='Get group by id'),
    partial_update=extend_schema(
        summary='Change group fields by group id'
    ),
    destroy=extend_schema(summary='Delete group by id'),
)
class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Group.objects.all()
