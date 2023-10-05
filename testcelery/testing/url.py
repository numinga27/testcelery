from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (EventDetails, EventIdViewSet,
                    TournamentViewSet, HockeyView, EndedMatchView,
                    ScheduledView, AllView,AllHockeyView,ScheduledHockeyView,EndedHockeyView
                    )


router = DefaultRouter()

# router.register('live-events', LiveOfEventsViewSet)
router.register(r'event-ids', EventIdViewSet)
# router.register(r'tournaments', TournamentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/live/football/', TournamentViewSet.as_view({'get': 'list'})),
    path('api/events/live/', EventIdViewSet.as_view({'get': 'list'})),
    path('live-events/event-details/<str:live_event_id>/',
         EventDetails.as_view(), name='event-details'),
    path('api/live/hockey/', HockeyView.as_view({'get': 'list'})),
    path('api/ended/', EndedMatchView.as_view({'get': 'list'})),
    path('api/scheduled/', ScheduledView.as_view({'get': 'list'})),
    path('api/all/', AllView.as_view({'get': 'list'})),
    path('api/all_hockey/', AllHockeyView.as_view({'get': 'list'})),
    path('api/scheduled_hockey/', ScheduledHockeyView.as_view({'get': 'list'})),
    path('api/ended_hockey/', EndedHockeyView.as_view({'get': 'list'})),
]
