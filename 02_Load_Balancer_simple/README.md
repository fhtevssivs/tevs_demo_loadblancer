# TEVS Demo HAProxy Load Balancer

A demonstration of a round-robin load balancer using **HAProxy** running in a Docker container, balancing requests between two Python backend web servers.

## Project Overview

This project simulates a load-balanced architecture:
- **HAProxy (`/haproxy`)**: A containerized HAProxy instance with its own Dockerfile and config.
- **Backend Servers (`/webserver1`, `/webserver2`)**: Two separate containerized Python web servers, each with their own Dockerfile and source code.

## Features

- **Component-Based Structure**: Each service has its own directory and Dockerfile.
- **HAProxy Integration**: Uses a industry-standard load balancer for SSL termination.
- **Fully Dockerized**: Managed by Docker Compose with internal networking.
- **Local DNS**: Custom .tevs hostnames managed via a helper script.

## Setup Instructions
...

### 1. Generate SSL Certificates
Generate the local CA and certificates (including the combined .pem for HAProxy):
```bash
./prepare_certs.sh
```

### 2. Configure Local DNS
Add the .tevs hostnames to your system's /etc/hosts file. This requires sudo:
```bash
sudo ./manage_hosts.sh add
```

### 3. Start the Setup
Launch the backend servers and the HAProxy container:
```bash
./start_servers.sh
```

## Testing

You can test the setup using curl. Use the -k (insecure) flag for self-signed certs:

```bash
# Access the HAProxy load balancer
curl -k https://loadbalancer.tevs:8000
```

Repeatedly running the command will show responses from webserver1 and webserver2 as HAProxy proxies the requests in a round-robin fashion.

## Cleanup

To stop the servers and the container, press Ctrl+C in the terminal.

To remove the entries from your /etc/hosts file:
```bash
sudo ./manage_hosts.sh remove
```
