from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Player
from .forms import RegistrationForm

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


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigez l'utilisateur vers une page de confirmation ou une autre page
            return redirect('main/')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})
