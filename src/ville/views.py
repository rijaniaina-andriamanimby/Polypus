from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import VilleModel
from .forms import VilleForm

message_erreur = "Une erreur s'est produite, veuillez réessayer !"


@login_required
# Create your views here.
def index_ville(request):
    ville_data = VilleModel.objects.all().order_by("codePostal")
    if request.method == 'POST':
        recherche = request.POST.get('rechercheVille')
        if recherche is not None:
            ville_data = VilleModel.objects.all().filter(nomVille__icontains=recherche)

    paginator_ville = Paginator(ville_data, 3)
    paginator_ville_number = request.GET.get('page', 1)
    ville = paginator_ville.get_page(paginator_ville_number)
    context = {'ville': ville}
    return render(request, 'ville/ville.html', context)


@login_required
def add_ville(request):
    if request.method == 'GET':
        form = VilleForm()
        return render(request, 'ville/form-ville.html', {'form': form})
    else:
        form = VilleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le nouvel élément a été ajouté avec succès")
            return redirect('/Ville/')
        else:
            messages.error(request, message=message_erreur)
            form = VilleForm()
            return render(request, 'ville/form-ville.html', {'form': form})


@login_required
def update_ville(request, codePostal):
    if request.method == 'GET':
        ville = VilleModel.objects.get(pk=codePostal)
        form = VilleForm(instance=ville)
        return render(request, 'ville/form-ville.html', {'form': form})
    else:
        ville = VilleModel.objects.get(pk=codePostal)
        form = VilleForm(request.POST, request.FILES, instance=ville)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont été appliqués avec soin et succès.")
            return redirect('/Ville/')
        else:
            form = VilleForm(instance=ville)
            return render(request, 'ville/form-ville.html', {'form': form})


@login_required
def delete_ville(request, codePostal):
    ville = VilleModel.objects.get(pk=codePostal)
    suppression = ville.delete()
    if suppression is not None:
        messages.success(request, "L'élément a été supprimé avec succès")
    else:
        messages.error(request, message=message_erreur)
    return redirect('/Ville/')
