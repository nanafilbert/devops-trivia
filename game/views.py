from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
import json
import random
from .models import Room, Question, GameSession


def landing(request):
    return render(request, 'game/landing.html')


def rooms(request):
    username = request.GET.get('username', '').strip()
    if len(username) < 4:
        return redirect('landing')
    rooms = Room.objects.all()
    return render(request, 'game/rooms.html', {
        'rooms': rooms,
        'username': username
    })


def join_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    username = request.GET.get('username', '').strip()
    difficulty = request.GET.get('difficulty', 'easy')

    if len(username) < 4:
        return redirect('landing')

    questions = list(Question.objects.filter(room=room, difficulty=difficulty))

    if len(questions) < 10:
        questions = list(Question.objects.filter(room=room))

    if not questions:
        return render(request, 'game/error.html', {
            'message': 'No questions available for this room yet.'
        })

    selected = random.sample(questions, min(10, len(questions)))

    session = GameSession.objects.create(
        username=username,
        room=room,
        difficulty=difficulty,
        total_questions=len(selected)
    )

    # Store just the question IDs — shuffle happens at display time
    request.session[str(session.id)] = [q.id for q in selected]

    return redirect('game', session_id=session.id)


def game(request, session_id):
    session = get_object_or_404(GameSession, id=session_id)
    return render(request, 'game/game.html', {'session': session})


def get_question(request, session_id):
    session = get_object_or_404(GameSession, id=session_id)
    question_ids = request.session.get(str(session_id), [])
    answered_count = session.answers.count()

    if answered_count >= len(question_ids) or session.completed:
        return JsonResponse({'complete': True, 'score': session.score})

    question_id = question_ids[answered_count]
    question = get_object_or_404(Question, id=question_id)

    # Get the correct answer text
    correct_text = getattr(question, f'option_{question.correct_answer}')

    # Shuffle the option values, then assign new letters by position
    values = [question.option_a, question.option_b, question.option_c, question.option_d]
    random.shuffle(values)

    labels = ['a', 'b', 'c', 'd']
    shuffled_options = dict(zip(labels, values))

    # The correct letter is whichever label now holds the correct text
    new_correct = next(k for k, v in shuffled_options.items() if v == correct_text)

    shuffled_key = f'{session_id}_correct_{question_id}'
    request.session[shuffled_key] = new_correct
    request.session.modified = True

    return JsonResponse({
        'complete': False,
        'question_number': answered_count + 1,
        'total': session.total_questions,
        'question': {
            'id': question.id,
            'text': question.text,
            'options': shuffled_options,
            'correct': new_correct
        }
    })


def game_complete(request, session_id):
    session = get_object_or_404(GameSession, id=session_id)
    return render(request, 'game/complete.html', {'session': session})
