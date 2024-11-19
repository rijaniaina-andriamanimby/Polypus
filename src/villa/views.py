from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import VillaModel, ImageModel
from .forms import VillaForm, ImageForm


@login_required
# Create your views here.
def index_villa(request):
    villa_data = VillaModel.objects.all().order_by("lotVilla")
    if request.method == 'POST':
        recherche = request.POST.get('rechercheVilla')
        if recherche is not None:
            villa_data = VillaModel.objects.all().filter(nomVilla__icontains=recherche)

    paginator_villa = Paginator(villa_data, 2)
    paginator_villa_number = request.GET.get('page', 1)
    villa = paginator_villa.get_page(paginator_villa_number)
    context = {'villa': villa}
    return render(request, 'villa/villa.html', context)


@login_required
def add_villa(request):
    if request.method == 'GET':
        form = VillaForm()
        return render(request, 'villa/form-villa.html', {'form': form})
    else:
        form = VillaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le nouvel élément a été ajouté avec succès")
            return redirect('/Model-villa/')
        else:
            messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
            form = VillaForm()
            return render(request, 'villa/form-villa.html', {'form': form})


def update_villa(request, lotVilla):
    if request.method == 'GET':
        villa = VillaModel.objects.get(pk=lotVilla)
        form = VillaForm(instance=villa)
        return render(request, 'villa/form-villa.html', {'form': form})
    else:
        villa = VillaModel.objects.get(pk=lotVilla)
        form = VillaForm(request.POST, request.FILES, instance=villa)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont été appliqués avec soin et succès.")
            return redirect('/Model-villa/')
        else:
            messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
            form = VillaForm(instance=villa)
            return render(request, 'villa/form-villa.html', {'form': form})


def delete_villa(request, lotVilla):
    villa = VillaModel.objects.get(pk=lotVilla)
    suppression = villa.delete()
    if suppression is not None:
        messages.success(request, "L'élément a été supprimé avec succès")
    else:
        messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
    return redirect('/Model-villa/')


# views pour les images

@login_required
# Create your views here.
def index_image(request):
    image_data = ImageModel.objects.all().order_by("id")
    paginator_image = Paginator(image_data, 3)
    paginator_image_number = request.GET.get('page', 1)
    image = paginator_image.get_page(paginator_image_number)
    context = {'image': image}
    return render(request, 'image_villa/image_villa.html', context)


@login_required
def add_image(request):
    if request.method == 'GET':
        form = ImageForm()
        return render(request, 'image_villa/form-image-villa.html', {'form': form})
    else:
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Le nouvel élément a été ajouté avec succès")
            return redirect('/Model-villa/image_villa/')
        else:
            messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
            form = ImageForm()
            return render(request, 'image_villa/form-image-villa.html', {'form': form})


def update_image(request, id):
    if request.method == 'GET':
        image = ImageModel.objects.get(pk=id)
        form = ImageForm(instance=image)
        return render(request, 'image_villa/form-image-villa.html', {'form': form})
    else:
        image = ImageModel.objects.get(pk=id)
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont été appliqués avec soin et succès.")
            return redirect('/Model-villa/image_villa/')
        else:
            messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
            form = ImageForm(instance=image)
            return render(request, 'image_villa/form-image-villa.html', {'form': form})


def delete_image(request, id):
    villa = ImageModel.objects.get(pk=id)
    suppression = villa.delete()
    if suppression is not None:
        messages.success(request, "Elément a été supprimé avec succès")
    else:
        messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
    return redirect('/Model-villa/image_villa/')
