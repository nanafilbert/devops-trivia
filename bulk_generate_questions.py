import anthropic
import json
import os
import sys
import django

# Setup Django
sys.path.insert(0, '/home/filbe/WorkSpace/Aws-Projects/gaming-app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trivia.settings')
django.setup()

from game.models import Room, Question

client = anthropic.Anthropic()

def generate_questions(room_name, topics, difficulty, count=50):
    """Generate questions using Claude"""
    prompt = f"""Generate {count} unique multiple choice trivia questions about {room_name} for DevOps engineers.
Topics to cover: {topics}
Difficulty: {difficulty} ({"conceptual understanding, common commands and definitions" if difficulty == "easy" else "deep technical knowledge, edge cases, specific configurations, subtle differences"})

Return ONLY a JSON array with no other text. Each question must have exactly this structure:
{{
    "text": "question text",
    "option_a": "first option",
    "option_b": "second option", 
    "option_c": "third option",
    "option_d": "fourth option",
    "correct_answer": "a"
}}

Rules:
- correct_answer must be a single lowercase letter: a, b, c, or d
- All 4 options must be plausible
- No duplicate questions
- Questions must be specific and technical
- Do not number the questions
- Return only the JSON array, nothing else
"""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=16000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = message.content[0].text.strip()
    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:]
    text = text.strip()

    return json.loads(text)


def import_questions_to_db(room_name, questions, difficulty):
    """Import generated questions into database"""
    room = Room.objects.get(name=room_name)
    added = 0
    
    for q in questions:
        _, created = Question.objects.get_or_create(
            room=room,
            text=q['text'],
            difficulty=difficulty,
            defaults={
                'option_a': q['option_a'],
                'option_b': q['option_b'],
                'option_c': q['option_c'],
                'option_d': q['option_d'],
                'correct_answer': q['correct_answer'],
            }
        )
        if created:
            added += 1
    
    return added


if __name__ == '__main__':
    # Get all rooms from database
    rooms = Room.objects.all()
    
    print(f"Found {rooms.count()} rooms in database")
    print("=" * 60)
    
    total_added = 0
    
    for room in rooms:
        print(f"\n🎯 Processing: {room.name}")
        print(f"   Description: {room.description}")
        
        # Get current counts
        easy_count = Question.objects.filter(room=room, difficulty='easy').count()
        hard_count = Question.objects.filter(room=room, difficulty='hard').count()
        print(f"   Current: {easy_count} easy, {hard_count} hard")
        
        # Generate for each difficulty
        for difficulty in ['easy', 'hard']:
            current = Question.objects.filter(room=room, difficulty=difficulty).count()
            target = 50  # Target 50 questions per difficulty
            
            if current >= target:
                print(f"   ✓ {difficulty.capitalize()}: Already has {current} questions (target: {target})")
                continue
            
            needed = target - current
            print(f"   🔄 {difficulty.capitalize()}: Generating {needed} questions...")
            
            try:
                questions = generate_questions(room.name, room.description, difficulty, needed)
                added = import_questions_to_db(room.name, questions, difficulty)
                total_added += added
                print(f"   ✅ {difficulty.capitalize()}: Added {added} new questions")
            except Exception as e:
                print(f"   ❌ {difficulty.capitalize()}: Error - {e}")
    
    print("\n" + "=" * 60)
    print(f"✨ Done! Added {total_added} new questions total")
    print(f"📊 Total questions in database: {Question.objects.count()}")
