from django.urls import path
from .views.ratings import topgamerating_list

urlpatterns = [
    path('reports/topgameratings', topgamerating_list),
]
