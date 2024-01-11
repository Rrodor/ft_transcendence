import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "transcendence.settings")
django.setup()

from website.models import User  # Assurez-vous que le chemin d'accès est correct

def reinitialiser_statistiques_pong():
    for objet in User.objects.all():
        objet.total_pong_games = 0
        objet.pong_victories = 0
        objet.pong_defeats = 0
        objet.pong_points_for = 0
        objet.pong_points_against = 0
        objet.pong_wl_ratio = 0
        objet.pong_points_ratio = 0
        objet.pong_average_for = 0
        objet.pong_average_against = 0
        objet.pong_victories_percentage = 0
        objet.pong_defeats_percentage = 0
        objet.save()

if __name__ == "__main__":
    reinitialiser_statistiques_pong()
