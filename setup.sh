#!/bin/bash
mkdir -p ~/.streamlit/
echo "
[general]\n
email = "[youremail@gmail.com](mailto:youremail@gmail.com)"\n
" > ~/.streamlit/credentials.toml
echo "
[server]\n
headless = true\n
enableCORS = false\n
enableXsrfProtection = false\n
port = $PORT\n
" > ~/.streamlit/config.toml
echo "
[theme]\n
base = "light"\n
primaryColor = "#0d6efd"\n
backgroundColor = "#f8f9fa"\n
secondaryBackgroundColor = "#e9ecef"\n
textColor = "#000000"\n
font = "sans serif"\n
" >> ~/.streamlit/config.toml
echo "✅ Streamlit environment configured successfully for MediScan."
