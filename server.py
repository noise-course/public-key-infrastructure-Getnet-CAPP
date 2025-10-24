from http.server import HTTPServer, BaseHTTPRequestHandler
import ssl
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            if os.path.exists('index.html'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('index.html', 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'index.html not found')
        elif self.path in ['/sample.jpg', '/another_image.jpg']:
            if os.path.exists(self.path[1:]):
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                with open(self.path[1:], 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Image not found')
        elif self.path == '/style.css':
            if os.path.exists('style.css'):
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                with open('style.css', 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.send_response(200)
                self.send_header('Content-type', 'text/css')
                self.end_headers()
                self.wfile.write(b'')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        if self.path == '/submit':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'r') as file:
                html = file.read()
            html = html.replace('<div id="postOutput"></div>', f'<div id="postOutput">Received: {post_data}</div>')
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

# Run HTTPS server
server_address = ('', 8443)
httpd = HTTPServer(server_address, SimpleHandler)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile='server.crt', keyfile='server.key')
httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
print('HTTPS server running at https://localhost:8443')
httpd.serve_forever()