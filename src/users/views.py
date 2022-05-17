from src.users.models import User
from rest_framework import generics
from rest_framework import permissions
from src.users.serializers import UserSerializer, OrganizationUserSerializer
from django.db.models import Q


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class OrganizationUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = OrganizationUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            ~Q(id=self.request.user.id),
            Q(organization=self.request.user.organization)
        )




