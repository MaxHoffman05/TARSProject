#!/usr/bin/env bash
#Start the backend with this script
echo "Starting backend"
cd backend

fastapi dev main.py
