FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app
# Copy backend .env.docker into image as .env (prod defaults; can be overridden at runtime)
COPY backend/.env.docker /app/.env
COPY backend/data.json /app/data.json
COPY backend/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PORT=8000
EXPOSE 8000

CMD ["/app/entrypoint.sh"]


