#-*- coding: ISO-8859-1 -*-
from __future__ import with_statement

import pspnet
import psp2d
import pspos
import stackless
import urlparse
import os
import socket
import time
# watki stackless bylyby dla psp lzejsze
from threading import Thread
from threading import RLock
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from MojSocket import MojSocket
from PSPParser import PSPParser
# import cProfile, pstats, StringIO

# przycisk psp moglby modyfikowac te wartosci, zmieniac je na inne
# ustawienia zegara
pspos.setclocks(333, 166)
dzialaj = True
##########################################################################
# nie moj kod, do przeanalizowania
# !!!!!!!!!!!!!!!! to prawdopodobnie nie jest potrzebne bo stawia serwer HTTP 192.168.1.13:80 w przegladarce zobacz
# dlatego aby polaczyc sie z ruterem wystarczy connectToAPCTL(1, cb)


class MSHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            path = 'ms0:' + urlparse.urlparse(self.path)[2]
            file('log.txt', 'a+').write('Request: %s (%s)\n' %
                                        (self.path, path))
            if path != 'ms0:/' and not os.path.exists(path):
                self.send_response(404)
                self.end_headers()
            elif os.path.isdir(path) or path == 'ms0:/':
                self.send_response(200)
                html = '<html><head><title>Directory listing for %s</title></head><body>' % path
                html += '<h1>Directories</h1><ul>'
                for name in os.listdir(path):
                    if name != '.':
                        fname = os.path.join(path, name)
                        if os.path.isdir(fname):
                            html += '<li><a href="%s">%s</a></li>' % (
                                fname[4:], name)
                html += '</ul><h1>Files</h1><ul>'
                for name in os.listdir(path):
                    fname = os.path.join(path, name)
                    if os.path.isfile(fname):
                        html += '<li><a href="%s">%s</a></li>' % (
                            fname[4:], name)

                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', str(len(html)))
                self.end_headers()
                self.wfile.write(html)
            elif os.path.isfile(path):
                sz = os.path.getsize(path)
                self.send_response(200)
                self.send_header('Content-Type', 'octet/stream')  # TODO: guess
                self.send_header('Content-Length', str(sz))
                self.end_headers()

                fp = file(path, 'rb')
                bf = fp.read(4096)
                while bf:
                    self.wfile.write(bf)
                    bf = fp.read(4096)
                fp.close()
            else:
                self.send_response(400)
                html = '<html><head><title>Error</title></head><body>'
                html += 'Bad request (%s)' % path
                self.send_header('Content-Type', 'text/html')
                self.send_header('Content-Length', str(len(html)))
                self.end_headers()
                self.wfile.write(html)
        except:
            import traceback
            traceback.print_exc(file=file('trace.txt', 'a+'))

    def log_message(self, fmt, *args):
        file('messages.txt', 'a+').write((fmt % args) + '\n')


class MSServer(HTTPServer):
    allow_reuse_address = True
##########################################################################

def main():
    pspnet.connectToAPCTL(1, cb)  # rozkmin
    thr = utworz_jakis_watek()  # rozkmin
    global dzialaj
    try:
        sock = MojSocket('192.168.1.12', 2314)
        sock.stworz_klienta()
        sluchacz_thr = utworz_watek_sluchacza(sock)
        nadawacz_thr = utworz_watek_nadawacza(sock)
        sluchacz_thr.join()
        nadawacz_thr.join()
    finally:
        dzialaj = False
        time.sleep(0.1)
        sock.zamknij()
        pspnet.disconnectAPCTL()  # with lock?


def cb(s):
    screen = psp2d.Screen()
    font = psp2d.Font('font.png')
    if s >= 0:
        font.drawText(screen, 0, 0, 'State: %d/4' % s)
    else:
        font.drawText(screen, 0, 20, 'Connected. IP: %s' % pspnet.getIP())
    screen.swap()


def utworz_jakis_watek():
    srv = MSServer(('', 80), MSHandler)
    thr = Thread(target=srv.serve_forever)
    thr.setDaemon(True)
    thr.start()
    return thr


def utworz_watek_sluchacza(sock):
    sluchacz_thr = Thread(target=sluchacz, args=(sock,))
    sluchacz_thr.setDaemon(True)
    sluchacz_thr.start()
    return sluchacz_thr


def utworz_watek_nadawacza(sock):
    nadawacz_thr = Thread(target=nadawacz, args=(sock,))
    nadawacz_thr.setDaemon(True)
    nadawacz_thr.start()
    return nadawacz_thr


def sluchacz(sock):  # thread
    font = psp2d.Font('font.png')
    parser = PSPParser()
    global dzialaj
    while dzialaj:
        waga_wiadomosci = sock.otrzymaj_dane(ile=6)
        # zmien nazwe usun_uzupelnienie, by rzutow. int zawrzec w metodzie
        waga_wiadomosci = int(parser.usun_uzupelnienie(waga_wiadomosci))
        bufor = sock.otrzymaj_dane(ile=waga_wiadomosci)
        with open('prtscr.jpeg', 'wb') as plik:
            plik.write(bufor)
        odrysuj_na_ekranie(obrazek='prtscr.jpeg')
        # time.sleep(0.02) #tcp ip nie traci pakietow, ale bedzie mniej baterii
        # uzywac


def odrysuj_na_ekranie(obrazek):
    screen = psp2d.Screen()
    image = psp2d.Image(obrazek)
    screen.blit(image)
    screen.swap()


def nadawacz(sock):  # thread
    global dzialaj
    while dzialaj:
        stan_przyciskow = pobierz_stan_przyciskow()
        sock.wyslij(stan_przyciskow)
        time.sleep(0.01)


def pobierz_stan_przyciskow():
    parser = PSPParser()
    pad = psp2d.Controller()
    rtn = parser.uzupelnij_dane_do_dlugosci(pad.analogX, dlugosc=4)
    rtn += parser.uzupelnij_dane_do_dlugosci(pad.analogY, dlugosc=4)
    stan_przyciskow = [pad.up, pad.right, pad.down, pad.left, pad.triangle,
                       pad.circle, pad.cross, pad.square, pad.l, pad.r, pad.start, pad.select]
    for stan in stan_przyciskow:
        rtn += to_string(stan)

    return rtn

    #result_list = map(lambda stan: '1' if stan else '0', stan_przyciskow) #map zwroci mi liste czy generator? bo to nie dziala
    #return ''.join(result_list)

    #mozna tez tak pomyslec:
    # if pad.cross:
    #	struktura.cross = True #bool zajmuje 1 bit, jak to odczytywac
    # trzeba dokladnie znac wage struktury i tyle bajtow czytac w serwerze
    # socket wysyla tylko string, jak wyslac strukture... ; i czy warto, czy
    # to wlasciwe rozwiazanie

def to_string(stan):
    if stan == True:
        return '1'
    else:
        return '0'

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except:
        import traceback
        traceback.print_exc(file=file('trace.txt', 'a+'))

