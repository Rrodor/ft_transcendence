from django.urls import path, include
from . import views
from django.conf.urls import handler404
from .views import register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
		path('', views.main, name='main'),
		path('main/', views.main, name='main'),
		path('players/', views.players, name='players'),
		path('players/details/<int:id>', views.details, name='details'),
		path('login/', views.login_view, name='login'),
		path('register/', views.register, name='register'),
		path('logout/', views.logout_view, name='logout'),
		path('profile/', views.profile, name='profile'),
		path('pong/', views.pong, name='pong'),
		path('increment_victory/<int:player_id>/', views.increment_victory, name='increment_victory'),	#bouton +1 victoire
		path('increment_defeat/<int:player_id>/', views.increment_defeat, name='increment_defeat'),		#bouton +1 défaite
		path('decrement_victory/<int:player_id>/', views.decrement_victory, name='decrement_victory'),	#bouton -1 victoire
		path('decrement_defeat/<int:player_id>/', views.decrement_defeat, name='decrement_defeat'),		#bouton -1 défaite
		path('resetWL/<int:player_id>/', views.resetWL, name='resetWL'),								#bouton reset Win et Lose
]

handler404 = 'website.views.handler404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
