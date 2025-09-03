import mysql.connector
from mysql.connector import Error
from config_bd import BD_CONFIG

# Estados válidos por su nombre
ESTADOS_VALIDOS = ["pre_venta", "en_venta", "vendido"]

class BaseDeDatos:
    def __init__(self):
        self.config = BD_CONFIG

    def conectar(self):
        """Establece la conexión con la base de datos."""
        try:
            conexion = mysql.connector.connect(**self.config)
            return conexion
        except Error as e:
            raise ConnectionError(f"Error al conectarse a la base de datos: {e}")

    def obtener_inmuebles(self, filtros):
        """
        Obtiene propiedades con su último estado disponible,
        aplicando filtros opcionales por ciudad, año de construcción y estado.
        """
        # --- Validaciones de tipos ---
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

            # --- Consulta base con JOIN a status ---
            query_base = """
                SELECT 
                    p.id AS property_id, 
                    p.address, 
                    p.city, 
                    p.price, 
                    p.year, 
                    st.name AS status_name,
                    st.label AS status_label,
                    sh.update_date
                FROM property p
                INNER JOIN (
                    SELECT 
                        property_id, 
                        status_id, 
                        update_date
                    FROM (
                        SELECT 
                            property_id,
                            status_id,
                            update_date,
                            ROW_NUMBER() OVER (
                                PARTITION BY property_id 
                                ORDER BY update_date DESC, status_id DESC
                            ) AS rn
                        FROM status_history
                    ) ranked
                    WHERE rn = 1
                ) sh 
                    ON p.id = sh.property_id
                INNER JOIN status st 
                    ON sh.status_id = st.id
                WHERE 1=1
            """

            filtros_sql = []
            valores = []

            # --- Filtros dinámicos ---
            if 'ciudad' in filtros and filtros['ciudad']:
                filtros_sql.append("p.city = %s")
                valores.append(filtros['ciudad'])

            if 'ano_construccion' in filtros and filtros['ano_construccion']:
                filtros_sql.append("p.year = %s")
                valores.append(filtros['ano_construccion'])

            if 'estado' in filtros and filtros['estado']:
                placeholders = ", ".join(["%s"] * len(filtros['estado']))
                filtros_sql.append(f"st.name IN ({placeholders})")
                valores.extend(filtros['estado'])

            # Agregar filtros a la consulta si existen
            if filtros_sql:
                query_base += " AND " + " AND ".join(filtros_sql)

            query_base += " ORDER BY p.id"

            # --- Ejecutar consulta ---
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
