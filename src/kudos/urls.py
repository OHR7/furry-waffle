from django.urls import path

from src.kudos.views import give_kudos, UsersKudos

urlpatterns = [
    path('give/<int:user_id>/', give_kudos, name='give-kudos'),
    path('received/', UsersKudos.as_view(), name='kudos-received'),
]
