from django.contrib import admin
from .models import Room, Question, GameSession, SessionAnswer


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['room', 'difficulty', 'text']
    list_filter = ['room', 'difficulty']
    search_fields = ['text']


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ['username', 'room', 'difficulty', 'score', 'total_questions', 'completed', 'started_at']
    list_filter = ['room', 'difficulty', 'completed']


@admin.register(SessionAnswer)
class SessionAnswerAdmin(admin.ModelAdmin):
    list_display = ['session', 'question', 'player_answer', 'is_correct']
    list_filter = ['is_correct']
