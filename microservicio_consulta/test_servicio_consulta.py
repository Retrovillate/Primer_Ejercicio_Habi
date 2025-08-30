import unittest
from bd_habi import BaseDeDatos, ESTADOS_VALIDOS

class TestServicioConsulta(unittest.TestCase):

    def setUp(self):
        self.bd = BaseDeDatos()

    def test_filtro_ciudad_valido(self):
        filtros = {"ciudad": "Bogotá"}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertEqual(r['ciudad'], "Bogotá")

    def test_filtro_ano_construccion_valido(self):
        filtros = {"ano_construccion": 2018}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertEqual(r['ano_construccion'], 2018)

    def test_filtro_estado_valido(self):
        filtros = {"estado": ["pre_venta", "en_venta"]}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertIn(r['estado'], ["pre_venta", "en_venta"])

    def test_filtros_combinados(self):
        filtros = {"ciudad": "Bogotá", "ano_construccion": 2018, "estado": ["pre_venta"]}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertEqual(r['ciudad'], "Bogotá")
            self.assertEqual(r['ano_construccion'], 2018)
            self.assertEqual(r['estado'], "pre_venta")

    def test_estado_invalido(self):
        filtros = {"estado": ["invalid_estado"]}
        with self.assertRaises(ValueError):
            self.bd.obtener_inmuebles(filtros)

    def test_tipo_ciudad_invalido(self):
        filtros = {"ciudad": 123}
        with self.assertRaises(TypeError):
            self.bd.obtener_inmuebles(filtros)

    def test_tipo_ano_construccion_invalido(self):
        filtros = {"ano_construccion": "2018"}
        with self.assertRaises(TypeError):
            self.bd.obtener_inmuebles(filtros)

    def test_tipo_estado_invalido(self):
        filtros = {"estado": "pre_venta"}
        with self.assertRaises(TypeError):
            self.bd.obtener_inmuebles(filtros)

    def test_sin_filtros(self):
        filtros = {}
        resultados = self.bd.obtener_inmuebles(filtros)
        self.assertIsInstance(resultados, list)

    def test_resultado_con_campos_correctos(self):
        filtros = {"ciudad": "Bogotá"}
        resultados = self.bd.obtener_inmuebles(filtros)
        for r in resultados:
            self.assertIn("direccion", r)
            self.assertIn("ciudad", r)
            self.assertIn("estado", r)
            self.assertIn("precio_venta", r)
            self.assertIn("descripcion", r)

if __name__ == "__main__":
    unittest.main()
