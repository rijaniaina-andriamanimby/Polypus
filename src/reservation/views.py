from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.templatetags.static import static
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from .models import ReservationModel
from .forms import ReservationForm


@login_required
# Create your views here.
def index_reservation(request):
    reservation_data = ReservationModel.objects.all()
    if request.method == "POST":
        recherche = request.POST.get('rechercheReservation')
        if recherche is not None:
            reservation_data = ReservationModel.objects.all().filter(
                clientReserver__nomCompletClient__icontains=recherche)

    paginator_reservation = Paginator(reservation_data, 5)
    paginator_reservation_number = request.GET.get('page', 1)
    reservation = paginator_reservation.get_page(paginator_reservation_number)
    context = {'reservation': reservation}
    return render(request, 'reservations/reservation.html', context)


@login_required
def add_update_reservation(request, id=0):
    if request.method == 'GET':
        if id == 0:
            form = ReservationForm()
            return render(request, 'reservations/form-reservation.html', {'form': form})
        else:
            reservation = ReservationModel.objects.get(pk=id)
            form = ReservationForm(instance=reservation)
            return render(request, 'reservations/form-reservation.html', {'form': form})
    else:
        if id == 0:
            form = ReservationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Le nouvel élément a été ajouté avec succès")
                return redirect('/reservation/')
            else:
                messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
                form = ReservationForm()
                return render(request, 'reservations/form-reservation.html', {'form': form})
        else:
            reservation = ReservationModel.objects.get(pk=id)
            form = ReservationForm(request.POST, instance=reservation)
            if form.is_valid():
                form.save()
                messages.success(request, "Les changements ont été appliqués avec soin et succès.")
                return redirect('/reservation/')
            else:
                messages.error(request, "Une erreur s'est produite, veuillez réessayer !")
                reservation = ReservationModel.objects.get(pk=id)
                form = ReservationForm(instance=reservation)
                return render(request, 'reservations/form-reservation.html', {'form': form})


@login_required
def delete_reservation(request, id):
    reservation = ReservationModel.objects.get(pk=id)
    suppression = reservation.delete()
    if suppression is not None:
        messages.success(request, "L'élément a été supprimé avec succès")
    else:
        messages.error(request, "Une erreur s'est produite, veuillez réessayer")
    return redirect('/reservation/')


def rapport(request):
    # Créer la réponse HTTP avec le type de contenu PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reservation_report.pdf"'

    # Créer le document PDF avec SimpleDocTemplate
    pdf = SimpleDocTemplate(response, pagesize=A4)

    # Créer une liste pour stocker les éléments du document
    elements = []

    # Définir le chemin du logo en utilisant la fonction static()
    logo_path = finders.find('accounts/logo-polypus.png')
    logo = Image(logo_path, width=3 * inch, height=1 * inch)  # Ajustez la taille selon les besoins
    elements.append(logo)

    # Définir le style pour le titre
    styles = getSampleStyleSheet()
    title = Paragraph("Rapport de Réservations", styles['Title'])
    elements.append(title)

    # Ajouter un espace entre le titre et le tableau
    elements.append(Paragraph("<br/><br/>", styles['Normal']))

    # Définir les en-têtes de colonnes pour le tableau
    data = [
        ["Villa", "Client", "Lotissement", "Date de Réservation", "Accompte"]
    ]

    # Récupérer les données des réservations et les ajouter dans le tableau
    reservations = ReservationModel.objects.all()
    for reservation in reservations:
        data.append([
            str(reservation.villaReserver),
            str(reservation.clientReserver),
            str(reservation.lotReserver),
            reservation.dateReservation.strftime('%d-%m-%Y'),  # Formatage de la date
            "Oui" if reservation.accompte else "Non"
        ])

    # Créer le tableau avec les données
    table = Table(data, colWidths=[1.5 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch, 1 * inch])

    # Appliquer un style au tableau
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Ajouter le tableau aux éléments du document
    elements.append(table)

    # Générer le PDF
    pdf.build(elements)

    return response
