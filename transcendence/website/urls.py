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
		path('brique/', views.brique, name='brique'),
		path('test/', views.test, name='test'),
        path('increment_game/<int:player_id>/', views.increment_game, name='increment_game'),			#bouton +1 game (pong)
		path('increment_victory/<int:player_id>/', views.increment_victory, name='increment_victory'),	#bouton +1 victoire
		path('increment_defeat/<int:player_id>/', views.increment_defeat, name='increment_defeat'),		#bouton +1 défaite
		path('decrement_victory/<int:player_id>/', views.decrement_victory, name='decrement_victory'),	#bouton -1 victoire
		path('decrement_defeat/<int:player_id>/', views.decrement_defeat, name='decrement_defeat'),		#bouton -1 défaite
		path('resetWL/<int:player_id>/', views.resetWL, name='resetWL'),						#bouton reset Win et Lose
        path('check_login/', views.check_login, name='check_login'),
		path('add_friend/<int:id>/', views.add_friend, name='add_friend'),
		path('remove_friend/<int:id>/', views.remove_friend, name='remove_friend'),
		path('accept_friend_request/<int:id>/', views.accept_friend_request, name='accept_friend_request'),
		path('decline_friend_request/<int:id>/', views.decline_friend_request, name='decline_friend_request'),
		path('pong/sendscore/', views.sendscore, name='sendscore'),
]

handler404 = 'website.views.handler404'

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.IMGS_URL, document_root=settings.IMGS_ROOT)
