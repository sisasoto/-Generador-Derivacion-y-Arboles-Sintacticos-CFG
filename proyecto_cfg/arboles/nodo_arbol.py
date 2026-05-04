"""Define la clase NodoArbol, el bloque fundamental de todos los árboles
del proyecto (árbol de derivación y AST). Un NodoArbol solo conoce su etiqueta y sus hijos. NO tiene atributos
de posición visual: esa responsabilidad recae en LienzoArbol."""
class NodoArbol:
    """Nodo genérico para árboles del proyecto.
    Atributos privados:etiqueta (str): El símbolo que representa este nodo.. hijos (list[NodoArbol]): Los nodos hijos (vacío si es hoja/terminal)."""
    def __init__(self, etiqueta: str,
                 hijos: list["NodoArbol"] | None = None) -> None:
        """Constructos que recibe el nodo con su etiqueta y, opcionalmente, sus hijos.
        Argumentos:etiqueta: El símbolo que representa (ej: 'E', '+', 'num'). hijos: Lista de nodos hijos. None equivale a lista vacía."""
        self._etiqueta: str = etiqueta
        self._hijos: list["NodoArbol"] = hijos if hijos is not None else [] #operador ternario: si hijos no es vacio, lo asigna, sino asigna una lista vacía.

    # Propiedades para acceder a los atributos privados
    @property
    def etiqueta(self) -> str:
        #Retorna la etiqueta del nodo.
        return self._etiqueta

    @property
    def hijos(self) -> list["NodoArbol"]:
        #Retorna la lista de hijos del nodo.
        return self._hijos

    def agregar_hijo(self, hijo: "NodoArbol") -> None: 
        #Agrega un hijo al nodo. Argumento:hijo: Nodo a agregar como hijo.
        self._hijos.append(hijo)

    def es_hoja(self) -> bool:
        #Retorna True si el nodo no tiene hijos (es terminal).
        return len(self._hijos) == 0

    # Recorridos para las derivaciones
    def preorden(self) -> list["NodoArbol"]:
        """Recorre el árbol en preorden: raíz, luego hijos de izquierda a derecha.
        Devuelve: Lista de nodos en orden de visita preorden. """
        
        resultado: list["NodoArbol"] = [self]
        for hijo in self._hijos:        #recorre los hijos
            resultado.extend(hijo.preorden()) #Cada hijo se recorre en preorden y se agrega al resultado. extend agrega los elementos de la lista devuelta por preorden() a resultado.
        return resultado

    def postorden(self) -> list["NodoArbol"]:
        """Recorre el árbol en postorden: hijos de izquierda a derecha, luego raíz.
        Devuelve: Lista de nodos en orden de visita postorden."""
        
        resultado: list["NodoArbol"] = []
        for hijo in self._hijos:
            resultado.extend(hijo.postorden())
        resultado.append(self)
        return resultado

    def postorden_inverso(self) -> list["NodoArbol"]:
        """ Recorre el árbol en postorden inverso: hijos de derecha a izquierda, luego raíz.
        Usado para la derivación por la derecha.
        Devuelve: Lista de nodos en orden de visita postorden inverso. """
        resultado: list["NodoArbol"] = []
        for hijo in reversed(self._hijos): #reversed recorre de derecha a izquierda
            resultado.extend(hijo.postorden_inverso())
        resultado.append(self)
        return resultado

    # Representación; si tiene hijos, muestra la cantidad; si no, indica que es hoja.
    
    def __repr__(self) -> str:
        if self._hijos:
            return f"NodoArbol({self._etiqueta!r}, hijos={len(self._hijos)})"
        return f"NodoArbol({self._etiqueta!r}, hoja)"
