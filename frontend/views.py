from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .models import Evenement, Conducteur
from .mapbox_utils import match_passenger_mapbox

from django.shortcuts import get_object_or_404

def home(request, event_id=None):
    evenements = Evenement.objects.all()
    event_names = Evenement.objects.values_list('nom', flat=True).distinct()
    event_courant = None
    if event_id:
        event_courant = get_object_or_404(Evenement, id=event_id)
        conducteurs = Conducteur.objects.filter(evenement=event_courant)
    else:
        event_id_query = request.GET.get('event_id')
        if event_id_query:
            event_courant = get_object_or_404(Evenement, id=event_id_query)
            conducteurs = Conducteur.objects.filter(evenement=event_courant)
        else:
            conducteurs = Conducteur.objects.all()
    return render(request, 'frontend/home.html', {
        'evenements': evenements,
        'conducteurs': conducteurs,
        'event_names': event_names,
        'event_courant': event_courant,
    })

def event_detail(request, event_id):
    return home(request, event_id=event_id)


def proposer_trajet(request):
    if request.method == 'POST':
        # Création du conducteur
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        telephone = request.POST.get('telephone', '')
        ville_depart = request.POST.get('ville_depart')
        latitude_depart = request.POST.get('latitude_depart')
        longitude_depart = request.POST.get('longitude_depart')
        nb_places = request.POST.get('nb_places')
        evenement_id = request.POST.get('evenement')
        heure_depart = request.POST.get('heure_depart')
        evenement = get_object_or_404(Evenement, id=evenement_id)
        conducteur = Conducteur.objects.create(
            nom=nom,
            email=email,
            telephone=telephone,
            ville_depart=ville_depart,
            latitude_depart=latitude_depart,
            longitude_depart=longitude_depart,
            nb_places=nb_places,
            evenement=evenement,
            heure_depart=heure_depart
        )
        # Après succès, recharge la page via JS côté client
        return HttpResponse('<div class="alert alert-success">Trajet proposé avec succès !<script>setTimeout(function(){ window.location.reload(); }, 700);</script></div>')
    else:
        # GET: afficher le formulaire, prérempli avec coordonnées
        lat = request.GET.get('lat', '')
        lng = request.GET.get('lng', '')
        evenements = Evenement.objects.all()
        event_id = request.GET.get('event_id')
        heure_depart_default = ''
        if event_id:
            try:
                event = Evenement.objects.get(id=event_id)
                # Si l'événement a un datetime, propose 2h avant
                if hasattr(event, 'datetime') and event.datetime:
                    from datetime import timedelta
                    heure_depart = (event.datetime - timedelta(hours=2)).time()
                    heure_depart_default = heure_depart.strftime('%H:%M')
            except Exception:
                pass
        return render(request, 'frontend/conducteur_form.html', {
            'latitude_depart': lat,
            'longitude_depart': lng,
            'evenements': evenements,
            'event_id': event_id,
            'heure_depart_default': heure_depart_default
        })
