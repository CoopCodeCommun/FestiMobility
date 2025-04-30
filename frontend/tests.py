import uuid
from django.test import TestCase
from django.urls import reverse
from .models import Evenement, Conducteur

class EvenementModelTest(TestCase):
    def test_create_evenement(self):
        e = Evenement.objects.create(
            id=uuid.uuid4(),
            nom="Test Event",
            description="Desc",
            datetime="2025-01-01T18:00:00",
            lieu="Montpellier",
            latitude=43.6111,
            longitude=3.8767
        )
        self.assertEqual(str(e), "Test Event (Montpellier)")

class ConducteurModelTest(TestCase):
    def setUp(self):
        self.evenement = Evenement.objects.create(
            id=uuid.uuid4(),
            nom="Jazz",
            description="Jazz fest",
            datetime="2025-01-01T18:00:00",
            lieu="Sète",
            latitude=43.4,
            longitude=3.7
        )
    def test_create_conducteur(self):
        c = Conducteur.objects.create(
            id=uuid.uuid4(),
            nom="Alice",
            email="alice@example.com",
            ville_depart="Agde",
            latitude_depart=43.3,
            longitude_depart=3.5,
            nb_places=3,
            evenement=self.evenement,
            heure_depart="14:00"
        )
        self.assertEqual(str(c), f"Alice (Agde → {self.evenement.nom})")
        self.assertEqual(c.evenement.nom, "Jazz")

class HomeViewTest(TestCase):
    def test_home_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_only_event_markers_and_no_trajet_form(self):
        evenement = Evenement.objects.create(
            id=uuid.uuid4(),
            nom="Test Event",
            description="Desc",
            datetime="2025-12-10T19:00:00",
            lieu="Montpellier",
            latitude=43.6111,
            longitude=3.8767
        )
        response = self.client.get(reverse('home'))
        content = response.content.decode()
        # Le JS doit contenir le marqueur d'événement avec le bon ID et le lien
        self.assertIn(f'id: "{evenement.id}"', content)
        # Le lien doit être présent dans le JS généré (popup Leaflet)
        self.assertIn(f'/event/{evenement.id}/', content)
        # Pas de bouton de proposition de trajet sur la page d'accueil
        self.assertNotIn('btn-proposer-trajet', content)
        # Pas de JS qui branche map.on("click") sans event_courant
        self.assertNotIn('map.on', content.split('if event_courant')[0])

    def test_event_and_driver_markers_visible(self):
        # Création d'un événement et d'un conducteur
        import uuid
        evenement = Evenement.objects.create(
            id=uuid.uuid4(),
            nom="Test Event",
            description="Desc",
            datetime="2025-01-01T18:00:00",
            lieu="Montpellier",
            latitude=43.6111,
            longitude=3.8767
        )
        conducteur = Conducteur.objects.create(
            id=uuid.uuid4(),
            nom="Alice",
            email="alice@example.com",
            ville_depart="Agde",
            latitude_depart=43.3108,
            longitude_depart=3.4758,
            nb_places=3,
            evenement=evenement,
            heure_depart="14:30"
        )
        # Page d'accueil : le conducteur NE doit PAS apparaître
        response = self.client.get(reverse('home'))
        content = response.content.decode()
        self.assertNotIn('lat: 43.3108', content)
        self.assertNotIn('lng: 3.4758', content)
        # Page événement : le conducteur DOIT apparaître
        response = self.client.get(reverse('event-detail', args=[evenement.id]))
        content = response.content.decode()
        self.assertIn('lat: 43.3108', content)
        self.assertIn('lng: 3.4758', content)

    def test_conducteur_form_get_and_post(self):
        import uuid
        evenement = Evenement.objects.create(
            id=uuid.uuid4(),
            nom="Test Event",
            description="Desc",
            datetime="2025-01-01T18:00:00",
            lieu="Montpellier",
            latitude=43.6111,
            longitude=3.8767
        )
        # GET: formulaire avec coordonnées préremplies
        response = self.client.get(reverse('proposer-trajet') + '?lat=43.123456&lng=3.654321')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('value="43.123456"', content)
        self.assertIn('value="3.654321"', content)
        self.assertIn('name="nom"', content)
        # POST: création conducteur
        data = {
            'nom': 'Bob',
            'email': 'bob@example.com',
            'telephone': '0600000000',
            'ville_depart': 'Béziers',
            'latitude_depart': '43.123456',
            'longitude_depart': '3.654321',
            'nb_places': 2,
            'evenement': str(evenement.id),
            'heure_depart': '15:00',
        }
        response = self.client.post(reverse('proposer-trajet'), data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Trajet proposé avec succès', response.content.decode())
        self.assertTrue(Conducteur.objects.filter(nom='Bob', email='bob@example.com').exists())
