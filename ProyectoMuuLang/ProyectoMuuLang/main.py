from analizador_lexico import Lexer
from parser import Parser
from semantic.SemanticAnalyzer import SemanticAnalyzer
from interpreter import Interpreter


def main():
    try:
        with open("programa.muu", "r", encoding="utf-8") as archivo:
            codigo = archivo.read()

        lexer = Lexer(codigo)
        tokens = lexer.analizar()

        parser = Parser(tokens)
        arbol = parser.analizar()

        print("\n== ANÁLISIS SEMÁNTICO ==")
        sem = SemanticAnalyzer()
        sem.analizar(arbol)
        print("Análisis semántico correcto.")

        print("\n== EJECUCIÓN ==")
        interpreter = Interpreter()
        interpreter.ejecutar(arbol)

    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
