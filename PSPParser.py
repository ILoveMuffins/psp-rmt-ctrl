#-*- coding: ISO-8859-1 -*-

from Overrides import overrides

class PSPParser(object):

    def parsuj_klawisze(self, dane):
        x, y, przyciski = dane[:3], dane[3:6], dane[6]
        x, y = self.usun_uzupelnienie(x), self.usun_uzupelnienie(y)
        return x, y, przyciski # TODO mozna lepiej

    def uzupelnij_dane_do_dlugosci(self, dane, dlugosc):
        dane = str(dane)
        dlugosc_danych = len(dane)
        dane += (dlugosc - dlugosc_danych) * 'A'
        return dane

    def usun_uzupelnienie(self, string):
        string = str(string)
        return string.rstrip('A')

