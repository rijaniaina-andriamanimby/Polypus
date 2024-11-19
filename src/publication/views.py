from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from villa.models import VillaModel, ImageModel
from ville.models import VilleModel
from resider.models import Resider
from villaUnique.models import VillaUnique
from visitor.models import Visitor
from django.utils.timezone import now


def get_client_ip(request):
    # Vérifie d'abord si l'adresse IP est dans les en-têtes HTTP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # Si plusieurs IPs sont renvoyées, on prend la première (côté client)
        ip = x_forwarded_for.split(',')[0]
    else:
        # Sinon, on récupère l'IP à partir de la connexion directe
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_visitor(request):
    ip = get_client_ip(request)  # Créez une fonction pour récupérer l'IP
    Visitor.objects.create(ip_address=ip, visit_time=now())


# Create your views here.
def acceuil_publication(request):
    log_visitor(request)
    adresse = VilleModel.objects.all()
    villa_all = VillaModel.objects.all()
    ville = VilleModel.objects.all()
    context = {'adresse': adresse, 'villaAll': villa_all, 'ville': ville}
    return render(request, "acceuil/index.html", context)


def a_propos(request):
    log_visitor(request)
    adresse = VilleModel.objects.all()
    context = {'adresse': adresse}
    return render(request, 'apropos/about.html', context=context)


def projet_detail(request, nomVille):
    log_visitor(request)
    adresse = VilleModel.objects.all()
    titre = [{'location': nomVille}]
    ville = VilleModel.objects.filter(nomVille=nomVille)
    villa = VillaModel.objects.filter(
        lotVilla__in=Resider.objects.filter(villeVilla__nomVille=nomVille).values_list('villaModel__lotVilla',
                                                                                       flat=True)
    )
    unique = VillaUnique.objects.all()
    villa_all = VillaModel.objects.all()
    img = ImageModel.objects.all()
    context = {
        'villa': villa, 'titre': titre,
        'villaAll': villa_all, 'adresse': adresse,
        'ville': ville, 'image': img, 'unique': unique
    }
    return render(request, 'residence/project-details.html', context=context)


def technologies(request):
    log_visitor(request)
    adresse = VilleModel.objects.all()
    context = {'adresse': adresse}
    return render(request, 'technologie/technologie.html', context)


def contact(request):
    log_visitor(request)
    adresse = VilleModel.objects.all()
    context = {'adresse': adresse}
    if request.method == 'POST':
        subject = "Formulaire de contact"
        nom_client = request.POST.get('name')
        phone = request.POST.get('number')
        email_client = request.POST.get('email')
        message_client = request.POST.get('message')
        if not subject or not nom_client or not phone or not email_client or not message_client:
            messages.error(request, 'Tous les champs sont obligatoires.')
            return redirect('/publication/contact/#formulaire')
        else:
            message = f"""
            Bonjour,
    
            Le client {nom_client} souhaite vous envoyer un message : {message_client} 
            Ses coordonnées sont les suivantes :
            - Téléphone : {phone}
            - Email : {email_client}
            Merci de bien vouloir traiter cette demande.
            Cordialement,
            L'équipe de Polypus Corporation S.A.
            """
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = ["voyondrozelmar@gmail.com"]  # Correct the email here
            try:
                # Envoi de l'email
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request, "Votre message a bien été envoyé. Nous vous contacterons dans les plus brefs "
                                          "délais !")
                # Réponse de succès
                return redirect('/publication/contact/#formulaire')
            except Exception as e:
                # Si une erreur se produit lors de l'envoi de l'email
                return messages.error(request, "Une erreur est survenue lors de l'envoi de votre message. Veuillez "
                                               "réessayer ultérieurement.")
    return render(request, 'contact/contact.html', context)


def reservation(request):
    log_visitor(request)
    if request.method == 'POST':
        subject = "Réservation de villa"
        nom_client = request.POST.get('name')
        phone = request.POST.get('number')
        email_client = request.POST.get('email')
        id_villa_reserver = request.POST.get('villaReserver')
        id_residence = request.POST.get('residence')
        lotVilla = request.POST.get('lotVilla')

        if not nom_client or not phone or not email_client or not id_villa_reserver or not id_residence or not lotVilla:
            messages.error(request, 'Tous les champs sont obligatoires.')
            previous_url = request.META.get('HTTP_REFERER', '/#reservations')
            return HttpResponseRedirect(previous_url)
        else:
            villa_reserver = VillaModel.objects.get(lotVilla=request.POST.get('villaReserver'))
            residence = VilleModel.objects.get(codePostal=request.POST.get('residence'))
            message = f"""
            Bonjour,
            Le client {nom_client} souhaite réserver la villa: {villa_reserver.nomVilla} qui se situe à {residence.nomVille} avec le lotissement {lotVilla}. 
            Ses coordonnées sont les suivantes :
            - Téléphone : {phone}
            - Email : {email_client}
            Merci de bien vouloir traiter cette demande.
            Cordialement,
            L'équipe de Polypus Corporation S.A.
            """

            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = ["voyondrozelmar@gmail.com"]  # Remplace par l'adresse email correcte
            try:
                # Envoi de l'email
                send_mail(subject, message, from_email, recipient_list)
                # Réponse de succès
                messages.success(request, "Votre réservation a bien été envoyé. Nous vous contacterons dans "
                                          "les plus brefs"
                                          "délais !")
                previous_url = request.META.get('HTTP_REFERER', '/')
                return HttpResponseRedirect(previous_url)
            except Exception as e:
                # Si une erreur se produit lors de l'envoi de l'email
                messages.error(request, "Une erreur est survenue lors de l'envoi de votre message. Veuillez "
                                        "réessayer ultérieurement.")
                previous_url = request.META.get('HTTP_REFERER', '/')
                return HttpResponseRedirect(previous_url)


def get_lots(request):
    log_visitor(request)
    villa_id = request.GET.get('villa_id')  # Récupérer l'ID de la villa sélectionnée

    if villa_id:
        # Filtrer les lots pour la villa sélectionnée
        lots = VillaUnique.objects.filter(
            modelVilla__lotVilla=villa_id)  # Vérifiez que 'nomVilla' est bien le champ à filtrer
        lot_data = [{'lotVilla': lot.lotVilla} for lot in lots]
        return JsonResponse({'lots': lot_data})
    else:
        return JsonResponse({'lots': []})


def get_villa_model(request):
    log_visitor(request)
    codePostal = request.GET.get('codePostal')  # Récupérer l'ID de la villa sélectionnée

    if codePostal:
        # Filtrer les lots pour la villa sélectionnée
        villa = VillaModel.objects.filter(
            lotVilla__in=Resider.objects.filter(villeVilla__codePostal=codePostal).values_list('villaModel__lotVilla',
                                                                                               flat=True)
        )  # Vérifiez que 'nomVilla' est bien le champ à filtrer
        villa_data = [{'lotVilla': villas.lotVilla, 'nomVilla': villas.nomVilla} for villas in villa]
        return JsonResponse({'villa': villa_data})
    else:
        return JsonResponse({'villa': []})
