import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendence.settings')
django.setup()

from website.models import User, Tournament, Match
from website.views import create_tournament, join_tournament
from django.test import RequestFactory

def create_tournament_and_add_participants():
    # Créer un tournoi
    factory = RequestFactory()
    request = factory.get('/')
    request.user = User.objects.get(username='tzec')
    create_tournament(request)
    import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transcendence.settings')
django.setup()

from website.models import User, Tournament, Match
from website.views import create_tournament, join_tournament
from django.test import RequestFactory

def create_tournament_and_add_participants():
    # Créer un tournoi
    factory = RequestFactory()
    request = factory.get('/')
    request.user = User.objects.get(username='tzec')
    create_tournament(request)
    name = {
        'test01': 'test01',
        'test03': 'test03',
        'test02': 'test02',
        'rrodor': 'rrodor',
        'aramon': 'aramon',
        'test00': 'test00',
    }
    for username in name:
        request.user = User.objects.get(username=username)
        join_tournament(request)

if __name__ == "__main__":
    Tournament.objects.all().delete()
    Match.objects.all().delete()
    create_tournament_and_add_participants()

if __name__ == "__main__":
    Tournament.objects.all().delete()
    Match.objects.all().delete()
    create_tournament_and_add_participants()
    print("Tournament created")