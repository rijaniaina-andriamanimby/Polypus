from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, redirect
from .models import ClientModel
from .forms import ClientForm, ClientRechercheForm
from reservation.models import ReservationModel
from visitor.models import Visitor


# List des clients
@login_required
def index_client(request):
    total_visits = Visitor.objects.count()
    unique_visits = Visitor.objects.values('ip_address').distinct().count()
    reservation = ReservationModel.objects.count()
    client = ClientModel.objects.count()
    # Obtenir le nombre de visites par jour
    daily_visits = (
        Visitor.objects
        .extra(select={'day': "DATE(visit_time)"})
        .values('day')
        .annotate(visits=Count('id'))
        .order_by('day')
    )

    # Extraire les données pour le graphique
    dates = [entry['day'].strftime("%Y-%m-%d") for entry in daily_visits]
    visits_counts = [entry['visits'] for entry in daily_visits]

    context = {
        'visit': total_visits,
        'unique_visit': unique_visits,
        'dates': dates,
        'visits_counts': total_visits,
        'reservation_count': reservation,
        'client_count': client
    }
    return render(request, 'index.html', context)


@login_required
def list_client(request):
    client_data = ClientModel.objects.all()
    if request.method == 'POST':
        recherche = request.POST.get('rechercheClient')
        if recherche is not None:
            client_data = ClientModel.objects.all().filter(nomCompletClient__icontains=recherche)

    paginator_client = Paginator(client_data, 5)
    page_number_client = request.GET.get('page', 1)
    client = paginator_client.get_page(page_number_client)
    context = {'client': client}
    return render(request, 'client/client.html', context)


@login_required
# Ajout d'un client
def add_client(request):
    if request.method == 'GET':
        form = ClientForm()
        return render(request, 'client/form-client.html', {'form': form})
    else:
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "L'ajout d'un nouveau client est éfféctuer avec succés !")
            return redirect('/client/')
        else:
            messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
            form = ClientForm()
            return render(request, 'client/form-client.html', {'form': form})


@login_required
# Modification d'un client
def update_client(request, telephoneClient):
    if request.method == 'GET':
        client = ClientModel.objects.get(pk=telephoneClient)
        form = ClientForm(instance=client)
        return render(request, 'client/form-client.html', {'form': form})
    else:
        client = ClientModel.objects.get(pk=telephoneClient)
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Modification éfféctuer")
            return redirect('/client/')
        else:
            messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
            client = ClientModel.objects.get(pk=telephoneClient)
            form = ClientForm(instance=client)
            return render(request, 'client/form-client.html', {'form': form})


@login_required
# Suppression de client
def delete_client(request, telephoneClient):
    client = ClientModel.objects.get(pk=telephoneClient)
    suppression = client.delete()
    if suppression is not None:
        messages.success(request, "Suppréssion éfféctuer")
    else:
        messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
    return redirect('/client/')


@login_required
# Recherche de client
def recherche_client(request):
    if request.method == 'GET':
        form_recherche = ClientRechercheForm()
        return render(request, 'client/recherche-client.html', {'form': form_recherche})
    else:
        form_recherche = ClientRechercheForm(request.POST)
        if form_recherche.is_valid():
            search_term = form_recherche.cleaned_data['search_field']
            clients = ClientModel.objects.filter(nomCompletClient__icontains=search_term)
            return render(request, 'client/recherche-client.html', {'form': form_recherche, 'clients': clients})


def client_reserver(request):
    client_data = ClientModel.objects.filter(
        telephoneClient__in=ReservationModel.objects.all().values_list('clientReserver__telephoneClient', flat=True)
    )
    paginator_client = Paginator(client_data, 5)
    page_number_client = request.GET.get('page', 1)
    client = paginator_client.get_page(page_number_client)
    return render(request, 'client/client.html', {'client': client})
