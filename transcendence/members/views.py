from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Player

def players(request):
    players = Player.objects.all().values()
    template = loader.get_template('all_members.html')
    context = {
        'players': players
    }
    return (HttpResponse(template.render(context, request)))

def details(request, id):
    player = Player.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
            'player': player,
    }
    return (HttpResponse(template.render(context, request)))

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def testing(request):
	template = loader.get_template('template.html')
	context = {
		'fruits': ['Apple', 'Banana', 'Cherry'],
	}
	return HttpResponse(template.render(context, request))
