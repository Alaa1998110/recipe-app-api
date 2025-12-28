from . import calc
from django.test import SimpleTestCase

class CalcTests(SimpleTestCase):

    def test_add_numbers(self):
        result = calc.add(1,2)
        self.assertEqual(result,3)
