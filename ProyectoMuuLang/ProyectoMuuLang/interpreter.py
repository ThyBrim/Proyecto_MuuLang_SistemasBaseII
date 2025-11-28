from nodo import Nodo


class Interpreter:
    def __init__(self):
        self.variables = {}

    def ejecutar(self, nodo):
        metodo = getattr(self, f"ej_{nodo.tipo}", None)
        if metodo is None:
            raise Exception(f"No existe ejecutor para nodo: {nodo.tipo}")
        return metodo(nodo)


    def ej_programa(self, nodo):
        instrucciones = nodo.hijos[0]
        self.ej_instrucciones(instrucciones)

    def ej_instrucciones(self, nodo):
        for hijo in nodo.hijos:
            self.ejecutar(hijo)

    def ej_declaracion(self, nodo):
        nombre = nodo.hijos[0].valor
        valor = self.evaluar(nodo.hijos[1])
        self.variables[nombre] = valor


    def ej_asignacion(self, nodo):
        nombre = nodo.hijos[0].valor
        valor = self.evaluar(nodo.hijos[1])
        self.variables[nombre] = valor

    def ej_impresion(self, nodo):
        hijo = nodo.hijos[0]
        if hijo.tipo == "cadena":
            print(hijo.valor.strip('"'))
        else:
            print(self.evaluar(hijo))

    def ej_mientras(self, nodo):
        condicion = nodo.hijos[0]
        instrucciones = nodo.hijos[1]

        while self.evaluar(condicion):
            self.ej_instrucciones(instrucciones)


    def ej_si(self, nodo):
        condicion = nodo.hijos[0]
        instrucciones_si = nodo.hijos[1]

        # Tiene bloque sino?
        tiene_sino = len(nodo.hijos) == 3

        if self.evaluar(condicion):
            self.ej_instrucciones(instrucciones_si)
        else:
            if tiene_sino:
                instrucciones_sino = nodo.hijos[2]
                self.ej_instrucciones(instrucciones_sino)

    def ej_para(self, nodo):
        nombre = nodo.hijos[0].valor
        inicio = self.evaluar(nodo.hijos[1])
        fin = self.evaluar(nodo.hijos[2])
        instrucciones = nodo.hijos[3]

        self.variables[nombre] = inicio

        while self.variables[nombre] < fin:
            self.ej_instrucciones(instrucciones)
            self.variables[nombre] += 1

    def evaluar(self, nodo):

        if nodo.tipo == "numero":
            return float(nodo.valor) if "." in nodo.valor else int(nodo.valor)

        if nodo.tipo == "identificador":
            if nodo.valor not in self.variables:
                raise Exception(f"Variable no definida: {nodo.valor}")
            return self.variables[nodo.valor]


        if nodo.tipo == "op":
            izq = self.evaluar(nodo.hijos[0])
            der = self.evaluar(nodo.hijos[1])
            op = nodo.valor

            if op == "+": return izq + der
            if op == "-": return izq - der
            if op == "*": return izq * der
            if op == "/": return izq / der


        if nodo.tipo == "comparacion":
            izq = self.evaluar(nodo.hijos[0])
            der = self.evaluar(nodo.hijos[1])
            op = nodo.valor

            if op == "<": return izq < der
            if op == ">": return izq > der
            if op == "<=": return izq <= der
            if op == ">=": return izq >= der
            if op == "==": return izq == der
            if op == "!=": return izq != der

        raise Exception(f"No se puede evaluar nodo: {nodo.tipo}")
