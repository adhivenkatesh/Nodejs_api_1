# Use an official Python runtime base image
FROM python:3.11-slim

# Set environment system variables
ENV PYTHONUNBUFFERED=1

# Install only basic network/CA tools (Removes heavy C++ compilers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set working container directory
WORKDIR /app

# Copy dependency mappings and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application script assets into the container workspace
COPY app.py .
COPY app.html .

# Expose web server port
EXPOSE 7000

# Run backend application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7000"]