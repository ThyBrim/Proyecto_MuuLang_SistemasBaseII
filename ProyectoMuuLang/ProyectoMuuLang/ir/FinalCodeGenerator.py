# ir/FinalCodeGenerator.py

class FinalCodeGenerator:

    def generar(self, code):
        lineas = []

        for op, a1, a2, res in code:

            if op == "ASSIGN":
                lineas.append(f"MOV {res}, {a1}")

            # Operaciones aritméticas
            elif op == "ADD":
                lineas.append(f"ADD {res}, {a1}, {a2}")

            elif op == "SUB":
                lineas.append(f"SUB {res}, {a1}, {a2}")

            elif op == "MUL":
                lineas.append(f"MUL {res}, {a1}, {a2}")

            elif op == "DIV":
                lineas.append(f"DIV {res}, {a1}, {a2}")

            # Impresión
            elif op == "PRINT_STR":
                # a1 contiene el texto de la cadena
                lineas.append(f'OUT_STR "{a1}"')

            elif op == "PRINT_VAR":
                # a1 es el nombre de la variable
                lineas.append(f"OUT {a1}")

            # Etiquetas y saltos
            elif op == "LABEL":
                # a1 es el nombre de la etiqueta
                lineas.append(f"{a1}:")

            elif op == "GOTO":
                # a1 es la etiqueta destino
                lineas.append(f"JMP {a1}")

            # Condicional: IF a1 >= a2 GOTO res
            elif op == "IF_GE":
                lineas.append(f"CMP_GE {a1}, {a2}")
                lineas.append(f"JMP_IF_TRUE {res}")

            # Condicional: IF a1 == a2 GOTO res
            elif op == "IF_EQ":
                lineas.append(f"CMP_EQ {a1}, {a2}")
                lineas.append(f"JMP_IF_TRUE {res}")

            # Comparación que produce un temporal (para expresiones booleanas)
            elif op == "CMP":
                # res = (a1 ? a2) → aquí lo dejamos como operación abstracta
                lineas.append(f"CMP {res}, {a1}, {a2}")

            # Cualquier instrucción desconocida se comenta
            else:
                lineas.append(f"; INSTR NO SOPORTADA: {op} {a1} {a2} {res}")

        return lineas
