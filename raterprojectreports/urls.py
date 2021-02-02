from django.urls import path
from .views.ratings import topgamerating_list, bottomgamerating_list
from .views.categories import gamecategory_list

urlpatterns = [
    path('reports/topgameratings', topgamerating_list),
    path('reports/bottomgameratings', bottomgamerating_list),
    path('reports/gamecategories', gamecategory_list),
]
