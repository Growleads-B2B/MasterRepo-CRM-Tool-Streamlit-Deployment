#!/bin/bash

# Create .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Create config file
echo '[server]
headless = true
port = $PORT
enableCORS = false

[browser]
gatherUsageStats = false
serverAddress = "0.0.0.0"

[runner]
magicEnabled = true
fastReruns = true

[client]
showErrorDetails = false
toolbarMode = "minimal"' > .streamlit/config.toml

# Run the app
streamlit run app.py
