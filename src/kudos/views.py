import datetime

from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from src.kudos.models import Kudo

from src.kudos.permissions import IsOnSameOrg
from src.kudos.serializers import KudoSerializer
from src.users.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsOnSameOrg])
def give_kudos(request, user_id):
    to_user = get_object_or_404(User, pk=user_id)

    today = datetime.date.today()
    start_week = today - datetime.timedelta(today.weekday())
    if request.user.last_updated < start_week:
        request.user.kudos_counter = 3
        request.user.save()

    if request.user.id == to_user.id:
        return Response({'detail': "Can't give your self kudos mate! :C"}, status=HTTP_400_BAD_REQUEST)

    if not request.user.kudos_counter > 0:
        return Response({'detail': 'Not Enough Kudos left for this Week :(.'}, status=HTTP_400_BAD_REQUEST)

    kudos = Kudo.objects.create(
        from_user=request.user,
        to_user=to_user,
        message=request.data['message']
    )
    request.user.kudos_counter -= 1
    request.user.last_updated = today
    request.user.save()

    kudos_serializer = KudoSerializer(kudos)
    return Response(kudos_serializer.data, status=HTTP_201_CREATED)


class UsersKudos(generics.ListAPIView):
    queryset = Kudo.objects.all()
    serializer_class = KudoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(
            to_user=self.request.user
        ).order_by('-date')
