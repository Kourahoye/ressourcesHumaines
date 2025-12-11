from django.urls import path

from Users.views import  Logout, RegisterView,LoginView, UserDeleteView,UserDetailView, UserupdateView,UserList, change_password,toggle_user_active
from django.views.generic import TemplateView

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',Logout,name="logout"),
    path('userDetail/<int:pk>/',UserDetailView.as_view(),name="userDetail"),
    path('edit/<int:pk>/',UserupdateView.as_view(),name="userEdit"),
    path('users/',UserList.as_view(),name="userList"),
    path('user/delete/<int:pk>/',UserDeleteView.as_view(),name="userDelete"),
     path("robots.txt", TemplateView.as_view(
        template_name="robots.txt",
        content_type="text/plain"
    )),
    path('toggle_active/<int:user_id>/', toggle_user_active, name='toggle_user_active'),
    path('password/change/', change_password.as_view(), name='password_change'),

]