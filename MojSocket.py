#!/usr/bin/python

import socket
from threading import RLock

from Overrides import overrides


class MojSocket(object):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.unbind = True
        self.sock = socket.socket()

    def stworz_serwer(self):
        if self.unbind:
            self.unbind = False
            self.sock.bind((self.host, self.port))
            self.sock.listen(1)
            self.sock, addr = self.sock.accept()
        else:
            raise RuntimeError("Socket is closed")

    def stworz_klienta(self):
        if self.unbind:
            self.unbind = False
            self.sock.connect((self.host, self.port))
        else:
            raise RuntimeError("Socket is closed")

    def otrzymaj_dane(self, ile):
        odebrane = self.sock.recv(ile)
        while len(odebrane) < ile:
            odebrane += self.sock.recv(ile - len(odebrane))
        return odebrane

    def wyslij(self, informacja):
        self.sock.send(informacja)

    def wyslij_plik(self, nazwa_pliku):
        with open(nazwa_pliku, 'rb') as plik:
            bufor = plik.read(131072)
            while bufor != '':
                self.sock.send(bufor)
                bufor = plik.read(131072)

    def zamknij(self):
        lock = RLock()
        with lock:
            if not self.unbind:
                self.unbind = True
                self.sock.close()

