import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class LeaderboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('leaderboard', self.channel_name)
        await self.accept()
        await self.send_leaderboard()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('leaderboard', self.channel_name)

    async def send_leaderboard(self):
        leaderboard = await self.get_leaderboard()
        await self.send(text_data=json.dumps({
            'type': 'leaderboard_update',
            'leaderboard': leaderboard
        }))

    async def leaderboard_update(self, event):
        await self.send_leaderboard()

    @database_sync_to_async
    def get_leaderboard(self):
        from .models import GameSession
        sessions = GameSession.objects.filter(
            completed=True
        ).select_related('room').order_by('-score', 'finished_at')[:20]

        return [
            {
                'username': s.username,
                'room': s.room.name,
                'score': s.score,
                'total': s.total_questions,
                'duration': str(s.finished_at - s.started_at).split('.')[0] if s.finished_at else None,
            }
            for s in sessions
        ]


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.room_group = f'game_{self.session_id}'
        await self.channel_layer.group_add(self.room_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'answer':
            result = await self.process_answer(
                data['session_id'],
                data['question_id'],
                data['answer'],
                data.get('shuffled_correct')
            )
            await self.send(text_data=json.dumps(result))
            if result.get('game_complete'):
                await self.broadcast_leaderboard_update()

    async def broadcast_leaderboard_update(self):
        from channels.layers import get_channel_layer
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            'leaderboard',
            {'type': 'leaderboard_update'}
        )

    @database_sync_to_async
    def process_answer(self, session_id, question_id, answer, shuffled_correct=None):
        from .models import GameSession, Question, SessionAnswer
        from django.utils import timezone

        try:
            session = GameSession.objects.get(id=session_id)
            question = Question.objects.get(id=question_id)
        except (GameSession.DoesNotExist, Question.DoesNotExist):
            return {'error': 'Invalid session or question'}

        # Use the shuffled correct answer sent from the frontend
        correct_answer = shuffled_correct if shuffled_correct else question.correct_answer
        is_correct = answer.lower() == correct_answer.lower()

        SessionAnswer.objects.create(
            session=session,
            question=question,
            player_answer=answer,
            is_correct=is_correct
        )

        if is_correct:
            session.score += 1
            session.save()

        answers_count = session.answers.count()
        game_complete = answers_count >= session.total_questions

        if game_complete:
            session.completed = True
            session.finished_at = timezone.now()
            session.save()

        return {
            'type': 'answer_result',
            'is_correct': is_correct,
            'correct_answer': correct_answer,
            'score': session.score,
            'question_number': answers_count,
            'game_complete': game_complete,
        }
