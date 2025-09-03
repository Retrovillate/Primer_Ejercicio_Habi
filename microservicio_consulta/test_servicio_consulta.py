import unittest
from bd_habi import BaseDeDatos, ESTADOS_VALIDOS

class TestServicioConsulta(unittest.TestCase):

    def setUp(self):
        # Se ejecuta antes de cada test para inicializar la conexión a la base de datos
        self.bd = BaseDeDatos()

    # --- PRUEBAS DE FILTROS INDIVIDUALES ---

    def test_filtro_ciudad_valido(self):
        """Verifica que filtrar por ciudad retorna solo inmuebles en esa ciudad."""
        filtros = {"ciudad": "bogota"}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertEqual(r['city'], "bogota")

    def test_filtro_ano_construccion_valido(self):
        """Verifica que filtrar por año de construcción funciona correctamente."""
        filtros = {"ano_construccion": 2018}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertEqual(r['year'], 2018)

    def test_filtro_estado_valido(self):
        """Verifica que filtrar por estado retorna solo estados válidos."""
        filtros = {"estado": ["pre_venta", "en_venta"]}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertIn(r['status_name'], ["pre_venta", "en_venta"])

    # --- PRUEBA DE FILTROS COMBINADOS ---

    def test_filtros_combinados(self):
        """Verifica que múltiples filtros aplicados simultáneamente funcionen."""
        filtros = {"ciudad": "bogota", "ano_construccion": 2018, "estado": ["pre_venta"]}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertEqual(r['city'], "bogota")
            self.assertEqual(r['year'], 2018)
            self.assertEqual(r['status_name'], "pre_venta")

    # --- PRUEBAS DE VALIDACIONES DE DATOS ---

    def test_estado_invalido(self):
        """Debe lanzar ValueError si se pasa un estado no permitido."""
        filtros = {"estado": ["invalid_estado"]}
        with self.assertRaises(ValueError):
            self.bd.obtener_inmuebles(filtros)

    def test_tipo_ciudad_invalido(self):
        """Debe lanzar TypeError si ciudad no es cadena de texto."""
        filtros = {"ciudad": 123}
        with self.assertRaises(TypeError):
            self.bd.obtener_inmuebles(filtros)

    def test_tipo_ano_construccion_invalido(self):
        """Debe lanzar TypeError si año de construcción no es entero."""
        filtros = {"ano_construccion": "2018"}
        with self.assertRaises(TypeError):
            self.bd.obtener_inmuebles(filtros)

    def test_tipo_estado_invalido(self):
        """Debe lanzar TypeError si estado no es lista (ej: string en vez de lista)."""
        filtros = {"estado": "pre_venta"}
        with self.assertRaises(TypeError):
            self.bd.obtener_inmuebles(filtros)

    # --- PRUEBAS DE CASOS ESPECIALES ---

    def test_sin_filtros(self):
        """Si no se envían filtros, la consulta debe funcionar y retornar lista."""
        filtros = {}
        resultados = self.bd.obtener_inmuebles(filtros)
        self.assertIsInstance(resultados, list)

    def test_resultado_con_campos_correctos(self):
        """Verifica que los registros retornados contengan todos los campos esperados."""
        filtros = {"ciudad": "bogota"}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertIn("address", r)
            self.assertIn("city", r)
            self.assertIn("status_name", r)
            self.assertIn("price", r)
            self.assertIn("status_label", r)
            self.assertIn("year", r)
            self.assertIn("update_date", r)

    def test_filtros_sin_resultados(self):
        """Si el filtro no coincide con ningún registro, debe retornar lista vacía."""
        filtros = {"ciudad": "ciudad_inexistente"}
        resultados = self.bd.obtener_inmuebles(filtros)
        self.assertEqual(resultados, [])

    def test_filtros_parcialmente_vacios(self):
        """Si un filtro está vacío (''), no debe romper la consulta y aplica los demás."""
        filtros = {"ciudad": "", "ano_construccion": 2018}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertEqual(r['year'], 2018)

    def test_ciudad_case_insensitive(self):
        """Verifica que la búsqueda por ciudad no dependa de mayúsculas/minúsculas."""
        filtros = {"ciudad": "BoGoTa"}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertEqual(r['city'].lower(), "bogota")

    def test_estado_lista_vacia(self):
        """Debe lanzar ValueError si se pasa una lista de estado vacía."""
        filtros = {"estado": []}
        with self.assertRaises(ValueError):
            self.bd.obtener_inmuebles(filtros)

    def test_tipos_incorrectos_combinados(self):
        """Debe lanzar TypeError si múltiples filtros son inválidos al mismo tiempo."""
        filtros = {"ciudad": 123, "ano_construccion": "2018", "estado": ["pre_venta"]}
        with self.assertRaises(TypeError):
            self.bd.obtener_inmuebles(filtros)


if __name__ == "__main__":
    unittest.main()
