import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from bd_habi import BaseDeDatos

bd = BaseDeDatos()

class ServicioConsulta(BaseHTTPRequestHandler):

    def _set_headers(self, codigo=200):
        self.send_response(codigo)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        if self.path == "/consultar_inmuebles":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                filtros = json.loads(post_data)
                resultados = bd.obtener_inmuebles(filtros)
                self._set_headers()
                self.wfile.write(json.dumps(resultados).encode('utf-8'))
            except (TypeError, ValueError) as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            except RuntimeError as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": f"Error inesperado: {e}"}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=ServicioConsulta, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servicio REST corriendo en puerto {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
