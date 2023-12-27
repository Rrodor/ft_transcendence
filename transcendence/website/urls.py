from django.urls import path, include
from . import views
from django.conf.urls import handler404
from .views import register

urlpatterns = [
		path('', views.main, name='main'),
		path('main/', views.main, name='main'),
		path('players/', views.players, name='players'),
		path('players/details/<int:id>', views.details, name='details'),
		path('login/', views.login_view, name='login'),
		path('register/', views.register, name='register'),
		path('logout/', views.logout_view, name='logout'),
		path('profile/', views.profile, name='profile'),
]

handler404 = 'website.views.handler404'

