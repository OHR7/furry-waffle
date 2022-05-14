from django.urls import path

from src.kudos.views import give_kudos

urlpatterns = [
    path('give/<int:user_id>/', give_kudos, name='give-kudos'),
]
