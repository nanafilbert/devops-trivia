A production-grade real-time trivia game built with Django, WebSockets, and PostgreSQL — deployed on AWS EC2 behind an Application Load Balancer. Test your knowledge of cloud infrastructure, networking, security, containers, and more.

**Live:** [https://api.therealblessing.com](https://api.therealblessing.com)

---

## What It Is

DevOps Trivia is a browser-based quiz game where players select a topic room, choose a difficulty, and answer 10 questions against a live leaderboard. Every completed game instantly updates the global leaderboard visible to all connected players in real time using WebSockets.

The game covers 10 deep technical topic rooms:

| Room | Topics Covered |
|------|---------------|
| Infrastructure & Cloud | VPCs, auto scaling, IaC, disaster recovery, cloud patterns |
| Security & Defense | Encryption, zero trust, OWASP, penetration testing, CVEs |
| Networking & Protocols | TCP/IP, BGP, DNS, routing, firewalls, VPNs |
| Containers & Orchestration | Docker, Kubernetes, CNI, operators, eBPF |
| CI/CD & Automation | GitHub Actions, OIDC, DORA metrics, GitOps, testing |
| Observability & Reliability | SLOs, OpenTelemetry, Prometheus, chaos engineering |
| Databases & Storage | MVCC, sharding, replication, WAL, indexing |
| Architecture & Design | Microservices, CQRS, event sourcing, DDD, CAP theorem |
| Linux & Systems | Kernel, processes, memory, namespaces, cgroups |
| APIs & Communication | REST, GraphQL, gRPC, WebSockets, message queues |

Each room has 30 easy and 30 hard questions — answers are shuffled on every game so the correct answer never appears in a predictable position.

---

## Architecture
Internet
│
▼ HTTPS (ACM certificate — auto-renewing)
Application Load Balancer
│ HTTP :80
▼
Server A — Production (private subnet, us-east-1a)
├── Nginx          reverse proxy
├── Django         application (Gunicorn + Daphne for WebSockets)
├── Celery         background task worker
├── PostgreSQL     relational database (no exposed ports)
├── Neo4j          graph database (no exposed ports)
└── Gotenberg      PDF converter (internal only)
│
│ WireGuard encrypted tunnel 10.99.0.0/24
▼
Server B — Workers (private subnet, us-east-1b)
├── Redis          WebSocket channel layer + task queue
├── Airflow        job scheduler
├── JupyterHub     data notebooks
└── WireGuard      VPN peer

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Web server | Nginx 1.25 | Reverse proxy, security headers |
| Application | Django 6 + Daphne | HTTP + WebSocket handling |
| WebSockets | Django Channels + Redis | Real-time leaderboard updates |
| Database | PostgreSQL 15 | Game sessions, questions, answers |
| Cache / Queue | Redis 7 | Channel layer, Celery broker |
| Task queue | Celery | Background processing |
| Static files | WhiteNoise | Serving static assets efficiently |
| Container | Docker + Docker Compose | Consistent deployment |
| Load balancer | AWS ALB | SSL termination, health checks |
| SSL | AWS ACM | Free auto-renewing certificates |
| Infrastructure | AWS EC2, VPC, NAT Gateway | Cloud hosting |
| VPN | WireGuard | Encrypted server-to-server tunnel |

---

## Key Design Decisions

### Private subnets for all compute
Both EC2 instances live in private subnets with no public IPs. The only public entry point is the ALB. Even if a security group is misconfigured, the instances cannot be reached directly from the internet.

### ALB + ACM instead of Certbot
SSL terminates at the ALB using AWS Certificate Manager. ACM auto-renews certificates with no cron jobs, no scripts, and no failure modes. This removes an entire class of operational burden from the stack.

### IAM Instance Profile instead of static credentials
EC2 instances assume an IAM role at boot and receive rotating temporary credentials automatically via the AWS metadata service at `169.254.169.254`. No AWS access keys exist in any `.env` file anywhere.

### WireGuard VPN tunnel
All cross-server traffic — Celery connecting to Redis, Airflow connecting to Postgres — flows through an encrypted WireGuard tunnel. Redis listens only on the WireGuard subnet IP `10.99.0.2`, making it unreachable from the internet.

### Docker network isolation
Server A runs two Docker networks. Nginx is on the frontend network with Django only. Postgres and Neo4j are on the backend network with Django only. Nginx cannot reach Postgres directly. Databases have zero exposed host ports — completely invisible outside Docker.

### WebSocket channel layer
Django Channels handles WebSocket connections for real-time updates. Redis serves as the channel layer backend. When a player finishes a game, the consumer broadcasts a leaderboard update to all connected clients simultaneously using channel groups.

### Answer shuffling
All four answer options are shuffled on each game session so the correct answer appears in a random position every time. The shuffled order is stored in the Django session and verified server-side, preventing client-side cheating.

---

## Known Tradeoffs

### Single NAT Gateway
One NAT Gateway serves both private subnets. In a full production environment you would deploy one NAT Gateway per availability zone for high availability — if the AZ hosting the NAT Gateway fails, outbound internet access for both servers is lost. The cost savings (~$32/month) outweigh this risk for the current scale.

### SQLite in development, Postgres in production
The container defaults to SQLite when `DATABASE_URL` is not set, making local development simple. The Dockerfile runs migrations on startup so the container is always ready.

### Migrations run on container start
`python manage.py migrate` runs every time the container starts. This is safe because Django migrations are idempotent — re-running them applies only pending changes. In a high-scale environment you would run migrations as a separate init container or job.

### Next evolution
The next architecture improvement would move both EC2 instances to private subnets with separate NAT Gateways per AZ, add a second Server A instance behind the ALB for horizontal scaling, and implement the CI/CD pipeline with GitHub Actions and OIDC federation.

---

## Local Development

### Prerequisites
- Python 3.12
- Redis running locally or via Docker

### Setup
```bash
git clone https://github.com/nanafilbert/devops-trivia.git
cd devops-trivia

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_questions
python manage.py seed_more_questions

daphne -p 8000 trivia.asgi:application
```

Visit `http://localhost:8000`

### Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DJANGO_SECRET_KEY` | Django secret key | insecure dev key |
| `DJANGO_DEBUG` | Debug mode | `True` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed hosts | `localhost,127.0.0.1` |
| `DATABASE_URL` | Postgres connection URL | SQLite |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` |
| `CELERY_BROKER_URL` | Celery broker URL | same as REDIS_URL |

---

## Docker
```bash
docker build -t devops-trivia .

docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY=your-secret-key \
  -e DJANGO_ALLOWED_HOSTS=localhost \
  devops-trivia
```

---

## Game Flow
Player visits site
│
▼
Live leaderboard loads via WebSocket
│
Player enters username → selects room → selects difficulty
│
▼
10 random questions from room at chosen difficulty
Answer options shuffled randomly each game
│
Wrong answer → correct answer shown → next question
Correct answer → score increments → next question
│
▼
Game complete → result screen
Score broadcasts to leaderboard via WebSocket
All connected players see update instantly

---

## Project Structure
devops-trivia/
├── trivia/
│   ├── settings.py          Django configuration
│   ├── urls.py              URL routing
│   └── asgi.py              ASGI entry point with WebSocket routing
├── game/
│   ├── models.py            Room, Question, GameSession, SessionAnswer
│   ├── views.py             HTTP views for game flow
│   ├── consumers.py         WebSocket consumers for real-time updates
│   ├── routing.py           WebSocket URL patterns
│   ├── admin.py             Django admin registration
│   └── management/
│       └── commands/
│           ├── seed_questions.py       Base question set
│           └── seed_more_questions.py  Extended question set
├── templates/
│   ├── base.html            Base template with CRT effect and matrix background
│   └── game/
│       ├── landing.html     Homepage with live leaderboard
│       ├── rooms.html       Room selection
│       ├── game.html        Active game with WebSocket answer submission
│       ├── complete.html    Results screen
│       └── error.html       Error page
├── static/
│   └── css/main.css         Retro pixel art theme
├── Dockerfile               Multi-stage production build
└── requirements.txt         Python dependencies

---

## Infrastructure Repository

The AWS infrastructure that runs this application is documented separately:

**[github.com/nanafilbert/eks-to-ec2](https://github.com/nanafilbert/eks-to-ec2)**

That repository covers the complete two-server EC2 stack including VPC setup, security groups, ALB configuration, WireGuard VPN, Docker Compose configurations for both servers, backup scripts, and provisioning automation.

---

## What's Next

- [ ] GitHub Actions CI/CD pipeline with OIDC federation to AWS
- [ ] Automatic deployment to Server A on every push to main
- [ ] Terraform replacing manual AWS setup
- [ ] Second NAT Gateway for AZ redundancy
- [ ] CloudWatch alarms and dashboards
- [ ] User accounts for tracking personal progress over time
- [ ] More question rooms — Terraform, Ansible, Python, Go