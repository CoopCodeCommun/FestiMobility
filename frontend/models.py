import uuid
from django.db import models

class Evenement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    datetime = models.DateTimeField()
    lieu = models.CharField(max_length=120)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.nom} ({self.lieu})"

class Conducteur(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=80)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    ville_depart = models.CharField(max_length=120)
    latitude_depart = models.FloatField()
    longitude_depart = models.FloatField()
    nb_places = models.PositiveSmallIntegerField(default=3)
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='conducteurs')
    heure_depart = models.TimeField()

    def __str__(self):
        return f"{self.nom} ({self.ville_depart} → {self.evenement.nom})"

class Passager(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=80)
    email = models.EmailField()
    ville_depart = models.CharField(max_length=120)
    latitude_depart = models.FloatField()
    longitude_depart = models.FloatField()
    evenement = models.ForeignKey(Evenement, on_delete=models.CASCADE, related_name='passagers')
    heure_souhaitee = models.TimeField()

    def __str__(self):
        return f"{self.nom} ({self.ville_depart} → {self.evenement.nom})"
