import unittest
import sys
import os

# Esto soluciona el error de "No module named librerias"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from librerias import libreria as lib

class TestVentas(unittest.TestCase):

    def test_calculo_iva(self):
        """Valida el cálculo correcto del IVA (10%)."""
        # Si algo cuesta 100€, el IVA es 10€ y el total 110€
        sub, iva, total = lib.calcular_totales([100.0])
        self.assertEqual(iva, 10.0)
        self.assertEqual(total, 110.0)

    def test_total_vacio(self):
        """Comprueba que si no hay productos, el total es 0."""
        sub, iva, total = lib.calcular_totales([])
        self.assertEqual(total, 0)

if __name__ == '__main__':
    unittest.main()
