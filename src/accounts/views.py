from django.contrib import messages
from django.contrib.auth import logout, login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, User
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserCreate, UserUpdate


# Create your views here.
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/admin/')
        else:
            messages.info(request, "Veuillez compléter correctement les champs « nom d’utilisateur » et « mot de "
                                   "passe » d'un compte autorisé.")
    form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('/accounts/login/')


@login_required
def register_user(request):
    if request.method == 'POST':
        form = UserCreate(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'utilisateur a été créer avec succéss")
            return redirect('/admin/')
        else:
            messages.error(request, "Une erreur s'est produite, veuillez bien vérifier vos coordonnées !")
    form = UserCreate()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def user_update(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        form = UserUpdate(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "L'utilisateur a été modifier avec succéss")
            return redirect('/admin/')
        else:
            messages.error(request, "Une erreur s'est produite, veuillez bien vérifier vos coordonnées !")
    user = User.objects.get(username=username)
    form = UserUpdate(instance=user)
    context = {'form': form}
    return redirect('/accounts/admin_user/')


@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Votre mot de passe a été modifié avec succéss")
        else:
            messages.error(request, "Erreur s'est produite lors de la modification de votre mot de passe, veuillez "
                                    "bien vérifier !")

    form = PasswordChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'accounts/password-change.html', context)


@login_required
def list_user(request):
    user = User.objects.all()
    context = {'user': user}
    return render(request, 'user/list-user.html', context)


@login_required
def delete_user(request, username):
    user = User.objects.get(username=username)
    suppression = user.delete()
    if suppression is not None:
        messages.success(request, "L'utilisateurs a été supprimé avec succéss")
    else:
        messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
    return redirect('/accounts/admin_user/')

