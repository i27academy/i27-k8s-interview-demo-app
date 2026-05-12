# ──────────────────────────────────────────────────────
# i27Academy Demo App — Dockerfile
# github.com/i27academy/devops-interview-series
# ──────────────────────────────────────────────────────

FROM python:3.11-slim

# Metadata
LABEL org.opencontainers.image.title="i27Academy Demo App"
LABEL org.opencontainers.image.description="Demo app for Kubernetes Interview Series"
LABEL org.opencontainers.image.url="https://github.com/i27academy/devops-interview-series"
LABEL org.opencontainers.image.vendor="i27Academy"

# Non-root user for security
RUN groupadd -r i27 && useradd -r -g i27 i27

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Own files
RUN chown -R i27:i27 /app

USER i27

# Expose port
EXPOSE 8080

# Environment defaults
ENV APP_VERSION=v1
ENV APP_ENV=production
ENV APP_COLOR=orange
ENV EPISODE=demo
ENV PORT=8080

# Health check built into image
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/healthz')" || exit 1

# Start with gunicorn for production
CMD ["gunicorn", \
     "--bind", "0.0.0.0:8080", \
     "--workers", "2", \
     "--timeout", "60", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "app:app"]
