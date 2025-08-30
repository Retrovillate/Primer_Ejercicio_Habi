import mysql.connector
from mysql.connector import Error
from config_bd import BD_CONFIG

ESTADOS_VALIDOS = ["pre_venta", "en_venta", "vendido"]

class BaseDeDatos:
    def __init__(self):
        self.config = BD_CONFIG

    def conectar(self):
        try:
            conexion = mysql.connector.connect(**self.config)
            return conexion
        except Error as e:
            raise ConnectionError(f"Error al conectarse a la base de datos: {e}")

    def obtener_inmuebles(self, filtros):
        # Validaciones de tipos
        if 'ciudad' in filtros and filtros['ciudad'] is not None and not isinstance(filtros['ciudad'], str):
            raise TypeError("El filtro 'ciudad' debe ser una cadena de texto")
        if 'ano_construccion' in filtros and filtros['ano_construccion'] is not None and not isinstance(filtros['ano_construccion'], int):
            raise TypeError("El filtro 'ano_construccion' debe ser un entero")
        if 'estado' in filtros and filtros['estado'] is not None:
            if not isinstance(filtros['estado'], list):
                raise TypeError("El filtro 'estado' debe ser una lista")
            for est in filtros['estado']:
                if est not in ESTADOS_VALIDOS:
                    raise ValueError(f"Estado inválido: {est}. Debe ser uno de {ESTADOS_VALIDOS}")

        try:
            conexion = self.conectar()
            cursor = conexion.cursor(dictionary=True)

            query_base = """
                SELECT i.direccion, i.ciudad, s.estado, i.precio_venta, i.descripcion
                FROM inmuebles i
                JOIN status_history s ON s.inmueble_id = i.id
                WHERE s.id = (
                    SELECT MAX(sh.id)
                    FROM status_history sh
                    WHERE sh.inmueble_id = i.id
                )
            """

            filtros_sql = []
            valores = []

            if 'ciudad' in filtros and filtros['ciudad']:
                filtros_sql.append("i.ciudad = %s")
                valores.append(filtros['ciudad'])

            if 'ano_construccion' in filtros and filtros['ano_construccion']:
                filtros_sql.append("i.ano_construccion = %s")
                valores.append(filtros['ano_construccion'])

            if 'estado' in filtros and filtros['estado']:
                placeholders = ", ".join(["%s"] * len(filtros['estado']))
                filtros_sql.append(f"s.estado IN ({placeholders})")
                valores.extend(filtros['estado'])

            if filtros_sql:
                query_base += " AND " + " AND ".join(filtros_sql)

            cursor.execute(query_base, tuple(valores))
            resultados = cursor.fetchall()
            return resultados

        except Error as e:
            raise RuntimeError(f"Error en la consulta: {e}")
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
