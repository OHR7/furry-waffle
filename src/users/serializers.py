from rest_framework import serializers

from src.users.models import Organization, User


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name']


class UserSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'last_updated', 'kudos_counter', 'organization', 'first_name', 'last_name']


class OrganizationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
