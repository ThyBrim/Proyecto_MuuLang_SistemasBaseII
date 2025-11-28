class SymbolTable:
    def __init__(self):
        self.tabla = {}

    def declarar(self, nombre, tipo):
        if nombre in self.tabla:
            raise Exception(f"Error semántico: la variable '{nombre}' ya fue declarada.")
        self.tabla[nombre] = tipo

    def asignar(self, nombre, tipo):
        if nombre not in self.tabla:
            raise Exception(f"Error semántico: la variable '{nombre}' no está declarada.")

        if self.tabla[nombre] != tipo:
            raise Exception(f"Error semántico: tipo incompatible al asignar a '{nombre}'.")

    def obtener(self, nombre):
        if nombre not in self.tabla:
            raise Exception(f"Error semántico: variable '{nombre}' no existe.")
        return self.tabla[nombre]
