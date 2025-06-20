from django.urls import path

from .views import CongesCreateView, CongesList, CongesRequestCreateView,CongesRequestList, CongesRequetsDelete, acceptRequest, finishConges, refuseRequest,CongesRequestDetails,deleteConges, unfinishConges

urlpatterns = [
    path('request/create/',CongesRequestCreateView.as_view(),name="conges_request_create"),
    path('request/accept/<int:pk>/',acceptRequest,name="conges_request_accept"),
    path('request/refuse/<int:pk>/',refuseRequest,name="conges_request_refuse"),
    path('requests/',CongesRequestList.as_view(),name="conges_request_list"),
    path("request/delete/<int:pk>/",CongesRequetsDelete.as_view(),name="conges_request_delete"),
    path("request/details/<int:pk>/",CongesRequestDetails.as_view(),name="conges_request_details"),
    path("",CongesList.as_view(),name="conges_list"),
    path("create/",CongesCreateView.as_view(),name="conges_create"),
    path("delete/<int:pk>/",deleteConges,name="conges_delete"),
    path("conges/finish/<int:pk>/",finishConges,name="conges_finish"),
    path("conges/unfinish/<int:pk>/",unfinishConges,name="conges_unfinish"),
]
