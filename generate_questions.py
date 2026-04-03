import anthropic
import json

client = anthropic.Anthropic()

ROOMS = {
    'Networking': 'DNS, TCP/IP, subnets, CIDR, routing, firewalls, OSI model, VLANs, NAT, BGP, WireGuard, network protocols',
    'AWS Core': 'EC2, VPC, IAM, S3, ALB, security groups, route tables, NAT gateway, ACM, EBS, CloudWatch, Auto Scaling',
    'Docker': 'containers, images, Dockerfile, Docker Compose, volumes, networks, multi-stage builds, health checks, registries',
    'Nginx': 'reverse proxy, server blocks, upstream, proxy_pass, SSL config, headers, rate limiting, load balancing, location blocks',
    'Security': 'SSL/TLS, encryption, IAM policies, least privilege, VPN, CSRF, XSS, JWT, zero trust, secrets management',
}

def generate_questions(room_name, topics, difficulty, count=40):
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
        max_tokens=8000,
        messages=[{"role": "user", "content": prompt}]
    )

    text = message.content[0].text.strip()
    if text.startswith('```'):
        text = text.split('```')[1]
        if text.startswith('json'):
            text = text[4:]
    text = text.strip()

    return json.loads(text)

if __name__ == '__main__':
    all_questions = {}

    for room_name, topics in ROOMS.items():
        print(f'Generating questions for {room_name}...')
        all_questions[room_name] = {'easy': [], 'hard': []}

        for difficulty in ['easy', 'hard']:
            print(f'  {difficulty}...')
            questions = generate_questions(room_name, topics, difficulty, 40)
            all_questions[room_name][difficulty] = questions
            print(f'  Generated {len(questions)} {difficulty} questions')

    with open('generated_questions.json', 'w') as f:
        json.dump(all_questions, f, indent=2)

    print(f'Done. Saved to generated_questions.json')
