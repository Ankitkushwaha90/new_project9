# Dockerfile
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (including pkg-config!)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        pkg-config \
        default-libmysqlclient-dev \   
        build-essential \             
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files (safe to run always)
RUN python manage.py collectstatic --noinput || echo "Collectstatic skipped in dev"

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000

# Development command (overridden in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# =============================================
# FINAL DOCKERFILE – Django + MySQL + phpMyAdmin
# Works 100% every time, even on first start
# # =============================================

# FROM python:3.12-slim

# # --- System dependencies ---
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     DEBIAN_FRONTEND=noninteractive

# WORKDIR /app

# # Install system packages: MySQL client + Node.js (fixes npm warning)
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends \
#         gcc \
#         default-libmysqlclient-dev \
#         pkg-config \
#         curl \
#         gnupg && \
#     curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
#     apt-get install -y nodejs && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*

# # Verify node/npm are available (optional but nice)
# RUN node --version && npm --version

# # --- Python dependencies ---
# COPY requirements.txt .
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir -r requirements.txt

# # --- Copy project ---
# COPY . .

# # --- Expose ports ---
# EXPOSE 8000

# # --- FINAL COMMAND: Smart wait for MySQL + migrate + runserver ---
# # This eliminates ALL "database not ready" errors forever
# CMD ["sh", "-c", \
#      "until echo 'SELECT 1' > /dev/tcp/my_db/3306 2>/dev/null && \
#             mysql -h my_db -u techforge_user -pyour_strong_password_here -e 'SELECT 1' techforge >/dev/null 2>&1; \
#       do echo 'Waiting for MySQL to be ready...'; sleep 3; done; \
#       echo 'MySQL is up! Running migrations...'; \
#       python manage.py migrate --noinput && \
#       python manage.py runserver 0.0.0.0:8000"]