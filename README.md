# TEVS Load Balancer Demos

This repository provides a step-by-step progression of load balancer implementations, demonstrating different levels of complexity and robustness. It serves as a practical guide for setting up load-balanced infrastructures using Python, Docker, HAProxy, and Keepalived.

## Overview

The project is divided into three main demonstrations, each building upon the previous one:

### 1. [Simple Redirect Load Balancer](./01_simple_redirect_loadbalancer/)
A basic implementation using pure Python.
- **Mechanism**: The load balancer receives a request and issues an HTTP 302 Redirect to one of the backend servers.
- **Tech Stack**: Python `http.server`, `ssl`.
- **Key Learning**: Basic round-robin logic and HTTPS certificate handling without complex infrastructure.

### 2. [Simple HAProxy Load Balancer](./02_Load_Balancer_simple/)
A standard industry-level setup using HAProxy in a containerized environment.
- **Mechanism**: HAProxy acts as a reverse proxy, terminating SSL and forwarding traffic to backend containers.
- **Tech Stack**: Docker, Docker Compose, HAProxy, Python backends.
- **Key Learning**: Container orchestration, HAProxy configuration, and SSL termination in a proxy.

### 3. [High Availability Load Balancer](./03_Load_Balancer_high_available/)
An enterprise-grade redundant setup designed for maximum uptime.
- **Mechanism**: Two HAProxy instances managed by Keepalived. They share a Virtual IP (VIP). If the master fails, the backup takes over the VIP instantly.
- **Tech Stack**: Docker, HAProxy, Keepalived (VRRP), Gateway Proxy for local testing.
- **Key Learning**: Redundancy, failover mechanisms, Virtual IP management, and high-availability architecture.

---

## Shared Features

All demos share several common components to ensure a consistent and realistic testing environment:

- **HTTPS by Default**: All setups use SSL/TLS. A `prepare_certs.sh` script is provided in each folder to generate local CA and server certificates.
- **Local DNS Management**: A `manage_hosts.sh` script helps manage custom `.tevs` hostnames (e.g., `loadbalancer.tevs`) in your system's `/etc/hosts` file.
- **Automated Startup**: Each demo includes a `start_servers.sh` script to quickly launch the entire stack.
- **Statistics Dashboard**: The HAProxy-based demos include a built-in monitoring dashboard (usually at `http://localhost:8404/stats`).

## Getting Started

To explore a demo, navigate to its directory and follow the instructions in its specific `README.md`. Generally, the workflow is:

1.  **Generate Certificates**: `./prepare_certs.sh`
2.  **Setup DNS**: `sudo ./manage_hosts.sh add`
3.  **Run**: `./start_servers.sh`

## Prerequisites

- **Docker & Docker Compose** (for demos 02 and 03)
- **Python 3.x**
- **OpenSSL** (for certificate generation)
- **Sudo privileges** (for modifying `/etc/hosts`)
- **Operating System**: Linux based OS (Tested with Ubuntu 24.x+)
