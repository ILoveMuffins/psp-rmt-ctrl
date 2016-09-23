#!/usr/bin/python

from Overrides import overrides


class CompParser(object):

    def __init__(self):
        self.index2przyciskPSP = {0: 'up', 1: 'right', 2: 'down', 3: 'left', 4: 'triangle',
                                  5: 'circle', 6: 'cross', 7: 'square', 8: 'l', 9: 'r', 10: 'start', 11: 'select'}

    def parsuj_klawisze(self, dane):
        x, y = dane[:4], dane[4:8]
        x, y = self.usun_uzupelnienie(x), self.usun_uzupelnienie(y)
        przyciskPSP2Stan = self.binary2map_przyciskPSP2stan(dane[8:])
        return int(x), int(y), przyciskPSP2Stan # TODO mozna lepiej to zrobic

    def binary2map_przyciskPSP2stan(self, dane):
        przyciskPSP2Stan = {self.index2przyciskPSP[index] : stan for index, stan in enumerate(dane)}
#maked
#        przyciskPSP2Stan = {}
#        for index, stan in enumerate(dane):
#            przycisk = self.index2przyciskPSP[index]
#            przyciskPSP2Stan[przycisk] = stan
        return przyciskPSP2Stan

    def uzupelnij_dane_do_dlugosci(self, dane, dlugosc):
        """uzupelnia string dane przez dodawanie 'A', tak aby len(dane) == dlugosc
        >>> print(CompParser().uzupelnij_dane_do_dlugosci("piwerko", 9))
        piwerkoAA
        >>> print(CompParser().uzupelnij_dane_do_dlugosci('', 5))
        AAAAA
        """
        dane = str(dane)
        dlugosc_danych = len(dane)
        dane += (dlugosc - dlugosc_danych) * 'A'
        return dane

    def usun_uzupelnienie(self, string):
        """usuwa ze stringu dodane uzupelnienie w postaci dopisanych liter 'A'
        >>> print(CompParser().usun_uzupelnienie('piwerkoAA'))
        piwerko
        """
        string = str(string)
        return string.rstrip('A')

