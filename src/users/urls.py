from django.urls import path
from src.users.views import UserDetailView, OrganizationUsers

urlpatterns = [
    path('profile/', UserDetailView.as_view(), name='user-profile'),
    path('organizations/', OrganizationUsers.as_view(), name='organization-list'),
]
