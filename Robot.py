#!/usr/bin/python

from Overrides import overrides
from pymouse import PyMouse
from pykeyboard import PyKeyboard

class Robot(object):

    def __init__(self):
        self.mouse = PyMouse()
        self.keyboard = PyKeyboard()
        self.przyciskPSP2klawiatura = {'up': 'w', 'right': 'd', 'down': 's', 'left': 'a', 'triangle': self.keyboard.enter_key,
                                       'circle': 'f', 'cross': 'g', 'square': 'h', 'l': self.keyboard.control_r_key, 'r': self.keyboard.shift_r_key, 'start': 'k', 'select': 'l'}

    def reaguj(self, x, y, przyciskPSP2Stan):
        self.reaguj_mysz(x, y)
        self.reaguj_klawiatura(przyciskPSP2Stan)

    def reaguj_mysz(self, x, y):
        max_predkosc_kursora = 0.00000000000000000000000000000000000000000000000000001

        # obecne polozenie myszy skoryguj o wychylenie analoga * jak szybko
        # zakres galki analogowej [-127, 128]
        x += int((x / float(128)) * max_predkosc_kursora +
                 self.mouse.position()[0])
        y += int((y / float(128)) * max_predkosc_kursora +
                 self.mouse.position()[1])
        #print "stare x: ", self.mouse.position()[0], " stare y: ", self.mouse.position()[1]
        #print "nowe  x: ", x, " nowe y: ", y
        # jesli mysz na krawedzi ekranu to nie przesuwaj jej dalej
        x, y = min(self.mouse.screen_size()[0], x), min(
            self.mouse.screen_size()[1], y)
        x, y = max(0, x), max(0, y)
        self.mouse.move(x, y)

    def reaguj_klawiatura(self, przyciskPSP2Stan):
        for przycisk_psp, czyWcisniety in przyciskPSP2Stan.iteritems():
            przycisk_klawiaturowy = self.przyciskPSP2klawiatura[przycisk_psp]
            if czyWcisniety == '1':
                if przycisk_klawiaturowy == 'g':
                    self.mouse.click(*self.mouse.position())
                    break
                self.keyboard.press_key(przycisk_klawiaturowy)
            else:
                self.keyboard.release_key(przycisk_klawiaturowy)

