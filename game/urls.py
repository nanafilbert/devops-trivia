from django.urls import path
from django.http import JsonResponse
from . import views

def health(request):
    return JsonResponse({"status": "ok"})

def ready(request):
    return JsonResponse({"status": "ready"})

urlpatterns = [
    path('', views.landing, name='landing'),
    path('health/', health, name='health'),                              # ← liveness probe
    path('ready/', ready, name='ready'),                                 # ← readiness probe
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:room_id>/join/', views.join_room, name='join_room'),
    path('game/<uuid:session_id>/', views.game, name='game'),
    path('game/<uuid:session_id>/question/', views.get_question, name='get_question'),
    path('game/<uuid:session_id>/complete/', views.game_complete, name='game_complete'),
]
