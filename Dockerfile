# Use official Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install required OS packages (if needed)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Copy .env file if needed
# (optional: not recommended for prod unless secrets are injected at runtime)
COPY .env .env

# Set environment variables from .env (optional)
# ENV VAR_NAME=value

# Default command
CMD ["python", "src/main.py"]