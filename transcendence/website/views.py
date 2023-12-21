from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from .forms import RegistrationForm

# Create your views here.
def main(request):
	template = loader.get_template('main.html')
	return HttpResponse(template.render())

def players(request):
	all_users = User.objects.all().values()
	template = loader.get_template('players.html')
	context = {
		'all_users': all_users,
	}
	return HttpResponse(template.render(context, request))

def details(request, id):
    player = User.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
            'player': player,
    }
    return (HttpResponse(template.render(context, request)))

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
