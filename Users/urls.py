from django.urls import path

from Users.views import  Logout, RegisterView,LoginView, UserDeleteView,UserDetailView, UserupdateView,UserList

urlpatterns = [
    path('register/',RegisterView.as_view(),name="register"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',Logout,name="logout"),
    path('userDetail/<int:pk>/',UserDetailView.as_view(),name="userDetail"),
    path('edit/<int:pk>/',UserupdateView.as_view(),name="userEdit"),
    path('users/',UserList.as_view(),name="userList"),
    path('user/delete/<int:pk>/',UserDeleteView.as_view(),name="userDelete"),
]