#!/bin/bash
# Setup script for Render / Heroku-like platforms
# Streamlit will use the PORT environment variable provided by the host.
if [ -z "$PORT" ]; then
  PORT=8501
fi
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
