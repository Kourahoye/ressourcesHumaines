from django.urls import path
from permissions.views import Permissions, get_user_permissions, get_permissions, get_users, remove_all_user_permissions, remove_user_permissions


urlpatterns = [
    path('getperms/', get_permissions,name='get_perms'),
    path('getusers/',get_users,name='get_users'),
    path('get_user_permissions/', get_user_permissions, name='get_user_permissions'),
    path('',Permissions.as_view(),name='add_permissions'),
    path('remove_all_user_permissions/', remove_all_user_permissions, name='remove_all_user_permissions'),
    path('remove_permissions/',remove_user_permissions,name='remove_user_permissions')
]