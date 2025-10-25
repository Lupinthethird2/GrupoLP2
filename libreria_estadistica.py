# libreria_estadistica.py
# Clase de Basee 
class Datos:
    def __init__(self, lista):
        self.lista = lista
    def cantidad(self):
        return len(self.lista)
    def mostrar(self):
        return self.lista
    def ordenar(self):
        return sorted(self.lista)