from http.server import BaseHTTPRequestHandler
from model import Tacotron2
import cgi


class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/resource/index.html'
        try:
            if self.path == '/resource/index.html':
                print(self.path[1:])
                f = open(self.path[1:]).read()
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(f, 'utf-8'))
            elif self.path.startswith("/resource") and "." not in self.path:
                print(self.path[1:])
                f = open(self.path[1:], 'rb')
                self.send_response(200)
                self.end_headers()
                self.wfile.write(bytes(f.read()))
            else:
                f = "File not found"
                self.send_error(404, f)
        except OSError:
            f = "File not found"
            self.send_error(404, f)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        file = Tacotron2().to_wave_form(form.getvalue("input").strip())
        self.send_response(self, 200, file)
