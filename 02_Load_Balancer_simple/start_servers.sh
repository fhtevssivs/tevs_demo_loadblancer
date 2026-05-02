#!/bin/bash

# Kill background processes and stop containers on exit
trap 'docker compose down' EXIT

# Generate certificates locally first so they can be mounted
./prepare_certs.sh

echo "Starting full stack with Docker Compose..."
docker compose up --build -d

echo ""
echo "=================================================="
echo "FULL STACK IS ACTIVE (Dockerized)"
echo "Click here to access: https://loadbalancer.tevs:8000"
echo "=================================================="
echo ""

echo "Following logs (Ctrl+C to stop)..."
docker compose logs -f
