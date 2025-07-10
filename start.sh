#!/bin/bash
# Start Flask in background
python app.py &

# Start Streamlit
streamlit run frontend.py --server.port $PORT --server.enableCORS false
