# ir/IROptimizer.py

class IROptimizer:
    """
    Optimizador simple de código intermedio.
    Aplica algunas reglas básicas de optimización local.
    """

    def optimizar(self, code):
        optimizado = []
        for instr in code:
            op, a1, a2, res = instr

            # Eliminar asignaciones redundantes: x = x
            if op == "ASSIGN" and a1 == res:
                continue

            # Simplificar suma con 0: x = y + 0  -> ASSIGN y -> x
            if op == "ADD" and a2 == "0":
                optimizado.append(("ASSIGN", a1, None, res))
                continue

            # (Opcional) otras reglas se pueden agregar aquí

            optimizado.append(instr)

        return optimizado
