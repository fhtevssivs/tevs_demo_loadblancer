# TEVS Demo Simple Redirect Load Balancer

Part of the [TEVS Load Balancer Demos](../README.md) series.

A demonstration of a simple round-robin load balancer (redirector) and two backend web servers implemented in Python, featuring HTTPS and local DNS management.

## Project Overview

This project simulates a basic load-balanced architecture:
- **Load Balancer (loadbalancer.tevs)**: Receives incoming HTTPS requests and redirects them to one of the two backends using a round-robin strategy.
- **Backend Servers (webserver1.tevs, webserver2.tevs)**: Simple HTTPS servers that identify themselves upon request.

## Features

- **HTTPS by Default**: All communication is secured via SSL/TLS using self-signed certificates.
- **Local DNS**: Custom .tevs hostnames managed via a helper script.
- **Zero Dependencies**: Uses only standard Python libraries (http.server, ssl, socketserver).
- **Configuration**: Managed via a central .env file.

## File Structure

- **src/**: Contains the Python server scripts.
- **certs/**: Generated SSL certificates.
- **.env**: Port and URL configuration.
- **prepare_certs.sh**: Script to generate SSL certificates.
- **manage_hosts.sh**: Script to add/remove .tevs names in /etc/hosts.
- **start_servers.sh**: Script to launch all servers.

## Setup Instructions

### 1. Generate SSL Certificates
Generate the local CA and certificates for the hostnames:
```bash
./prepare_certs.sh
```

Add the ca.crt to your truest browser certs (via Browser settings, otherwise Security warnings)

### 2. Configure Local DNS
Add the .tevs hostnames to your system's /etc/hosts file. This requires sudo:
```bash
sudo ./manage_hosts.sh add
```

### 3. Start the Servers
Launch all three servers simultaneously:
```bash
./start_servers.sh
```

## Testing

You can test the setup using curl. Since the certificates are self-signed, use the -k (insecure) flag:

```bash
# Access the load balancer
curl -kL https://loadbalancer.tevs:8000
```

Repeatedly running the command will show you alternating responses from webserver1.tevs and webserver2.tevs.

## Cleanup

To stop the servers, press Ctrl+C in the terminal where they are running.

To remove the entries from your /etc/hosts file:
```bash
sudo ./manage_hosts.sh remove
```
