from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Resider
from .forms import ResiderForm


@login_required
# Create your views here.
def index_residence(request):
    resider_data = Resider.objects.all().order_by("id")
    if request.method == 'POST':
        recherche = request.POST.get('rechercheVille')
        if recherche is not None:
            resider_data = Resider.objects.all().filter(villeVilla__nomVille__icontains=recherche)

    paginator_resider = Paginator(resider_data, 5)
    paginator_resider_number = request.GET.get('page', 1)
    resider = paginator_resider.get_page(paginator_resider_number)
    context = {'resider': resider}
    return render(request, 'residence/residence.html', context)


@login_required
def add_residence(request):
    if request.method == 'GET':
        form = ResiderForm()
        return render(request, 'residence/form-residence.html', {'form':form})
    else:
        form = ResiderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Le nouvel élément a été ajouté avec succès")
            return redirect('/residence/')
        else:
            messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
            form = ResiderForm()
            return render(request, 'residence/form-residence.html', {'form': form})


@login_required
def update_residence(request, id):
    if request.method == 'GET':
        ville = Resider.objects.get(pk=id)
        form = ResiderForm(instance=ville)
        return render(request, 'residence/form-residence.html', {'form': form})
    else:
        ville = Resider.objects.get(pk=id)
        form = ResiderForm(request.POST, instance=ville)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont été appliqués avec soin et succès.")
            return redirect('/residence/')
        else:
            messages.error(request, "une erreur s'est produite, veuillez réessayer !")
            form = ResiderForm(instance=ville)
            return render(request, 'residence/form-residence.html', {'form': form})



@login_required
def delete_residence(request, id):
    ville = Resider.objects.get(pk=id)
    suppression = ville.delete()
    if suppression is not None:
        messages.success(request, "L'élément a été supprimé avec succès")
    else:
        messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
    return redirect('/residence/')


