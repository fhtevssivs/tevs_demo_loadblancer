import http.server
import socketserver
import ssl
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("loadbalancer")

def load_env():
    env = {}
    script_dir = os.path.dirname(os.path.abspath(__file__))
    paths = [
        os.path.join(script_dir, '.env'),
        os.path.join(script_dir, '..', '.env'),
        os.path.join(script_dir, '..', '..', '.env')
    ]
    for path in paths:
        if os.path.exists(path):
            try:
                with open(path) as f:
                    for line in f:
                        if '=' in line:
                            key, value = line.strip().split('=', 1)
                            env[key] = value
                return env
            except Exception:
                pass
    return env

config = load_env()
PORT = int(config.get('SERVER1_PORT', 8000))
CERT_DIR = config.get('CERT_DIR', 'certs')
if not os.path.isabs(CERT_DIR):
    CERT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', CERT_DIR)

CERT_FILE = os.path.join(CERT_DIR, 'loadbalancer.crt')
KEY_FILE = os.path.join(CERT_DIR, 'loadbalancer.key')

BACKENDS = [
    config.get('SERVER2_URL', 'https://webserver1.tevs:8001'),
    config.get('SERVER3_URL', 'https://webserver2.tevs:8002')
]

current_backend = 0

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global current_backend
        target = BACKENDS[current_backend]
        current_backend = (current_backend + 1) % len(BACKENDS)
        
        logger.info(f"Redirecting {self.client_address} to {target}")
        
        self.send_response(302)
        self.send_header('Location', target)
        self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    with socketserver.TCPServer(("", PORT), RedirectHandler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        
        # Display the clickable link
        print("\n" + "="*50)
        print(f"LOAD BALANCER IS ACTIVE")
        print(f"Click here to access: https://loadbalancer.tevs:{PORT}")
        print("="*50 + "\n")
        
        logger.info(f"loadbalancer.tevs running on HTTPS port {PORT}")
        logger.info(f"Configured backends: {BACKENDS}")
        httpd.serve_forever()
