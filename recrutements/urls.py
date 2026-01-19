from django.urls import path


from recrutements.views import DeleteOffreView, OffreCreateView, OffreListView, OffreUpdateView, PostulationDetailView, PostulationListView, PostulerOffreView, offres_publiques


urlpatterns = [
    path('offre/', OffreListView.as_view(), name='offre-list'),
    path('offre/create/', OffreCreateView.as_view(), name='offre-create'),
    path('offre/update/<int:pk>/', OffreUpdateView.as_view(), name='offre-update'),
    path('offre/<int:offre_id>/postuler/', PostulerOffreView.as_view(), name='postuler_offre'),
    path('postulations/', PostulationListView.as_view(), name='postulation_list'),
    path('postulation/<int:pk>/', PostulationDetailView.as_view(), name='postulation_detail'),
    path('offre/<int:pk>/delete/', DeleteOffreView.as_view(), name='delete_offre'),
     path('offres/public', offres_publiques, name='offres_publiques'),
]