#!/bin/bash

# Set environment variable to use external Baserow
export BASEROW_INTEGRATION_MODE="external"

# Create a simple configuration file for external Baserow
cat > .baserow_config.json << EOL
{
    "api_token": "YOUR_API_TOKEN",
    "table_id": "YOUR_TABLE_ID",
    "base_url": "https://api.baserow.io"
}
EOL

# Start Streamlit app
echo "Starting Streamlit app with external Baserow..."
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
