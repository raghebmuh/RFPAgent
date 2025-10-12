# MCP-Doc Server Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# Create directory for generated documents
RUN mkdir -p /app/documents

# Expose port
EXPOSE 8080

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV MCP_SERVER_HOST=0.0.0.0
ENV MCP_SERVER_PORT=8080

# Run the FastMCP server
CMD ["python", "server.py"]
