from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import VillaUnique
from .forms import VillaFormU

messages_erreur = "Une erreur s'est produite, veuillez réessayer !"


@login_required
# Create your views here.
def index_villa_u(request):
    villa_data = VillaUnique.objects.all().order_by("lotVilla")
    if request.method == 'POST':
        recherche = request.POST.get('rechercheVilla')
        if recherche is not None:
            villa_data = VillaUnique.objects.all().filter(modelVilla__nomVilla__icontains=recherche)

    paginator_villa = Paginator(villa_data, 5)
    paginator_villa_number = request.GET.get('page',5)
    villa = paginator_villa.get_page(paginator_villa_number)

    context = {'villa': villa}
    return render(request, 'villaUnique/villa-unique.html', context)


@login_required
def add_villa_u(request):
    if request.method == 'GET':
        form = VillaFormU()
        return render(request, 'villaUnique/form-villa-unique.html', {'form': form})
    else:
        form = VillaFormU(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le nouvel élément a été ajouté avec succès")
            return redirect('/villa/')
        else:
            messages.error(request, message=messages_erreur)
            form = VillaFormU()
            return render(request, 'villaUnique/form-villa-unique.html', {'form': form})


@login_required
def update_villa_u(request, lotVilla):
    if request.method == 'GET':
        villa = VillaUnique.objects.get(pk=lotVilla)
        form = VillaFormU(instance=villa)
        return render(request, 'villaUnique/form-villa-unique.html', {'form': form})
    else:
        villa = VillaUnique.objects.get(pk=lotVilla)
        form = VillaFormU(request.POST, instance=villa)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont été appliqués avec soin et succès.")
            return redirect('/villa/')
        else:
            messages.error(request, message=messages_erreur)
            form = VillaFormU(instance=villa)
            return render(request, 'villaUnique/form-villa-unique.html', {'form': form})


@login_required
def delete_villa_u(request, lotVilla):
    villa = VillaUnique.objects.get(pk=lotVilla)
    suppression = villa.delete()
    if suppression is not None:
        messages.success(request, "L'élément a été supprimé avec succès")
    else:
        messages.error(request, message=messages_erreur)
    return redirect('/villa/')
