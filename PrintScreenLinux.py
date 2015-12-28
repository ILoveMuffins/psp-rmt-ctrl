#!/usr/bin/python

#For cross platform compatibility, a person may be best off with using the wxPython library.
#http://wiki.wxpython.org/WorkingWithImages#A_Flexible_Screen_Capture_App
#w pliku senderServer musimy tez rozrozniac windows / linux i importowac stad opowiednia funkcje
# mozna tez - PIL - jest cross platform
#from PIL import ImageGrab
#im = ImageGrab.grab()
#im.save('screenshot.png')

"""
import win32gui
import win32ui
hwnd = win32gui.FindWindow(None, windowname)
wDC = win32gui.GetWindowDC(hwnd)
dcObj=win32ui.CreateDCFromHandle(wDC)
cDC=dcObj.CreateCompatibleDC()
dataBitMap = win32ui.CreateBitmap()
dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
cDC.SelectObject(dataBitMap)
cDC.BitBlt((0,0),(w, h) , dcObj, (0,0), win32con.SRCCOPY)
dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)
# Free Resources
dcObj.DeleteDC()
cDC.DeleteDC()
win32gui.ReleaseDC(hwnd, wDC)
win32gui.DeleteObject(dataBitMap.GetHandle())
"""

from ZrzutEkranuException import ZrzutEkranuException
import gtk.gdk
import os

def stworz_plik_do_wyslania(nazwa_pliku='prtscr.jpeg'):
    zrzut_ekranu = get_zrzut_ekranu()
    width, height, typ_pliku, jakosc = 480, 272, 'jpeg', '30'
    zrzut_ekranu = zrzut_ekranu.scale_simple(
        width, height, gtk.gdk.INTERP_BILINEAR)
    zrzut_ekranu.save(nazwa_pliku, typ_pliku, {'quality': jakosc})
    waga_pliku = os.path.getsize(nazwa_pliku)
    return waga_pliku


def get_zrzut_ekranu():
    w = gtk.gdk.get_default_root_window()
    sz = w.get_size()
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, False, 8, sz[0], sz[1])
    pb = pb.get_from_drawable(w, w.get_colormap(), 0, 0, 0, 0, sz[0], sz[1])
    if (pb == None):
        raise ZrzutEkranuException("Nie udalo sie dokonac zrzutu ekranu")
    return pb

