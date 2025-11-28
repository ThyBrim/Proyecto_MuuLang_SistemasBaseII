# Proyecto MuuLang

MuuLang es un lenguaje de programacion simplficado e intuitivo, enfocado en el area educativa tematizado con "vacas" y "granja" y diseñado para demostrar el funcionamiento interno de un compilador. 

## Información del Curso
* Materia: Programación en Sistemas de Base II
* Institución: Univerisidad Autonoma de Tamaulipas
* Semestre: Noveno semestre de 2025
* Profesor: Dante Adolfo Muñoz Quintero

## Integrantes del Equipo
-Angel Alejandro Cervantes de la Rosa - a2213332146
-Emmanuel Mendez de Jesus - a2213332184
-Fernando Aron Saenz Rico Perez - a2213332206
-Leonardo Yañez Reyna - a2183228019

## Estructura del Proyecto
Directorio Raíz
* main.py - Punto de entrada principal de la aplicación.
* analizador_lexico.py - Convierte el código fuente en una secuencia de tokens.
* parser.py - Verifica la estructura gramatical del código.
* nodo.py - Define la estructura de los nodos para la construcción del Árbol de Sintaxis Abstracta (AST).
* interfaz.py - Gestiona la interfaz gráfica (GUI) o de línea de comandos para interactuar con el compilador.
* interpreter.py - Módulo para la ejecución directa o interpretación del código fuente.
* programa.muu - Archivo de ejemplo con código fuente escrito en el lenguaje MuuLang para pruebas.
* tokens.txt - Archivo de salida o referencia que lista los tokens generados.

Módulo Semántico
* SemanticAnalyzer.py - Realiza el análisis semántico (comprobación de tipos, scopes, etc.).
* SymbolTable.py - Implementación de la Tabla de Símbolos para gestionar variables y funciones.

Módulo de Código Intermedio
* IRGenerator.py - Generador de Representación Intermedia (Intermediate Representation).
* IROptimizer.py - Módulo encargado de la optimización del código intermedio.
* FinalCodeGenerator.py - Generador de código final (target code) a partir de la representación intermedia optimizada.


## Requisitos y Dependencias
* re: Utilizada para expresiones regares en el analisis lexico para identificar los tokens.
* tkinter: Utilizada para crear la interfaz grafica de usario, incluyendo el módulo scrpññedtext para el área de edición y consola
* sys: Utilizada dentro de la interfaz para redirigir la salida estándar (stdout) y capaturar lo que imprime el intérprete.
* io: Utilizada junto con sys para crear un buffer de memoria (StringIO) donde se almacena temporalmente la salda del programa antes de mostrarla en la ventana de la aplicación.


## Instrucciones de Compilación y Ejecución

### 1. Preparar el Entorno
Asegurarte de estar en ela carpeta raíz del proyecto y activa el entorno virtual 
    bash
    .\venv\Scripts\active

### 2. Ejecutar la interfaz Grafica
La forma mas completa de probar el compilador es mediante su IDE visual, que permite ver los tokens, el árbol sintáctico, la tabla de simbolos y el código intermedio/optimizado

Ejecuta el siguiente comando:
bash 
pythin interfaz.py

## Ejemplos de Uso

establo 

    vaca i = 0;
    vaca limite = 3;
    vaca suma = 0;
    
    muu "Inicio del bucle para";
    para vaca j = 0 hasta 3;
        muu "Hola mundo";
    fin_para;

    muu "Fin del programa";
fin_establo;
