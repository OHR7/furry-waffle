from rest_framework import serializers

from src.kudos.models import Kudo
from src.users.serializers import OrganizationUserSerializer


class KudoSerializer(serializers.ModelSerializer):
    from_user = OrganizationUserSerializer(many=False, read_only=True)

    class Meta:
        model = Kudo
        fields = ['id', 'from_user', 'to_user', 'date', 'message']
