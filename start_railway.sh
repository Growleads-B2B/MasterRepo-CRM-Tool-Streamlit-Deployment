#!/bin/bash

# Start Docker service
service docker start

# Start Baserow using the optimized Docker Compose file for Railway
docker-compose -f docker-compose.railway.yml up -d

# Wait for Baserow to be ready
echo "Waiting for Baserow to start..."
for i in {1..30}; do
  if curl -s http://localhost:8080/api/ > /dev/null; then
    echo "Baserow is ready!"
    break
  fi
  echo "Waiting for Baserow... ($i/30)"
  sleep 2
done

# Start Streamlit app
echo "Starting Streamlit app..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
