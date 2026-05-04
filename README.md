# ✨ Generador de Árboles Sintácticos

> **Derivación y Árboles Sintácticos para Gramáticas Libres de Contexto**  
> Visualiza derivaciones izquierda/derecha, árboles de derivación y AST de forma interactiva.

---

![Python](https://img.shields.io/badge/Python-3.13.3-4A9EC4?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-5BBF8A?style=for-the-badge&logo=qt&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-3.8+-F9C8D4?style=for-the-badge)
![License](https://img.shields.io/badge/Paradigma-POO-B5D5F5?style=for-the-badge)

---

## 👤 Integrante

| Nombre completo | Lenguaje | Versión | IDE |
|---|---|---|---|
| Simon Santiago Soto Berrío | Python | 3.13.3 | Visual Studio Code |

---

## 📖 ¿Qué es esta aplicación?

Esta aplicación es una herramienta visual e interactiva para el estudio de **gramáticas libres de contexto (CFG)**. Dado una gramática y una expresión objetivo, el programa genera automáticamente:

- 📋 La **derivación paso a paso** — izquierda o derecha, según elijas
- 🌳 El **árbol de derivación** — representación visual de cada expansión
- ✨ El **AST (Árbol Sintáctico Abstracto)** — versión simplificada sin nodos redundantes

---
## 🎬 Demostración

https://github.com/user-attachments/assets/4847d12a-f082-4c8f-8978-7bed91076029
## 🚀 Instalación y ejecución

**1. Clona el repositorio**
```bash
git clone https://github.com/sisasoto/Practica-2.git
cd Practica-2/proyecto_cfg
```

**2. Instala las dependencias**
```bash
pip install -r requirements.txt
```

**3. Descarga los recursos de NLTK** *(solo la primera vez)*
```bash
python -m nltk.downloader all
```

**4. Ejecuta la aplicación**
```bash
python main.py
```

---

## 📦 Librerías utilizadas

| Librería | Versión | Uso en el proyecto |
|---|---|---|
| `PyQt5` | ≥ 5.15.0 | Interfaz gráfica, ventanas, widgets y dibujo de árboles con QPainter |
| `nltk` | ≥ 3.8.0 | Parsing de la gramática y construcción del árbol de derivación |

---

## 🎮 ¿Cómo usar la aplicación?

### Paso 1 — Cargar la gramática

Tienes **tres formas** de ingresar una gramática:

**📂 Desde archivo:** presiona *"Cargar desde archivo…"* y selecciona un `.txt` con tus reglas.

**✏️ Desde el editor:** escribe directamente en el área de texto y presiona *"Usar gramática del texto"*.

**⚡ Gramática predefinida:** selecciona *"Expresiones aritméticas"* en el menú desplegable — el programa carga automáticamente una gramática completa lista para usar, con soporte para letras `a-z`, dígitos `0-9`, operadores `+ - * /` y paréntesis.

---

### Paso 2 — Escribir la gramática (formato)

```
# Esto es un comentario, se ignora
E -> E '+' T | E '-' T | T
T -> T '*' F | T '/' F | F
F -> '(' E ')' | <a-z> | <0-9>
```

| Elemento | Cómo se escribe | Ejemplo |
|---|---|---|
| No-terminal | Sin comillas, en mayúscula | `E`, `T`, `F` |
| Terminal | Entre comillas simples | `'+'`, `'x'`, `'('` |
| Alternativas | Separadas por `\|` | `E '+' T \| T` |
| Rango de letras | Entre `< >` | `<a-z>` |
| Rango de dígitos | Entre `< >` | `<0-9>` |
| Comentarios | Línea que empieza con `#` | `# mi comentario` |

> ⚠️ La expresión que ingreses debe tener los tokens **separados por espacios**:  
> ✅ Correcto: `( 5 * x ) + y`  
> ❌ Incorrecto: `(5*x)+y`

---

### Paso 3 — Generar la derivación

1. Escribe la expresión objetivo en el campo *"Expresión objetivo"*
2. Elige **Derivación por la Izquierda** o **Derivación por la Derecha**
3. Presiona **▶ Generar Derivación**

Los resultados aparecen automáticamente en los tres paneles: pasos, árbol de derivación y AST.

---

## 🧱 Programación Orientada a Objetos

Este proyecto aplica el paradigma POO de forma rigurosa. Cada componente del problema está modelado como una clase con responsabilidad única.

### Diagrama de clases principal

```
Gramatica ──────────────── Produccion ─── Simbolo
    │
    ▼
ArbolDerivacion  (única clase que usa NLTK)
    │
    ▼
NodoArbol  ◄──── viaja por todo el sistema
    │
    ├──► Derivacion  (clase abstracta)
    │         ├── DerivacionIzquierda
    │         └── DerivacionDerecha
    │
    └──► ConstructorAST
    
HiloDerivacion (QThread) ──► VentanaPrincipal
LienzoArbol (QWidget)    ──► dibuja NodoArbol
```

### Principios aplicados

| Principio | Cómo se aplica |
|---|---|
| **Encapsulamiento** | Atributos privados con `_` y acceso controlado por propiedades `@property` |
| **Herencia** | `DerivacionIzquierda` y `DerivacionDerecha` heredan de la clase abstracta `Derivacion` |
| **Polimorfismo** | `HiloDerivacion` llama `.derivar()` sin importar cuál de las dos subclases tiene |
| **Abstracción** | `VentanaPrincipal` no conoce NLTK. Solo `ArbolDerivacion` lo usa internamente |
| **Responsabilidad única** | Cada clase hace exactamente una cosa: `NodoArbol` solo guarda datos, `LienzoArbol` solo dibuja |

---

## ✨ Características destacadas

### 🌳 Árbol visual estilo JFLAP
Los árboles se dibujan con `QPainter` directamente sobre el canvas. Los nodos no-terminales se muestran en **azul lavanda** y los terminales en **rosa pastel**, con sombra suave y distribución simétrica automática por niveles.

### 🔀 Derivación izquierda y derecha
Implementadas como subclases de una clase abstracta. La derivación trabaja sobre el árbol ya construido por NLTK — simulando la expansión con una lista de nodos que se reemplaza iterativamente sin necesidad de backtracking propio.

### ❓ Popup de ayuda interactivo
El botón *"¿Cómo se escribe?"* abre un diálogo con guía completa del formato de gramática, incluyendo ejemplos de rangos `<a-z>` y `<0-9>`, comentarios y casos de uso. Construido desde un diccionario de secciones para mantener el código limpio.

### ⚡ Gramática predefinida lista para usar
El menú desplegable incluye una gramática de expresiones aritméticas completa que soporta todas las letras del alfabeto, dígitos del 0 al 9, los cuatro operadores básicos y paréntesis. Ideal para probar la aplicación sin escribir nada.

### 🧵 Multithreading con QThread
El cálculo de la derivación ocurre en un hilo separado para que la interfaz nunca se congele. Mientras se calcula, el botón muestra una **animación de pulso** y la barra de estado indica el progreso.

### 🛡️ Manejo de errores
La aplicación detecta y reporta claramente los siguientes casos:
- Gramática con errores de sintaxis en el archivo
- Expresión que no pertenece al lenguaje de la gramática
- Símbolo inicial sin producciones definidas
- Archivo vacío o ilegible

---

## 🗂️ Estructura del proyecto

```
proyecto_cfg/
├── main.py                        ← Punto de entrada, lanza PyQt5
├── requirements.txt               ← Dependencias
│
├── modelo/
│   ├── simbolo.py                 ← Clase Simbolo (terminal / no-terminal)
│   ├── produccion.py              ← Clase Produccion (regla A → α)
│   └── gramatica.py               ← Clase Gramatica (colección de reglas + lectura de archivo)
│
├── derivacion/
│   ├── derivacion.py              ← Clase abstracta Derivacion (ABC)
│   ├── derivacion_izquierda.py    ← Expande siempre el no-terminal más a la izquierda
│   └── derivacion_derecha.py      ← Expande siempre el no-terminal más a la derecha
│
├── arboles/
│   ├── nodo_arbol.py              ← Nodo genérico con etiqueta e hijos
│   ├── arbol_derivacion.py        ← Usa NLTK y convierte a NodoArbol propio
│   └── constructor_ast.py         ← Simplifica el árbol de derivación → AST
│
└── interfaz/
    ├── ventana_principal.py       ← QMainWindow con todos los widgets
    ├── lienzo_arbol.py            ← QWidget que dibuja el árbol con QPainter
    └── hilo_derivacion.py         ← QThread que ejecuta el cálculo en paralelo
```

---

## 🔗 Repositorio

[![GitHub](https://img.shields.io/badge/GitHub-sisasoto%2FPractica--2-1A3A4A?style=for-the-badge&logo=github&logoColor=white)](https://github.com/sisasoto/Practica-2)

---

<div align="center">

✨ *Hecho con Python, PyQt5 y NLTK*  
**Simon Santiago Soto Berrío — ST0244 Lenguajes de Programación — EAFIT 2026**

</div>
