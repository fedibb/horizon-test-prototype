FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p tests evidence

# Set Python path
ENV PYTHONPATH=/app

# Default command: generate tests and run them
CMD ["sh", "-c", "python generator/generator.py && pytest tests/ -v --html=evidence/report.html --self-contained-html"]
