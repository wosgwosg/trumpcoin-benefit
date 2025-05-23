#!/bin/bash
# TrumpCoin Benefit Program Development Server Script
# This script activates the virtual environment and runs the development server

echo "Starting TrumpCoin Benefit Program Development Server..."
echo

# Activate the virtual environment
source venv/bin/activate

# Run the development server
python manage.py runserver

# If the server stops, keep the window open
echo "Press Enter to exit..."
read
