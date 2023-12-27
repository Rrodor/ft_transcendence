from django.urls import path, include
from . import views
from django.conf.urls import handler404
from .views import register

urlpatterns = [
		path('', views.main, name='main'),
		path('players/', views.players, name='players'),
		path('players/details/<int:id>', views.details, name='details'),
		path('login/', views.login_view, name='login'),
		path('register/', views.register, name='register'),
		path('logout/', views.logout_view, name='logout'),
		path('profile/', views.profile, name='profile'),
		path('increment_victory/<int:player_id>/', views.increment_victory, name='increment_victory'),
    	path('increment_defeat/<int:player_id>/', views.increment_defeat, name='increment_defeat'),
		path('decrement_victory/<int:player_id>/', views.decrement_victory, name='decrement_victory'),
		path('decrement_defeat/<int:player_id>/', views.decrement_defeat, name='decrement_defeat'),
		path('resetWL/<int:player_id>/', views.resetWL, name='resetWL'),
]

handler404 = 'website.views.handler404'

