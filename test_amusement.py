from unittest import TestCase

import Folke_Bengtsson_3.Folke_Bengtsson_3 as fb3


class TestAmusement(TestCase):
    def setUp(self):
        self.amusement = fb3.Amusement()

    def test_register_options(self): pass

    def test_has_option(self): pass

    def test_fear_factor(self):
        am = self.amusement
        am.fear_factor()
        print(am)

    def test_permit_riders(self):
        am = self.amusement
        # print(am.permit_riders(120))


import unittest

if __name__ == '__main__':
    unittest.main()
