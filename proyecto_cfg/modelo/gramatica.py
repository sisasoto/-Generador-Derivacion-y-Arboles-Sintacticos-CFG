"""Define la clase Gramatica, que agrupa todas las producciones de una CFG,
conoce el símbolo inicial, puede validarse, leer desde archivo de texto
y ofrecer gramáticas predefinidas como métodos estáticos.
Formato esperado del archivo de texto:
    S -> A B
    A -> 'a'
    B -> 'b' | 'c'  - Las comillas simples marcan terminales en estilo NLTK; también se aceptan tokens en minúscula o dígitos como terminales sin comillas."""
from modelo.simbolo import Simbolo
from modelo.produccion import Produccion

class Gramatica:
    """Colección completa de producciones de una gramática libre de contexto.
    Atributos privados:
        producciones (list[Produccion]): Todas las reglas de la gramática.
        simbolo_inicial (Simbolo): El símbolo de arranque de la gramática.
        no_terminales (set[Simbolo]): Conjunto de no-terminales detectados.
        terminales (set[Simbolo]): Conjunto de terminales detectados."""
        
    def __init__(self,
                 producciones: list[Produccion],
                 simbolo_inicial: Simbolo) -> None:  #Constructor que recibe la lista de producciones y el símbolo inicial.
        self._producciones: list[Produccion] = producciones
        self._simbolo_inicial: Simbolo = simbolo_inicial
        self._no_terminales: set[Simbolo] = set() #Inicia dos conjuntos vacios pa terminales y no y luego los llena con el método _clasificar_simbolos.
        self._terminales: set[Simbolo] = set()
        self._clasificar_simbolos()

    # Propiedades

    @property
    def producciones(self) -> list[Produccion]:
        return self._producciones

    @property
    def simbolo_inicial(self) -> Simbolo:
        return self._simbolo_inicial

    @property
    def no_terminales(self) -> set[Simbolo]:
        return self._no_terminales

    @property
    def terminales(self) -> set[Simbolo]:
        return self._terminales

    def _clasificar_simbolos(self) -> None: #Identifica y clasifica todos los símbolos en terminales y no-terminales.
        lhs_nombres: set[str] = {p.izquierda.nombre for p in self._producciones} #pa cada producción, toma el nombre del símbolo del lado izquierdo y lo pone en un conjunto.
        for prod in self._producciones: 
            self._no_terminales.add(prod.izquierda)
            for simbolo in prod.derecha: #lo mismo pal lado derecho
                if simbolo.nombre in lhs_nombres:   #Si el nombre del símbolo aparece como lado izquierdo en alguna producción, es un no-terminal.
                    simbolo.es_terminal = False
                    self._no_terminales.add(simbolo)
                else:       #Si no aparece como lado izquierdo, se asume que es terminal.
                    simbolo.es_terminal = True
                    self._terminales.add(simbolo)

    # Conversión a formato NLTK
    def a_nltk_string(self) -> str:
        #Convierte la gramática a una cadena en formato NLTK CFG.Retorna: Cadena con todas las producciones en formato NLTK.
        lineas: list[str] = []
        for prod in self._producciones:
            lhs = prod.izquierda.nombre
            rhs_partes: list[str] = []
            for s in prod.derecha:
                if s.es_terminal:
                    rhs_partes.append(f"'{s.nombre}'")
                else:
                    rhs_partes.append(s.nombre)
            lineas.append(f"{lhs} -> {' '.join(rhs_partes)}") #convierte terminales con comillas simples y no terminales con comillas "E -> E '+' T".

        # Agrupar por lado izq para compactar (A -> x | y)
        agrupadas: dict[str, list[str]] = {}
        for linea in lineas:
            lhs, rhs = linea.split(" -> ", 1)
            agrupadas.setdefault(lhs, []).append(rhs)

        resultado: list[str] = []
        # El símbolo inicial va primero y obtendo un strinf con las poducciones agrupadas. ejemplo: S -> A B | C D
        inicio = self._simbolo_inicial.nombre
        if inicio in agrupadas:
            resultado.append(f"{inicio} -> {' | '.join(agrupadas[inicio])}")
        for lhs, rhs_lista in agrupadas.items():
            if lhs != inicio:
                resultado.append(f"{lhs} -> {' | '.join(rhs_lista)}")

        return "\n".join(resultado)

    # Validación
     #Verifica que la gramática sea internamente consistente.Retorna:(True, "") si es válida, (False, mensaje) si hay error.
    def validar(self) -> tuple[bool, str]:
        if not self._producciones:
            return False, "La gramática no tiene producciones."
        lhs_nombres = {p.izquierda.nombre for p in self._producciones}
        if self._simbolo_inicial.nombre not in lhs_nombres:
            return False, (
                f"El símbolo inicial '{self._simbolo_inicial.nombre}' "
                "no aparece como lado izquierdo de ninguna producción."
            )
        return True, ""  #Si pasa todas las validaciones, retorna True y un mensaje vacío.

    # Carga desde archivo
    @staticmethod #Permite crear una gramática a partir de un texto con el formato especificado. No necesita un objeto pa ejecutarse
    def desde_texto(texto: str) -> "Gramatica":
        """Parsea el texto de la gramática y construye un objeto Gramatica.
        Argumentos: texto: Contenido del archivo de gramática. Retorna: Objeto Gramatica construido.Raises:ValueError: Si el formato no es válido."""
        
        producciones: list[Produccion] = []
        simbolo_inicial: Simbolo | None = None

        for numero, linea_raw in enumerate(texto.strip().splitlines(), start=1):
            linea = linea_raw.strip() #Elimina espacios al inicio y al final de la línea.
            if not linea or linea.startswith("#"): #Ignora líneas vacías o comentarios
                continue
            #Busca el separador '->' o '→' para dividir lado izquierdo y derecho. Si no encuentra, lanza error. 
            if "->" in linea:
                partes = linea.split("->", 1)
            elif "→" in linea:
                partes = linea.split("→", 1)
            else:
                raise ValueError(
                    f"Línea {numero}: falta '->' en '{linea_raw.rstrip()}'"
                )
            #Divide la línea en lado izquierdo y derecho, eliminando espacios extra. Si el lado izquierdo está vacío, lanza error.
            lhs_str = partes[0].strip()
            rhs_str = partes[1].strip()

            if not lhs_str:
                raise ValueError(f"Línea {numero}: lado izquierdo vacío.")

            lhs_simbolo = Simbolo(lhs_str, es_terminal=False)
            if simbolo_inicial is None:
                simbolo_inicial = lhs_simbolo

            alternativas = rhs_str.split("|") # Divide las alternativas del lado derecho
            for alt in alternativas:  #crea los simbolos y construye las producciones. Todos como no terminales al principio.
                tokens = Gramatica._tokenizar_rhs(alt.strip(), numero)
                rhs_simbolos = [Simbolo(t, es_terminal=False) for t in tokens] #construye una lista transdormando cada elemento en otor elemento de otra lista
                producciones.append(Produccion(lhs_simbolo, rhs_simbolos))

        if simbolo_inicial is None:
            raise ValueError("El archivo de gramática está vacío.")

        return Gramatica(producciones, simbolo_inicial)

    # Divide el lado derecho de una producción en tokens individuales. Respeta los terminales entre comillas simples como una unidad.
    @staticmethod
    def _tokenizar_rhs(rhs: str, numero_linea: int) -> list[str]:
        tokens: list[str] = []
        i = 0
        while i < len(rhs):
            c = rhs[i]
            if c == "'":
                j = rhs.find("'", i + 1) #busca comillas simples para identificar terminales. Si no encuentra una comilla de cierre, lanza error.
                if j == -1:
                    raise ValueError(
                        f"Línea {numero_linea}: comilla sin cerrar en '{rhs}'"
                    )
                tokens.append(rhs[i + 1:j])
                i = j + 1
            elif c == " ":  
                i += 1
            else:
                j = i
                while j < len(rhs) and rhs[j] not in (" ", "'"):
                    j += 1
                tokens.append(rhs[i:j]) #Agrega el token encontrado a la lista. Un token es una secuencia de caracteres sin espacios ni comillas.
                i = j
        return tokens

    @staticmethod
    def desde_archivo(ruta: str) -> "Gramatica":
    #Lee un archivo de texto y construye la gramática. argumentos: uta: Ruta al archivo .txt con las producciones.Retorna:Objeto Gramatica construido.
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        return Gramatica.desde_texto(contenido)

    # Gramáticas predefinidas

    """Gramática de expresiones aritméticas con precedencia.
    Acepta letras individuales (a-z) y dígitos (0-9) como terminales,
    además de operadores +, -, *, / y paréntesis.
     E -> E + T | E - T | T
    T -> T * F | T / F | F
    F -> ( E ) | a | b | ... | z | 0 | 1 | ... | 9"""
    @staticmethod
    def expresiones_aritmeticas() -> "Gramatica":
        letras = [chr(c) for c in range(ord('a'), ord('z') + 1)] #Chr convierte un código ASCII a su caracter correspondiente. ord('a') da el código ASCII de 'a' y ord('z') el de 'z'. Esto genera una lista de letras de la a a la z.
        digitos = [str(d) for d in range(10)] #str convierte un número en su representación de cadena. range(10) genera los números del 0 al 9.
        terminales_f = " | ".join(f"'{t}'" for t in letras + digitos) #une las letras y dígitos en una cadena con formato de terminales para la producción de F.

        texto = (
            "E -> E '+' T | E '-' T | T\n"
            "T -> T '*' F | T '/' F | F\n"
            f"F -> '(' E ')' | {terminales_f}\n"
        )
        return Gramatica.desde_texto(texto)

    def __repr__(self) -> str: #Representación legible de la gramática, mostrando el símbolo inicial y el número de producciones.
        return (
            f"Gramatica(inicio={self._simbolo_inicial.nombre!r}, "
            f"producciones={len(self._producciones)})"
        )