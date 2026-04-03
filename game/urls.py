from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('rooms/', views.rooms, name='rooms'),
    path('rooms/<int:room_id>/join/', views.join_room, name='join_room'),
    path('game/<uuid:session_id>/', views.game, name='game'),
    path('game/<uuid:session_id>/question/', views.get_question, name='get_question'),
    path('game/<uuid:session_id>/complete/', views.game_complete, name='game_complete'),
]
