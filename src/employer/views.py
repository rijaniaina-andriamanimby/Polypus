from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .forms import *
from .models import EmployerModel


@login_required
# Views for Employer
def index(request):
    employer_data = EmployerModel.objects.order_by('matriculeEmployer')
    if request.method == 'POST':
        recherche = request.POST.get('rechercheEmployer')
        if recherche is not None:
            employer_data = EmployerModel.objects.all().filter(nomPrenomsEmployer__icontains=recherche).order_by(
                'matriculeEmployer')

    # Nombre par page .....
    p_employer = Paginator(employer_data, 5)
    # Recuperation du page 1
    p_number = request.GET.get('page', 1)
    p_obj = p_employer.get_page(p_number)
    context = {'employer': p_obj}
    return render(request, 'employer/employer.html', context)


@login_required
def employer_formulaire(request):
    if request.method == 'GET':
        form = EmployerForm()
        return render(request, 'employer/formEmployer.html', {'form': form})
    else:
        form = EmployerForm(request.POST)
        try:
            form.is_valid()
            form.save()
            messages.success(request, "Le nouvel élément a été ajouté avec succès")
            return redirect('/employer/')
        except Exception as e:
            messages.error(request, "Le nouvel élément n'a pas été ajouté avec succès")
            form = EmployerForm()
            return render(request, "employer/formEmployer.html", {'form': form})
        # if form.is_valid():
        #     form.save()
        #     messages.success(request, "Le nouvel élément a été ajouté avec succès")
        # else:
        #     messages.error(request, "Le nouvel élément n'a pas été ajouté avec succès")
        # return redirect('/employer/')


@login_required
def update_employer(request, matriculeEmployer):
    if request.method == 'GET':
        employer = EmployerModel.objects.get(pk=str(matriculeEmployer))
        form = EmployerForm(instance=employer)
        return render(request, 'employer/formEmployer.html', {'form': form})
    else:
        employer = EmployerModel.objects.get(pk=matriculeEmployer)
        form = EmployerForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            messages.success(request, "Les changements ont été appliqués avec soin et succès.")
            return redirect('/employer/')
        else:
            messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
            form = EmployerForm(instance=employer)
            return render(request, 'client/form-client.html', {'form': form})


@login_required
def delete_employer(request, matriculeEmployer):
    employer = EmployerModel.objects.get(pk=matriculeEmployer)
    suppression = employer.delete()
    if suppression is not None:
        messages.success(request, "L'élément a été supprimé avec succès")
    else:
        messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
    return redirect('/employer/')
