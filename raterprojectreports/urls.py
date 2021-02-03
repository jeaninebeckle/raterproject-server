from django.urls import path
from .views.ratings import topgamerating_list, bottomgamerating_list
from .views.categories import gamecategory_list
from .views.players import numberofplayers_list, suitableforkids_list
from .views.reviews import mostreviewedgame


urlpatterns = [
    path('reports/topgameratings', topgamerating_list),
    path('reports/bottomgameratings', bottomgamerating_list),
    path('reports/gamecategories', gamecategory_list),
    path('reports/gameplayers', numberofplayers_list),
    path('reports/mostreviewedgame', mostreviewedgame),
    path('reports/suitableforkids', suitableforkids_list)
]
