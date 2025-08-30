import unittest
from datetime import datetime

class MeGusta:
    """Clase conceptual para representar 'me gusta'"""
    registros = []

    @classmethod
    def agregar_me_gusta(cls, usuario_id, inmueble_id):
        # Evitar duplicados
        for r in cls.registros:
            if r['usuario_id'] == usuario_id and r['inmueble_id'] == inmueble_id:
                raise ValueError("El usuario ya dio me gusta a este inmueble")
        cls.registros.append({
            'usuario_id': usuario_id,
            'inmueble_id': inmueble_id,
            'fecha_creacion': datetime.now()
        })

class TestMeGusta(unittest.TestCase):

    def setUp(self):
        MeGusta.registros = []

    def test_agregar_me_gusta(self):
        MeGusta.agregar_me_gusta(1, 100)
        self.assertEqual(len(MeGusta.registros), 1)

    def test_evitar_duplicado(self):
        MeGusta.agregar_me_gusta(1, 100)
        with self.assertRaises(ValueError):
            MeGusta.agregar_me_gusta(1, 100)

    def test_historico(self):
        MeGusta.agregar_me_gusta(1, 100)
        MeGusta.agregar_me_gusta(2, 100)
        self.assertEqual(len(MeGusta.registros), 2)

if __name__ == "__main__":
    unittest.main()
