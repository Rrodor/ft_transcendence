from django.urls import path
from . import views

urlpatterns = [
		path('', views.main, name='main'),
        path('players/', views.players, name='players'),
        path('players/details/<int:id>', views.details, name='details'),
		path('testing/', views.testing, name='testing'),
]
