FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make sure the script is executable
RUN chmod +x start_railway.sh

# Expose port for Streamlit
EXPOSE 8501

# Start the application with the simplified app
CMD ["streamlit", "run", "app_railway.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
