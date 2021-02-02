from django.urls import path
from .views.ratings import topgamerating_list, bottomgamerating_list

urlpatterns = [
    path('reports/topgameratings', topgamerating_list),
    path('reports/bottomgameratings', bottomgamerating_list),
]
