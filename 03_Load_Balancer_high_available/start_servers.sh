#!/bin/bash

# Kill background processes and stop containers on exit
trap 'docker compose down' EXIT

# Generate certificates locally first so they can be mounted
./prepare_certs.sh

echo "Starting High Available stack with Docker Compose..."
docker compose up --build -d

echo ""
echo "=================================================="
echo "HIGH AVAILABLE STACK IS ACTIVE (via Gateway)"
echo "Virtual IP (Internal): 10.21.0.100"
echo "Load Balancer: https://loadbalancer.tevs:8000"
echo "               (Maps to localhost:8000 -> Gateway -> VIP)"
echo ""
echo "HAProxy 1 Internal IP: 10.21.0.10"
echo "HAProxy 2 Internal IP: 10.21.0.11"
echo "HAProxy Stats: http://localhost:8404/stats (via haproxy1)"
echo "=================================================="
echo ""

echo "Following logs (Ctrl+C to stop)..."
docker compose logs -f
