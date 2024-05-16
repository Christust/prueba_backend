from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from django.conf import settings


class HasGroupPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if settings.DEBUG:
            return True
        required_user_types = view.permission_types.get(view.action)
        if required_user_types == None:
            return request.user.user_type == "superadmin"
        elif "all" in required_user_types or request.user.user_type == "superadmin":
            return True
        else:
            return request.user.user_type in required_user_types


class BaseGenericViewSet(viewsets.GenericViewSet):
    model = None
    out_serializer_class = None
    serializer_class = None
    queryset = None
    permission_classes = [HasGroupPermission]
    permission_types = {}
    searched_object = None
    offset = 0
    limit = 100

    def get_object(self, pk):
        return get_object_or_404(self.queryset, pk=pk)


class BaseModelViewSet(viewsets.ModelViewSet):
    model = None
    out_serializer_class = None
    serializer_class = None
    queryset = None
    permission_classes = [HasGroupPermission]
    permission_types = {}
    searched_object = None
    offset = 0
    limit = 100

    def get_object(self, pk):
        return get_object_or_404(self.queryset, pk=pk)
