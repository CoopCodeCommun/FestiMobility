from rest_framework import serializers
from .models import Conducteur

class ConducteurSerializer(serializers.ModelSerializer):
    evenement_nom = serializers.CharField(source='evenement.nom', read_only=True)
    class Meta:
        model = Conducteur
        fields = ['id', 'nom', 'email', 'telephone', 'ville_depart', 'latitude_depart', 'longitude_depart', 'nb_places', 'evenement', 'evenement_nom', 'heure_depart']
