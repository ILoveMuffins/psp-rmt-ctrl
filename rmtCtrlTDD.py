#!/usr/bin/python

import unittest
from senderServ import CompParser

class TestCompParser(unittest.TestCase):

    def test_uzupelnij_dane_do_dlugosci(self):
        parser = CompParser()
        self.assertEqual(
            parser.uzupelnij_dane_do_dlugosci('bzdura', 7), 'bzduraA')
        self.assertEqual(parser.uzupelnij_dane_do_dlugosci(123, 4), '123A')
        string = "12A9AA100111001010"
        print parser.parsuj_klawisze(string)
        # with self.assertRaises(TypeError):
        # parser.uzupelnij_dane_do_dlugosci("tu powinno byc cos czego do
        # stringa sie nie da rzutowac", 9)

unittest.main()  # Calling from the command line invokes all tests

