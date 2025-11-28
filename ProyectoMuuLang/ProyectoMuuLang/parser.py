from nodo import Nodo

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0


    def actual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("EOF", "")

    def avanzar(self):
        self.pos += 1

    def coincidir(self, tipo_esperado):
        tipo, valor = self.actual()
        if tipo == tipo_esperado:
            self.avanzar()
            return valor
        else:
            raise SyntaxError(f"Se esperaba {tipo_esperado}, pero llegó {tipo} ('{valor}')")


    def analizar(self):
        nodo = self.programa()
        return nodo

    def programa(self):
        if self.actual()[1] != "establo":
            raise SyntaxError("El programa debe iniciar con 'establo'")

        self.coincidir("PALABRA_CLAVE")  # establo
        nodo_prog = Nodo("programa", "establo")

        instrucciones = self.instrucciones()
        nodo_prog.agregar_hijo(instrucciones)

        if self.actual()[1] != "fin_establo":
            raise SyntaxError("El programa debe finalizar con 'fin_establo'")

        self.coincidir("PALABRA_CLAVE")
        return nodo_prog


    def instrucciones(self):
        nodo = Nodo("instrucciones", "")
        while True:
            tipo, valor = self.actual()

            if valor in ("fin_establo", "fin_mientras", "fin_para", "fin_si"):
                break

            nodo_ins = self.instruccion()
            nodo.agregar_hijo(nodo_ins)

        return nodo

    def instruccion(self):
        tipo, valor = self.actual()

        if valor == "vaca":
            return self.declaracion()

        elif valor == "muu":
            return self.impresion()

        elif valor == "si":
            return self.condicional()

        elif valor == "mientras":
            return self.bucle_mientras()

        elif valor == "para":
            return self.bucle_para()

        elif tipo == "IDENTIFICADOR":
            return self.asignacion()

        elif valor == "mientras":
            return self.bucle_mientras()


        else:
            raise SyntaxError(f"Instrucción inválida: {valor}")

    def declaracion(self):
        self.coincidir("PALABRA_CLAVE")
        nombre = self.coincidir("IDENTIFICADOR")
        self.coincidir("ASIGNACION")
        expr = self.expresion()
        self.coincidir("DELIMITADOR")

        nodo = Nodo("declaracion", "vaca")
        nodo.agregar_hijo(Nodo("identificador", nombre))
        nodo.agregar_hijo(expr)
        return nodo

    def asignacion(self):
        nombre = self.coincidir("IDENTIFICADOR")
        self.coincidir("ASIGNACION")
        expr = self.expresion()
        self.coincidir("DELIMITADOR")

        nodo = Nodo("asignacion", "=")
        nodo.agregar_hijo(Nodo("identificador", nombre))
        nodo.agregar_hijo(expr)
        return nodo

    def impresion(self):
        self.coincidir("PALABRA_CLAVE")
        tipo, valor = self.actual()

        nodo = Nodo("impresion", "muu")

        if tipo == "CADENA":
            nodo.agregar_hijo(Nodo("cadena", valor))
            self.coincidir("CADENA")
        elif tipo == "IDENTIFICADOR":
            nodo.agregar_hijo(Nodo("identificador", valor))
            self.coincidir("IDENTIFICADOR")
        else:
            raise SyntaxError("Se esperaba cadena o identificador después de 'muu'.")

        self.coincidir("DELIMITADOR")
        return nodo

    def condicional(self):
        self.coincidir("PALABRA_CLAVE")  # si

        condicion = self.comparacion()
        self.coincidir("DELIMITADOR")

        nodo_si = Nodo("si", "si")
        nodo_si.agregar_hijo(condicion)

        instrucciones_si = self.instrucciones()
        nodo_si.agregar_hijo(instrucciones_si)

        if self.actual()[1] == "sino":
            self.coincidir("PALABRA_CLAVE")
            self.coincidir("DELIMITADOR")

            instrucciones_sino = self.instrucciones()
            nodo_si.agregar_hijo(instrucciones_sino)

        if self.actual()[1] != "fin_si":
            raise SyntaxError("Se esperaba 'fin_si'")

        self.coincidir("PALABRA_CLAVE")
        self.coincidir("DELIMITADOR")

        return nodo_si

    def bucle_mientras(self):
        self.coincidir("PALABRA_CLAVE")  # mientras

        condicion = self.comparacion()
        self.coincidir("DELIMITADOR")

        nodo = Nodo("mientras", "mientras")
        nodo.agregar_hijo(condicion)

        instrucciones = self.instrucciones()
        nodo.agregar_hijo(instrucciones)

        if self.actual()[1] != "fin_mientras":
            raise SyntaxError("Se esperaba 'fin_mientras'")

        self.coincidir("PALABRA_CLAVE")
        self.coincidir("DELIMITADOR")

        return nodo


    def bucle_para(self):
        self.coincidir("PALABRA_CLAVE")  # para
        self.coincidir("PALABRA_CLAVE")  # vaca

        nombre = self.coincidir("IDENTIFICADOR")
        self.coincidir("ASIGNACION")
        inicio = self.expresion()
        self.coincidir("PALABRA_CLAVE")  # hasta
        fin = self.expresion()
        self.coincidir("DELIMITADOR")

        nodo = Nodo("para", "para")
        nodo.agregar_hijo(Nodo("identificador", nombre))
        nodo.agregar_hijo(inicio)
        nodo.agregar_hijo(fin)

        instrucciones = self.instrucciones()
        nodo.agregar_hijo(instrucciones)

        if self.actual()[1] != "fin_para":
            raise SyntaxError("Se esperaba 'fin_para'")

        self.coincidir("PALABRA_CLAVE")
        self.coincidir("DELIMITADOR")

        return nodo

    def expresion(self):
        return self.suma_resta()

    def suma_resta(self):
        nodo = self.termino()
        while self.actual()[1] in ("+", "-"):
            op = self.actual()[1]
            self.avanzar()
            nodo2 = self.termino()
            op_node = Nodo("op", op)
            op_node.agregar_hijo(nodo)
            op_node.agregar_hijo(nodo2)
            nodo = op_node
        return nodo

    def termino(self):
        nodo = self.factor()
        while self.actual()[1] in ("*", "/"):
            op = self.actual()[1]
            self.avanzar()
            nodo2 = self.factor()
            op_node = Nodo("op", op)
            op_node.agregar_hijo(nodo)
            op_node.agregar_hijo(nodo2)
            nodo = op_node
        return nodo

    def factor(self):
        tipo, valor = self.actual()
        if tipo == "NUMERO":
            self.avanzar()
            return Nodo("numero", valor)
        elif tipo == "IDENTIFICADOR":
            self.avanzar()
            return Nodo("identificador", valor)
        elif valor == "(":
            self.coincidir("DELIMITADOR")
            nodo = self.expresion()
            self.coincidir("DELIMITADOR")
            return nodo
        else:
            raise SyntaxError(f"Token inesperado en expresión: {valor}")
    def bucle_mientras(self):

        self.coincidir("PALABRA_CLAVE")  # 'mientras'

        # Leer condición
        condicion = self.expresion()

        # Crear nodo AST
        nodo_mientras = Nodo("mientras", "mientras")
        nodo_mientras.agregar_hijo(Nodo("condicion", condicion))

        # Instrucciones internas
        instrucciones_bucle = self.instrucciones()
        nodo_mientras.agregar_hijo(instrucciones_bucle)

        # Fin del bucle
        if self.actual()[1] != "fin_mientras":
            raise SyntaxError("Se esperaba 'fin_mientras'.")
        self.coincidir("PALABRA_CLAVE")  # fin_mientras
        self.coincidir("DELIMITADOR")    # ;

        return nodo_mientras


    def comparacion(self):
        izquierda = self.expresion()

        tipo, op = self.actual()
        if tipo != "OPERADOR":
            raise SyntaxError(f"Se esperaba operador de comparación, llegó {op}")

        self.avanzar()

        derecha = self.expresion()

        nodo = Nodo("comparacion", op)
        nodo.agregar_hijo(izquierda)
        nodo.agregar_hijo(derecha)
        return nodo
