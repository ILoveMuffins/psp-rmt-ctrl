#!/usr/bin/python

def overrides(interface_class):
    """ metoda globala sluzaca do sygnalizowania dziedziczenia
        jesli jakas metoda nadpisuje metode klasy podstawowej to umieszczamy nad nia @overrides(base_class_name)
    """
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider
