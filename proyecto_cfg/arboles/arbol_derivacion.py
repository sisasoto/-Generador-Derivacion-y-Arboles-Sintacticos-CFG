"""Define la clase ArbolDerivacion. Es la ÚNICA clase del proyecto que
importa NLTK. Convierte inmediatamente el árbol NLTK a objetos NodoArbol propios."""

import nltk
from nltk import CFG, ChartParser
from arboles.nodo_arbol import NodoArbol
from modelo.gramatica import Gramatica

class ArbolDerivacion:
    """Construye el árbol de derivación para una expresión dada una gramática.
    Usa NLTK internamente y convierte el resultado a objetos NodoArbol.
    Attributes: raiz (NodoArbol | None): La raíz del árbol construido, o None si la expresión no pertenece al lenguaje."""

    def __init__(self, gramatica: Gramatica, expresion: str) -> None:
        """El constructor recibe la gramática y la expresión, y llama al método de construcción.
        Al finalizar, si la expresión pertenece al lenguaje, raiz contendrá el árbol; si no, será None."""
        self._gramatica: Gramatica = gramatica
        self._expresion: str = expresion
        self._raiz: NodoArbol | None = None
        self._construir()

    # Propiedades
    @property
    def raiz(self) -> NodoArbol:
        #Si la expresión pertenece al lenguaje, retorna la raíz del árbol de derivación. Si no, lanza un error indicando que la expresión no es válida para la gramática dada.
        if self._raiz is None:
            raise ValueError(
                f"La expresión '{self._expresion}' no pertenece al lenguaje "
                "de la gramática proporcionada."
            )
        return self._raiz #Se ahorra preguntar si rais es vacio

    # Construcción interna
   
    def _construir(self) -> None:
        #Usa NLTK para parsear la expresión y construye el árbol de NodoArbol. Solo toma el primer árbol encontrado
        try:
            cfg_string = self._gramatica.a_nltk_string()
            gramatica_nltk = CFG.fromstring(cfg_string)
        except Exception as e:
            raise RuntimeError(
                f"Error al convertir la gramática a formato NLTK: {e}"
            ) from e

        tokens = self._expresion.split()
        parser = ChartParser(gramatica_nltk)

        try:
            arboles = list(parser.parse(tokens))
        except ValueError as e:
            raise ValueError(
                f"Error al parsear '{self._expresion}': {e}"
            ) from e

        if not arboles:
            # La expresión no pertenece al lenguaje
            return

        # Tomamos el primer árbol (en caso de ambigüedad)
        arbol_nltk = arboles[0]
        self._raiz = self._convertir_nltk(arbol_nltk)

    def _convertir_nltk(self, nodo_nltk: nltk.Tree | str) -> NodoArbol:
        """Convierte recursivamente un nodo NLTK a un NodoArbol propio. Argumentos: nodo_nltk: Árbol NLTK o string terminal.
       Retorna: El NodoArbol equivalente al nodo NLTK dado. Si el nodo NLTK es un string, se considera un terminal y se crea un NodoArbol hoja. 
       Si es un árbol, se crea un NodoArbol con la etiqueta del nodo y se convierten recursivamente sus hijos."""

        if isinstance(nodo_nltk, str):
            # Es un terminal: hoja del árbol
            return NodoArbol(nodo_nltk)

        # Es un nodo interno (no-terminal)
        etiqueta: str = nodo_nltk.label()
        hijos: list[NodoArbol] = [
            self._convertir_nltk(hijo) for hijo in nodo_nltk #Recorre cada hijo del nodo NLTK y lo convierte a NodoArbol.
        ]
        return NodoArbol(etiqueta, hijos)

    def __repr__(self) -> str:
        estado = "construido" if self._raiz else "sin árbol"
        return f"ArbolDerivacion(expr={self._expresion!r}, {estado})"
