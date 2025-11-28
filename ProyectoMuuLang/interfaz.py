import tkinter as tk
from tkinter import scrolledtext
from analizador_lexico import Lexer
from parser import Parser
from interpreter import Interpreter
from semantic.SemanticAnalyzer import SemanticAnalyzer
from ir.IRGenerator import IRGenerator
from ir.IROptimizer import IROptimizer
from ir.FinalCodeGenerator import FinalCodeGenerator


class Interfaz:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Compilador MuuLang IDE")
        self.ventana.geometry("1050x720")

        tk.Label(self.ventana, text="Editor de Código MuuLang:", font=("Arial", 12, "bold")).pack()

        editor_frame = tk.Frame(self.ventana)
        editor_frame.pack(fill="both", expand=True)

        # --- Numeración de líneas ---
        self.line_numbers = tk.Text(
            editor_frame,
            width=4,
            padx=4,
            takefocus=0,
            border=0,
            background="#e8e8e8",
            state="disabled",
            font=("Consolas", 11)
        )
        self.line_numbers.pack(side="left", fill="y")

        self.editor = scrolledtext.ScrolledText(
            editor_frame,
            width=100,
            height=20,
            font=("Consolas", 11),
            undo=True
        )
        self.editor.pack(side="right", fill="both", expand=True)

        self.editor.tag_configure("error", background="#ffcccc")

        self.editor.insert(tk.END,
"""establo
    vaca i = 0;
    vaca limite = 3;
    vaca suma = 0;

    muu "Inicio del bucle para";
    para vaca j = 0 hasta 3;
        muu "Hola mundo";
    fin_para;

    muu "Fin del programa";
fin_establo""")

        # Eventos
        self.editor.bind("<KeyRelease>", self.editor_evento)
        self.editor.bind("<MouseWheel>", self.scroll_sync)

        self.actualizar_numeros()

        frame_botones1 = tk.Frame(self.ventana)
        frame_botones1.pack(pady=2)

        tk.Button(frame_botones1, text="Mostrar Tokens", width=18,
                  command=self.mostrar_tokens).grid(row=0, column=0, padx=4, pady=3)

        tk.Button(frame_botones1, text="Mostrar Árbol Sintáctico", width=18,
                  command=self.mostrar_arbol).grid(row=0, column=1, padx=4, pady=3)

        tk.Button(frame_botones1, text="Tabla de Símbolos", width=18,
                  command=self.mostrar_tabla_simbolos).grid(row=0, column=2, padx=4, pady=3)

        tk.Button(frame_botones1, text="Ejecutar Programa", width=18,
                  command=self.ejecutar_programa).grid(row=0, column=3, padx=4, pady=3)

        # Segunda fila de botones (IR, optimización, código final)
        frame_botones2 = tk.Frame(self.ventana)
        frame_botones2.pack(pady=2)

        tk.Button(frame_botones2, text="Código Intermedio", width=18,
                  command=self.mostrar_codigo_intermedio).grid(row=0, column=0, padx=4, pady=3)

        tk.Button(frame_botones2, text="Código Optimizado", width=18,
                  command=self.mostrar_codigo_optimizado).grid(row=0, column=1, padx=4, pady=3)

        tk.Button(frame_botones2, text="Código Final", width=18,
                  command=self.mostrar_codigo_final).grid(row=0, column=2, padx=4, pady=3)

        tk.Label(self.ventana, text="Salida:", font=("Arial", 12, "bold")).pack()

        self.salida = scrolledtext.ScrolledText(self.ventana, width=120, height=16,
                                                font=("Consolas", 11))
        self.salida.pack(pady=5)

    def editor_evento(self, event=None):
        self.actualizar_numeros()
        self.analizar_en_tiempo_real()


    def actualizar_numeros(self, event=None):
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)

        total_lineas = int(self.editor.index("end-1c").split(".")[0])
        numeros = "\n".join(str(i) for i in range(1, total_lineas + 1))

        self.line_numbers.insert("1.0", numeros)
        self.line_numbers.config(state="disabled")

        self.scroll_sync()

    def scroll_sync(self, event=None):
        self.line_numbers.yview_moveto(self.editor.yview()[0])

    def analizar_en_tiempo_real(self):
        codigo = self.editor.get("1.0", tk.END)

        # Quitar marcas de error anteriores
        self.editor.tag_remove("error", "1.0", tk.END)

        if codigo.strip() == "":
            return

        try:
            lexer = Lexer(codigo)
            tokens = lexer.analizar()

            parser = Parser(tokens)
            arbol = parser.analizar()

            semantic = SemanticAnalyzer()
            semantic.analizar(arbol)

        except Exception as e:
            mensaje = str(e)
            token_error = None
            if "'" in mensaje:
                partes = mensaje.split("'")
                if len(partes) >= 3:
                    token_error = partes[1]

            if token_error:
                pos = self.editor.search(token_error, "1.0", tk.END)
                if pos:
                    linea = pos.split(".")[0]
                    inicio = f"{linea}.0"
                    fin = f"{linea}.end"
                    self.editor.tag_add("error", inicio, fin)
                    return

            self.editor.tag_add("error", "1.0", "end-1c")


    def mostrar_tokens(self):
        try:
            codigo = self.editor.get("1.0", tk.END)
            lexer = Lexer(codigo)
            tokens = lexer.analizar()

            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, "TOKENS GENERADOS:\n\n")

            for t, v in tokens:
                self.salida.insert(tk.END, f"{t}: {v}\n")

        except Exception as e:
            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, f"ERROR EN TOKENS: {e}")

    def mostrar_arbol(self):
        try:
            codigo = self.editor.get("1.0", tk.END)
            lexer = Lexer(codigo)
            tokens = lexer.analizar()

            parser = Parser(tokens)
            arbol = parser.analizar()

            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, "ÁRBOL SINTÁCTICO:\n\n")
            self.imprimir_arbol_widget(arbol)

        except Exception as e:
            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, f"ERROR EN PARSER: {e}")

    def imprimir_arbol_widget(self, nodo, nivel=0):
        self.salida.insert(tk.END, "  " * nivel + f"{nodo.tipo}: {nodo.valor}\n")
        for hijo in nodo.hijos:
            self.imprimir_arbol_widget(hijo, nivel + 1)


    def mostrar_tabla_simbolos(self):
        try:
            codigo = self.editor.get("1.0", tk.END)

            lexer = Lexer(codigo)
            tokens = lexer.analizar()

            parser = Parser(tokens)
            arbol = parser.analizar()

            semantic = SemanticAnalyzer()
            semantic.analizar(arbol)
            simbolos = semantic.get_symbols()

            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, "TABLA DE SÍMBOLOS:\n\n")
            self.salida.insert(tk.END, f"{'Nombre':15}Tipo\n")
            self.salida.insert(tk.END, "-" * 26 + "\n")

            for nombre, tipo in simbolos.items():
                self.salida.insert(tk.END, f"{nombre:15}{tipo}\n")

        except Exception as e:
            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, f"ERROR EN SEMÁNTICO: {e}")


    def _generar_ir(self):
        codigo = self.editor.get("1.0", tk.END)

        lexer = Lexer(codigo)
        tokens = lexer.analizar()

        parser = Parser(tokens)
        arbol = parser.analizar()

        semantic = SemanticAnalyzer()
        semantic.analizar(arbol)

        irgen = IRGenerator()
        code = irgen.generar(arbol)
        return code

    def mostrar_codigo_intermedio(self):
        try:
            code = self._generar_ir()
            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, "CÓDIGO INTERMEDIO (TAC):\n\n")
            for instr in code:
                op, a1, a2, res = instr
                self.salida.insert(tk.END, f"{op:10} {str(a1):8} {str(a2):8} {str(res):8}\n")
        except Exception as e:
            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, f"ERROR AL GENERAR IR: {e}")


    def mostrar_codigo_optimizado(self):
        try:
            code = self._generar_ir()
            opt = IROptimizer()
            code_opt = opt.optimizar(code)

            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, "CÓDIGO INTERMEDIO OPTIMIZADO:\n\n")
            for instr in code_opt:
                op, a1, a2, res = instr
                self.salida.insert(tk.END, f"{op:10} {str(a1):8} {str(a2):8} {str(res):8}\n")
        except Exception as e:
            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, f"ERROR AL OPTIMIZAR: {e}")

    def mostrar_codigo_final(self):
        try:
            code = self._generar_ir()
            opt = IROptimizer()
            code_opt = opt.optimizar(code)

            gen_final = FinalCodeGenerator()
            lineas = gen_final.generar(code_opt)

            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, "CÓDIGO FINAL (PSEUDO ENSAMBLADOR):\n\n")
            for linea in lineas:
                self.salida.insert(tk.END, linea + "\n")

        except Exception as e:
            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, f"ERROR EN CÓDIGO FINAL: {e}")


    def ejecutar_programa(self):
        import sys
        try:
            codigo = self.editor.get("1.0", tk.END)

            lexer = Lexer(codigo)
            tokens = lexer.analizar()

            parser = Parser(tokens)
            arbol = parser.analizar()

            semantic = SemanticAnalyzer()
            semantic.analizar(arbol)

            interpreter = Interpreter()

            import io
            output = io.StringIO()
            sys.stdout = output

            interpreter.ejecutar(arbol)

            sys.stdout = sys.__stdout__
            salida_final = output.getvalue()

            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, "SALIDA DEL PROGRAMA:\n\n")
            self.salida.insert(tk.END, salida_final)

        except Exception as e:
            try:
                sys.stdout = sys.__stdout__
            except:
                pass
            self.salida.delete(1.0, tk.END)
            self.salida.insert(tk.END, f"ERROR: {e}")


def main():
    ventana = tk.Tk()
    app = Interfaz(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
