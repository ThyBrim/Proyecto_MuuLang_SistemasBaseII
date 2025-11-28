from semantic.SymbolTable import SymbolTable


class SemanticAnalyzer:
    def __init__(self):
        self.sym = SymbolTable()   # tabla de símbolos

    # ==================================================
    #   DESPACHO GENERAL (llama sa_tipo según el nodo)
    # ==================================================
    def analizar(self, nodo):
        metodo = getattr(self, f"sa_{nodo.tipo}", None)
        if metodo is None:
            raise Exception(f"No existe análisis semántico para nodo: {nodo.tipo}")
        return metodo(nodo)

    def get_symbols(self):
        """Devuelve la tabla de símbolos actual como diccionario."""
        return dict(self.sym.tabla)

    # ==================================================
    #                PROGRAMA E INSTRUCCIONES
    # ==================================================
    def sa_programa(self, nodo):
        instrucciones = nodo.hijos[0]
        self.sa_instrucciones(instrucciones)

    def sa_instrucciones(self, nodo):
        for hijo in nodo.hijos:
            self.analizar(hijo)

    # ==================================================
    #                    DECLARACIÓN
    # ==================================================
    def sa_declaracion(self, nodo):
        nombre = nodo.hijos[0].valor
        valor = nodo.hijos[1]

        tipo_val = self.tipo_expresion(valor)
        self.sym.declarar(nombre, tipo_val)

    # ==================================================
    #                    ASIGNACIÓN
    # ==================================================
    def sa_asignacion(self, nodo):
        nombre = nodo.hijos[0].valor
        expr = nodo.hijos[1]

        tipo_expr = self.tipo_expresion(expr)
        self.sym.asignar(nombre, tipo_expr)

    # ==================================================
    #                    IMPRESIÓN
    # ==================================================
    def sa_impresion(self, nodo):
        hijo = nodo.hijos[0]
        if hijo.tipo == "identificador":
            self.sym.obtener(hijo.valor)  # valida que exista

    # ==================================================
    #                    BUCLE PARA
    # ==================================================
    def sa_bucle_para(self, nodo):
        nombre = nodo.hijos[0].valor
        inicio = nodo.hijos[1]
        fin = nodo.hijos[2]
        instrucciones = nodo.hijos[3]

        if self.tipo_expresion(inicio) != "numero":
            raise Exception("Error semántico: el inicio del 'para' debe ser número.")

        if self.tipo_expresion(fin) != "numero":
            raise Exception("Error semántico: el fin del 'para' debe ser número.")

        # declarar variable iteradora
        self.sym.declarar(nombre, "numero")

        # analizar cuerpo
        self.sa_instrucciones(instrucciones)

    # alias por si el parser usa "para" en vez de "bucle_para"
    sa_para = sa_bucle_para

    # ==================================================
    #                BUCLE MIENTRAS
    # ==================================================
    def sa_mientras(self, nodo):
        condicion = nodo.hijos[0]      # nodo de la condición
        instrucciones = nodo.hijos[1]  # bloque interno

        tipo = self.tipo_expresion(condicion)

        if tipo != "booleano":
            raise Exception("Error semántico: la condición de 'mientras' debe ser booleana.")

        self.sa_instrucciones(instrucciones)

    # ==================================================
    #                CONDICIONAL SI
    # ==================================================
    def sa_si(self, nodo):
        condicion = nodo.hijos[0]
        tipo = self.tipo_expresion(condicion)

        if tipo != "booleano":
            raise Exception("Error semántico: la condición del 'si' debe ser booleana.")

        # bloque del si
        self.sa_instrucciones(nodo.hijos[1])

        # si tiene sino
        if len(nodo.hijos) == 3:
            self.sa_instrucciones(nodo.hijos[2])

    # ==================================================
    #                TIPOS DE EXPRESIONES
    # ==================================================
    def tipo_expresion(self, nodo):
        # número literal
        if nodo.tipo == "numero":
            return "numero"

        # identificador (buscar en tabla)
        if nodo.tipo == "identificador":
            return self.sym.obtener(nodo.valor)

        # operación aritmética
        if nodo.tipo == "op":
            izq = self.tipo_expresion(nodo.hijos[0])
            der = self.tipo_expresion(nodo.hijos[1])

            if izq != "numero" or der != "numero":
                raise Exception("Error semántico: operaciones solo permitidas entre números.")

            return "numero"

        # expresión booleana / comparación
        if nodo.tipo == "comparacion":
            izq = self.tipo_expresion(nodo.hijos[0])
            der = self.tipo_expresion(nodo.hijos[1])

            if izq != "numero" or der != "numero":
                raise Exception("Error semántico: comparación solo entre números.")

            return "booleano"

        raise Exception(f"No se puede determinar tipo para nodo: {nodo.tipo}")
