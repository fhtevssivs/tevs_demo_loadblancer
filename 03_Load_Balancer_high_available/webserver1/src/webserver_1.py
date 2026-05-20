import http.server
import socketserver
import ssl
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("webserver1")

def load_env():
    env = {}
    # Check local, then parent, then project root relative to this script
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
PORT = int(config.get('SERVER2_PORT', 8001))
CERT_DIR = config.get('CERT_DIR', 'certs')
# Handle relative path for certs if needed
if not os.path.isabs(CERT_DIR):
    CERT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', CERT_DIR)

CERT_FILE = os.path.join(CERT_DIR, 'webserver1.crt')
KEY_FILE = os.path.join(CERT_DIR, 'webserver1.key')

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        logger.info(f"Received request from {self.client_address}")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"I am webserver 1 (webserver1.tevs)")

    def log_message(self, format, *args):
        # Silence default http.server logging to use our own
        pass

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        logger.info(f"webserver1.tevs running on HTTPS port {PORT}")
        httpd.serve_forever()
