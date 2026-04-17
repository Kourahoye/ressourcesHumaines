from django.urls import path

from .views import SendFormview, mark_notification_read, notifications_list, send_message


urlpatterns = [
    path("", SendFormview.as_view(), name="send_message"),
    path("notif",notifications_list,name="notifications_list"),
    path("notification/mark_read/<int:pk>",mark_notification_read,name="notification_read"),
    path("mark_all_read/", mark_notification_read, name="mark_all_notifications_read")
]
