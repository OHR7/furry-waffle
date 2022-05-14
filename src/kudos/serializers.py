from rest_framework import serializers

from src.kudos.models import Kudo


class KudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kudo
        fields = ['id', 'from_user', 'to_user', 'date', 'message']
