FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml ./
COPY .env.example ./
COPY src/ ./src/

# Install dependencies
RUN pip install --no-cache-dir -e .

# Copy .env.example if .env doesn't exist
RUN if [ ! -f .env ]; then cp .env.example .env; fi

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
