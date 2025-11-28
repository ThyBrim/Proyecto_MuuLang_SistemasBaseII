import re

class Lexer:
    TOKEN_REGEX = [
        ("COMENTARIO", r"rumiar.*"),
        ("PALABRA_CLAVE",
         r"\b(muu|vaca|toro|pastar|ordeñar|establo|fin_establo|si|sino|mientras|fin_mientras|para|hasta|fin_para)\b"),
        ("NUMERO", r"\b\d+(\.\d+)?\b"),
        ("CADENA", r'"[^"\n]*"'),
        ("OPERADOR", r"(==|!=|>=|<=|[+\-*/<>])"),
        ("ASIGNACION", r"="),
        ("IDENTIFICADOR", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
        ("DELIMITADOR", r"[();{}]"),
        ("ESPACIO", r"[ \t\n]+"),
        ("DESCONOCIDO", r".")
    ]

    # Crear el patrón global de expresiones regulares
    TOKEN_PATTERN = re.compile(
        "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_REGEX)
    )

    def __init__(self, codigo):
        self.codigo = codigo
        self.tokens = []

    def analizar(self):
        """Analiza el código fuente y extrae los tokens"""
        posicion = 0
        while posicion < len(self.codigo):
            match = self.TOKEN_PATTERN.match(self.codigo, posicion)
            if match:
                for tipo in self.TOKEN_PATTERN.groupindex:
                    valor = match.group(tipo)
                    if valor:  # Si se encontró una coincidencia
                        if tipo != "ESPACIO" and tipo != "COMENTARIO":  # Ignorar espacios y comentarios
                            self.tokens.append((tipo, valor))
                        break
                posicion = match.end()  # Avanzar a la siguiente posición
            else:
                raise SyntaxError(f"Carácter inesperado: '{self.codigo[posicion]}' en la posición {posicion}")
        return self.tokens

    def guardar_en_archivo(self, archivo_salida):
        """Guarda los tokens en un archivo de salida"""
        with open(archivo_salida, "w", encoding="utf-8") as f:
            for tipo, valor in self.tokens:
                f.write(f"{tipo}: {valor}\n")
        print(f"Tokens guardados en {archivo_salida}")
