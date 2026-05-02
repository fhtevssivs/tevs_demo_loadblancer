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
PORT = int(config.get('SERVER3_PORT', 8002))
CERT_DIR = config.get('CERT_DIR', 'certs')
CERT_FILE = os.path.join(CERT_DIR, 'webserver2.crt')
KEY_FILE = os.path.join(CERT_DIR, 'webserver2.key')

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"I am webserver 2 (webserver2.tevs)")

if __name__ == "__main__":
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        print(f"webserver2.tevs running on HTTPS port {PORT}")
        httpd.serve_forever()
