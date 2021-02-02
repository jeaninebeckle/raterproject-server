from raterprojectapi.views.gamepicture import GamePictures
from django.conf.urls import include
from django.urls import path
from raterprojectapi.views import register_user, login_user
from rest_framework import routers
from raterprojectapi.views import Games, Categories, Reviews, Ratings
from django.conf import settings
from django.conf.urls.static import static



router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', Games, 'game')
router.register(r'categories', Categories, 'category')
router.register(r'reviews', Reviews, 'review')
router.register(r'ratings', Ratings, 'rating')
router.register(r'image', GamePictures, 'image')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('', include('raterprojectreports.urls')),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
