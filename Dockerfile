FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy and install python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose Hugging Face Space default port
EXPOSE 7860

# Run FastAPI server via uvicorn
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "7860"]
