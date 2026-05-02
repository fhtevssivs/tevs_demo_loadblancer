#!/bin/bash

# Kill background processes on exit
trap 'kill 0' EXIT

echo "Starting webserver1.tevs on port 8001 (HTTPS)..."
python3 src/webserver_1.py &

echo "Starting webserver2.tevs on port 8002 (HTTPS)..."
python3 src/webserver_2.py &

# Wait a moment for backends to start
sleep 1

echo "Starting loadbalancer.tevs on port 8000 (HTTPS)..."
python3 src/loadbalancer.py &

echo "All servers started. Press Ctrl+C to stop."
wait
