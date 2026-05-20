# TEVS Demo HA High Availability Load Balancer

A demonstration of a High Availability (HA) load balancer setup using **HAProxy** and **Keepalived** running in Docker containers.

## Project Overview

This project extends the simple load balancer by adding redundancy:
- **Two HAProxy Nodes (`haproxy1`, `haproxy2`)**: Redundant load balancers.
- **Keepalived**: Manages an internal Virtual IP (VIP) `10.21.0.100` across the HAProxy nodes.
- **Gateway Container**: A helper service that maps `localhost:8000` to the internal VIP.
- **Failover**: If the Master node fails, the VIP automatically moves to the Backup node.
- **Backend Servers (`webserver1`, `webserver2`)**: Containerized Python web servers.

## The Gateway Workaround (Local Demo)

In a **real-world** High Availability setup, the Keepalived VIP (`10.21.0.100`) would be assigned to a physical network interface accessible by other machines on the network.

**For this local demonstration**, accessing a Docker bridge VIP directly from your host machine can be unreliable and OS-dependent. To ensure this demo works out-of-the-box on any machine:
1. We added a **Gateway container** (HAProxy in TCP mode).
2. This container listens on your host's **localhost:8000**.
3. It forwards all traffic to the internal **VIP (10.21.0.100)**.

This allows you to test the failover logic (stopping `haproxy1` and seeing `haproxy2` take over) without needing complex network routing on your host machine.

## Features

- **Redundancy**: Multiple load balancer instances.
- **Virtual IP (VIP)**: An internal IP address that always points to an active load balancer.
- **Automatic Failover**: VRRP protocol ensures high availability.
- **Gateway Access**: Easy local testing via `localhost:8000`.

## Setup Instructions

### 1. Generate SSL Certificates
Generate the local CA and certificates:
```bash
./prepare_certs.sh
```

### 2. Configure Local DNS
Add the .tevs hostname to your system's `/etc/hosts` file. This maps `loadbalancer.tevs` to `127.0.0.1` (which hits the Gateway).
```bash
sudo ./manage_hosts.sh add
```

### 3. Start the Setup
Launch the entire stack:
```bash
./start_servers.sh
```

## Testing High Availability

1. **Access the Load Balancer**:
   ```bash
   curl -k https://loadbalancer.tevs:8000
   ```
2. **Identify the Active Node**:
   Check the stats or logs to see which HAProxy instance is receiving the requests.
3. **Simulate a Failure**:
   Stop the master container:
   ```bash
   docker stop 03_load_balancer_high_available-haproxy1-1
   ```
4. **Verify Failover**:
   Run the curl command again. The request will still succeed because:
   - The Gateway still points to `10.21.0.100`.
   - Keepalived has moved `10.21.0.100` from `haproxy1` to `haproxy2`.
   - `haproxy2` is now handling the traffic.

### Monitoring

HAProxy statistics (via haproxy1):
- **URL**: [http://localhost:8404/stats](http://localhost:8404/stats)
- **Credentials**: `admin` / `admin`

## Cleanup

To stop the servers and containers, press Ctrl+C in the terminal.

To remove the entries from your /etc/hosts file:
```bash
sudo ./manage_hosts.sh remove
```
