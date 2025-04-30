from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.template.loader import render_to_string
from django.http import HttpResponse
from .models import Conducteur, Evenement
from .serializers import ConducteurSerializer
from django.utils import timezone

class ConducteurViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Conducteur.objects.all()
    serializer_class = ConducteurSerializer

    @action(detail=False, methods=['get'], url_path='partial')
    def partial(self, request):
        event = request.GET.get('event')
        date = request.GET.get('date')
        qs = self.queryset
        if event:
            qs = qs.filter(evenement__nom=event)
        if date:
            qs = qs.filter(evenement__date=date)
        html = render_to_string('frontend/_conducteur_markers.html', {'conducteurs': qs})
        return HttpResponse(html)
