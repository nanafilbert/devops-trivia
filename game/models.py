from django.db import models
import uuid

class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('hard', 'Hard'),
    ]
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)  # 'a', 'b', 'c', or 'd'
    difficulty = models.CharField(max_length=4, choices=DIFFICULTY_CHOICES)

    def __str__(self):
        return f"{self.room.name} — {self.text[:50]}"


class GameSession(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('hard', 'Hard'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='sessions')
    difficulty = models.CharField(max_length=4, choices=DIFFICULTY_CHOICES)
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=10)
    completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} — {self.room.name} — {self.score}/{self.total_questions}"


class SessionAnswer(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    player_answer = models.CharField(max_length=1)  # 'a', 'b', 'c', or 'd'
    is_correct = models.BooleanField()
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.session.username} — Q{self.question.id} — {'✓' if self.is_correct else '✗'}"
    
    
    