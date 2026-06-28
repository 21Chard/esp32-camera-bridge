from http.server import HTTPServer, BaseHTTPRequestHandler

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ESP32 Camera Bridge OK")

HTTPServer(("0.0.0.0", 8088), Handler).serve_forever()
