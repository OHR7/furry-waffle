import logging

from rest_framework.permissions import BasePermission

from src.users.models import User


logger = logging.getLogger(__name__)


def is_on_same_org(request, obj=None):
    try:
        if obj.organization and obj.organization == request.user.organization:
            return True
        else:
            return False
    except Exception as e:
        logger.error(e)
        return False


class IsOnSameOrg(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return is_on_same_org(request, obj)
