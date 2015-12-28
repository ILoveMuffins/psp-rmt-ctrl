#!/usr/bin/python

import time
import logging
from CompParser import CompParser
from MojSocket import MojSocket
from Robot import Robot
from threading import Thread

import os
if os.name == 'posix':
    from PrintScreenLinux import stworz_plik_do_wyslania
elif os.name == 'nt':
    from PrintScreenWindows import stworz_plik_do_wyslania
else:
    raise OSError('Niewspierany system operacyjny')

dzialaj = True

def main():
    global dzialaj
    # dzialaj zatrzymuje oba watki, ale wznawianie polaczenia ma trwac caly
    # czas
    while True:
        try:
            sock = MojSocket('192.168.1.12', 2314) #domowy
            #sock = MojSocket('192.168.0.4', 2314) # mieszkaniowy
            # tworzenie socketu musi byc tutaj ! ; ABY ZATRZYMAC PROGRAM PRZYTRZYMAJ ^C -
            # poleci excep w finally
            sock.stworz_serwer()
            sluchacz_thr = utworz_watek_sluchacza(sock)
            nadawacz_thr = utworz_watek_nadawacza(sock)
            sluchacz_thr.join()
            nadawacz_thr.join()
        except KeyboardInterrupt as err:
            logging.warning('keyboardInterrupt' + ' --> ' + repr(err))
            break
        except Exception as err:
            logging.critical(' -- ' + repr(err))
        # niestety nie mozna skorzystac z zalecenia i uzyc else, bo wyjatek
        # moze wystapic w trakcie czekania (join) na watek
        finally:
            dzialaj = False
            # chodzi o to by drugi watek spostrzegl dzialaj == False
            time.sleep(0.2)
            sock.zamknij()


def utworz_watek_sluchacza(sock):
    sluchacz_thr = Thread(target=sluchaj_wejscie_z_gniazda, args=(sock,))
    sluchacz_thr.setDaemon(True)
    sluchacz_thr.start()
    return sluchacz_thr


def utworz_watek_nadawacza(sock):
    nadawacz_thr = Thread(target=nadawaj_do_gniazda, args=(sock,))
    # czemu nie False, przeciez moze nasluchiwac nawet jak klient sie odczepi
    # -o ile nie przerwie to polaczenia
    nadawacz_thr.setDaemon(True)
    nadawacz_thr.start()
    return nadawacz_thr


def sluchaj_wejscie_z_gniazda(sock): # thread
    parser = CompParser()
    robot = Robot()
    global dzialaj
    while dzialaj:
        odebrane_dane = sock.otrzymaj_dane(ile=20)
        print odebrane_dane
        x, y, przyciskPSP2Stan = parser.parsuj_klawisze(dane=odebrane_dane)
        robot.reaguj(int(x), int(y), przyciskPSP2Stan)
        # krotszy niz na psp ; 50razy/sek cos odczytam; ale w pesymistycznym
        # przypadku tylko 25 razy na sek ;/
        time.sleep(0.002)


def nadawaj_do_gniazda(sock): # thread
    parser = CompParser()
    global dzialaj
    while dzialaj:
        waga_pliku = stworz_plik_do_wyslania()  # zrobic cos z tym(klase?)
        dane = parser.uzupelnij_dane_do_dlugosci(
            waga_pliku, dlugosc=6)  # usun hardcode (6)
        sock.wyslij(dane)
        sock.wyslij_plik('prtscr.jpeg')  # usun hardcode
        # time.sleep(0.02) #tcp nie pozwala pakietom ginac, pytanie czy bez tej
        # linii procesor sie meczy

if __name__ == '__main__':
    #import doctest
    # automatycznie wykonuje testy zawarte w docstringach funkcji, np. w fun.
    # uzupelnij_dane_do_dlugosci
    #doctest.testmod()
    main()

