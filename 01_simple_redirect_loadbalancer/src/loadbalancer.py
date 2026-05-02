import http.server
import socketserver
import ssl
import os

def load_env():
    env = {}
    path = '.env' if os.path.exists('.env') else '../../.env'
    try:
        with open(path) as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    env[key] = value
    except FileNotFoundError:
        pass
    return env

config = load_env()
PORT = int(config.get('SERVER1_PORT', 8000))
CERT_DIR = config.get('CERT_DIR', 'certs')
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
        
        self.send_response(302)
        self.send_header('Location', target)
        self.end_headers()
        print(f"Redirecting to {target}")

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    with socketserver.TCPServer(("", PORT), RedirectHandler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print(f"loadbalancer.tevs running on HTTPS port {PORT}")
        print(f"Configured backends: {BACKENDS}")
        httpd.serve_forever()
