# ── Build stage ───────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Apply OS security patches then install build dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# 1. Upgrade pip, setuptools, and msgpack FIRST
RUN pip install --no-cache-dir --upgrade pip "setuptools>=83.0.0" "msgpack>=1.2.1"

# 2. Install requirements (force upgrade setuptools and msgpack if requirements.txt contains older versions)
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade "setuptools>=83.0.0" "msgpack>=1.2.1"

# ── Runtime stage ─────────────────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Apply OS security patches
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Safety check: Ensure runtime image keeps the clean patched versions after COPY
RUN pip install --no-cache-dir --upgrade pip "setuptools>=83.0.0" "msgpack>=1.2.1"

COPY . .

RUN python manage.py collectstatic --noinput

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py seed_questions && python manage.py seed_more_questions && daphne -b 0.0.0.0 -p 8000 trivia.asgi:application"]