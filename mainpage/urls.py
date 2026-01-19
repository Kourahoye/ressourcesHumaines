from django.urls import path
from .views import Dasboard, notification_count
urlpatterns = [
    path('',Dasboard.as_view(),name='dashbord'),
    path("notifications/count/", notification_count)

]