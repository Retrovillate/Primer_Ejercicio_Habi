import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from bd_habi import BaseDeDatos

bd = BaseDeDatos()
ESTADOS_VALIDOS = ["pre_venta", "en_venta", "vendido"]

class ServicioConsulta(BaseHTTPRequestHandler):

    def _set_headers(self, codigo=200):
        self.send_response(codigo)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/consultar_inmuebles"):
            # Extraer parámetros conservando valores vacíos
            query = urlparse(self.path).query
            params = parse_qs(query, keep_blank_values=True)
            filtros = {}

            try:
                # Debe venir al menos UNO de los 3 con valor NO vacío
                tiene_valor = False
                for clave in ["ciudad", "ano_construccion", "estado"]:
                    if clave in params and any(v.strip() for v in params[clave] if v is not None):
                        tiene_valor = True
                        break
                if not tiene_valor:
                    raise ValueError(
                        "Debe enviar al menos uno de los parámetros con valor: 'ciudad', 'ano_construccion' o 'estado'."
                    )

                # Validar ciudad (si existe)
                if 'ciudad' in params:
                    ciudad = (params['ciudad'][0] or "").strip()
                    if ciudad == "":
                        raise ValueError("El parámetro 'ciudad' está vacío. Debe ingresar un valor para la consulta.")
                    filtros['ciudad'] = ciudad

                # Validar año de construcción (si existe)
                if 'ano_construccion' in params:
                    valor_ano = (params['ano_construccion'][0] or "").strip()
                    if valor_ano == "":
                        raise ValueError("El parámetro 'ano_construccion' está vacío. Debe ingresar un valor para la consulta.")
                    try:
                        filtros['ano_construccion'] = int(valor_ano)
                    except ValueError:
                        raise ValueError("El parámetro 'ano_construccion' debe ser un número entero.")

                # Validar estado (si existe)
                if 'estado' in params:
                    valor_estado = (params['estado'][0] or "")
                    if valor_estado.strip() == "":
                        raise ValueError("El parámetro 'estado' está vacío. Debe ingresar un valor para la consulta.")
                    # separar por comas y eliminar espacios; prohibir elementos vacíos
                    estados = [e.strip() for e in valor_estado.split(',')]
                    if any(e == "" for e in estados):
                        raise ValueError("El parámetro 'estado' contiene valores vacíos. Use valores válidos separados por comas.")
                    for est in estados:
                        if est not in ESTADOS_VALIDOS:
                            raise ValueError(f"Estado inválido: {est}. Debe ser uno de {ESTADOS_VALIDOS}")
                    filtros['estado'] = estados

                # Obtener resultados desde la base de datos
                resultados = bd.obtener_inmuebles(filtros)

                # Traducir variables al español
                resultados_traducidos = []
                for r in resultados:
                    resultados_traducidos.append({
                        "direccion": r.get("address") or r.get("direccion"),
                        "ciudad": r.get("city") or r.get("ciudad"),
                        "estado": r.get("status_name") or r.get("estado"),
                        "descripcion_estado": r.get("status_label") or r.get("descripcion"),
                        "precio_venta": r.get("price") or r.get("precio_venta"),
                        "ano_construccion": r.get("year") or r.get("ano_construccion"),
                        "fecha_actualizacion": (
                            r.get("update_date").strftime("%Y-%m-%d %H:%M:%S")
                            if r.get("update_date") else None
                        )
                    })

                # Responder
                self._set_headers()
                self.wfile.write(json.dumps({"inmuebles": resultados_traducidos}, ensure_ascii=False).encode('utf-8'))

            except (TypeError, ValueError) as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode('utf-8'))
            except RuntimeError as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": str(e)}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self._set_headers(500)
                self.wfile.write(json.dumps({"error": f"Error inesperado: {e}"}, ensure_ascii=False).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=ServicioConsulta, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Servicio REST corriendo en puerto {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
