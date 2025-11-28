class Nodo:
    def __init__(self, tipo, valor):
        self.tipo = tipo
        self.valor = valor
        self.hijos = []

    def agregar_hijo(self, hijo):
        if hijo is None:
            raise ValueError("Intentas agregar un hijo None al nodo "
                             f"{self.tipo}:{self.valor}")
        self.hijos.append(hijo)

    def __repr__(self):
        return f"{self.tipo}: {self.valor}"
