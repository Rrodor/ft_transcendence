from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import UserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def main(request):
    context = {
        'user': request.user,
    }
    return render(request, 'main.html', context)

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
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Account created successfully')
                return redirect('main')  # Redirigez vers la page appropriée
            else:
                messages.error(request, 'Error in user authentication')
        else:
            messages.error(request, 'Error in form submission')
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('passsword')
            user = authenticate(username=username, password=password)
            user = form.get_user()
            login(request, user)
            # Rediriger vers une page de succès/après connexion
            return redirect('main')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
	logout(request)
	return redirect('main')

def profile(request):
	return render(request, 'profile.html')