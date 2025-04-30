from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views_partial import ConducteurViewSet

router = DefaultRouter()
router.register(r'conducteurs', ConducteurViewSet, basename='conducteur')

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<uuid:event_id>/', views.event_detail, name='event-detail'),
    path('proposer-trajet/', views.proposer_trajet, name='proposer-trajet'),
    path('api/', include(router.urls)),
    path('conducteurs-partial/', ConducteurViewSet.as_view({'get': 'partial'}), name='conducteurs-partial'),
]

