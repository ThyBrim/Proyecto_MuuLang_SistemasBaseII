# ir/IROptimizer.py

class IROptimizer:


    def optimizar(self, code):
        optimizado = []
        for instr in code:
            op, a1, a2, res = instr


            if op == "ASSIGN" and a1 == res:
                continue


            if op == "ADD" and a2 == "0":
                optimizado.append(("ASSIGN", a1, None, res))
                continue



            optimizado.append(instr)

        return optimizado
