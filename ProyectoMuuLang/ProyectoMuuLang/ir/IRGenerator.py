# ir/IRGenerator.py

class IRGenerator:

    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self, base="L"):
        self.label_counter += 1
        return f"{base}{self.label_counter}"

    def generar(self, nodo):
        self.code = []
        self._gen(nodo)
        return self.code

    def _gen(self, nodo):
        metodo = getattr(self, f"_gen_{nodo.tipo}", None)

        if metodo is None:
            if nodo.tipo == "instrucciones":
                return self._gen_instrucciones(nodo)
            if nodo.tipo == "mientras":
                return self._gen_mientras(nodo)
            return  # nodo no soportado

        return metodo(nodo)

    def _gen_programa(self, nodo):
        if nodo.hijos:
            self._gen(nodo.hijos[0])


    def _gen_instrucciones(self, nodo):
        for hijo in nodo.hijos:
            self._gen(hijo)

    def _gen_declaracion(self, nodo):
        nombre = nodo.hijos[0].valor
        valor_nodo = nodo.hijos[1]
        src = self._gen_expr(valor_nodo)
        self.code.append(("ASSIGN", src, None, nombre))


    def _gen_asignacion(self, nodo):
        nombre = nodo.hijos[0].valor
        expr_nodo = nodo.hijos[1]
        src = self._gen_expr(expr_nodo)
        self.code.append(("ASSIGN", src, None, nombre))


    def _gen_impresion(self, nodo):
        hijo = nodo.hijos[0]

        if hijo.tipo == "cadena":
            self.code.append(("PRINT_STR", hijo.valor, None, None))

        elif hijo.tipo == "identificador":
            self.code.append(("PRINT_VAR", hijo.valor, None, None))


    def _gen_bucle_para(self, nodo):

        nombre = nodo.hijos[0].valor
        inicio_nodo = nodo.hijos[1]
        fin_nodo = nodo.hijos[2]
        cuerpo = nodo.hijos[3]

        inicio = self._gen_expr(inicio_nodo)
        fin = self._gen_expr(fin_nodo)

        # i = inicio
        self.code.append(("ASSIGN", inicio, None, nombre))

        lbl_inicio = self.new_label("Lpara")
        lbl_fin = self.new_label("Lfin")

        self.code.append(("LABEL", lbl_inicio, None, None))

        # if i >= fin goto Lfin
        self.code.append(("IF_GE", nombre, fin, lbl_fin))

        # cuerpo
        self._gen(cuerpo)

        # i = i + 1
        self.code.append(("ADD", nombre, "1", nombre))

        # goto Lpara
        self.code.append(("GOTO", lbl_inicio, None, None))

        self.code.append(("LABEL", lbl_fin, None, None))

    _gen_para = _gen_bucle_para   # alias por compatibilidad

    def _gen_mientras(self, nodo):
        """
        mientras
            condicion
            instrucciones
        """
        condicion = nodo.hijos[0]
        cuerpo = nodo.hijos[1]

        lbl_inicio = self.new_label("Lmientras")
        lbl_fin = self.new_label("Lfinm")

        # Lmientras:
        self.code.append(("LABEL", lbl_inicio, None, None))

        # condición
        cond_temp = self._gen_expr(condicion)

        # si cond_temp == 0 → terminar
        self.code.append(("IF_EQ", cond_temp, "0", lbl_fin))

        # cuerpo
        self._gen(cuerpo)

        # regresar al inicio
        self.code.append(("GOTO", lbl_inicio, None, None))

        # salida
        self.code.append(("LABEL", lbl_fin, None, None))


    def _gen_expr(self, nodo):

        if nodo.tipo in ("numero", "NUMERO"):
            return str(nodo.valor)

        if nodo.tipo in ("identificador", "IDENTIFICADOR"):
            return nodo.valor

        if nodo.tipo == "op":
            izq = self._gen_expr(nodo.hijos[0])
            der = self._gen_expr(nodo.hijos[1])
            op = nodo.valor
            temp = self.new_temp()

            if op == "+":
                self.code.append(("ADD", izq, der, temp))
            elif op == "-":
                self.code.append(("SUB", izq, der, temp))
            elif op == "*":
                self.code.append(("MUL", izq, der, temp))
            elif op == "/":
                self.code.append(("DIV", izq, der, temp))

            return temp

        if nodo.tipo == "comparacion":
            izq = self._gen_expr(nodo.hijos[0])
            der = self._gen_expr(nodo.hijos[1])
            temp = self.new_temp()
            self.code.append(("CMP", izq, der, temp))
            return temp

        if nodo.tipo == "valor" and nodo.hijos:
            return self._gen_expr(nodo.hijos[0])

        return str(nodo.valor)
