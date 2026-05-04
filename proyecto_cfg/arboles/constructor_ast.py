"""clase ConstructorAST, que simplifica el árbol de derivación para obtener el Árbol Sintáctico Abstracto (AST).
Reglas de simplificación aplicadas:
  1. Elimina nodos con un único hijo (cadenas de no-terminales).
  2. Elimina nodos de puntuación como paréntesis '(' y ')'.
  3. Convierte los operadores en raíces de sus subárboles.
Trabaja exclusivamente con objetos NodoArbol."""

from arboles.nodo_arbol import NodoArbol
# Operadores reconocidos para ser elevados a raíz de subárbol
_OPERADORES: frozenset[str] = frozenset({ #frozenset es un conjunto inmutable.
    "+", "-", "*", "/", "^",
    "and", "or", "not",
    "=", "==", "!=", "<", ">", "<=", ">=",
})
# Tokens de puntuación que se eliminan del AST
_PUNTUACION: frozenset[str] = frozenset({"(", ")", "[", "]", "{", "}", ","})

class ConstructorAST:
    #Metódo público. Recibe la raíz del árbol completo y devuelve la raíz del AST simplificado.
    def construir(self, raiz: NodoArbol) -> NodoArbol:
        return self._simplificar(raiz)

    # Lógica de simplificación (recursiva)
    #Recibe un nodo, lo analiza, y devuelve el nodo simplificado o None
    def _simplificar(self, nodo: NodoArbol) -> NodoArbol | None:
        # Caso 1: nodo hoja
        if nodo.es_hoja():
            if nodo.etiqueta in _PUNTUACION:
                return None  # Eliminar puntuación
            return NodoArbol(nodo.etiqueta)  # Mantener terminal relevante

        # Simplificar todos los hijos recursivamente
        hijos_simplificados: list[NodoArbol] = []
        for hijo in nodo.hijos:
            resultado = self._simplificar(hijo)
            if resultado is not None:
                hijos_simplificados.append(resultado)

        # Caso 2: nodo con un único hijo → eliminamos el nodo intermedio
        if len(hijos_simplificados) == 1:
            return hijos_simplificados[0]

        # Caso 3: ningún hijo útil → nodo se convierte en hoja
        if not hijos_simplificados:
            return NodoArbol(nodo.etiqueta)

        # Caso 4: buscar operador entre los hijos para elevar a raíz
        operador = self._encontrar_operador(hijos_simplificados)
        if operador is not None:
            # Elevar el operador: los demás hijos se vuelven sus hijos
            otros_hijos = [h for h in hijos_simplificados
                           if h.etiqueta != operador.etiqueta] #dame todos los hijos excepto el operador
            # Aplanar: si un hijo ya es el mismo operador, absorber
            hijos_finales: list[NodoArbol] = []
            for h in otros_hijos:
                hijos_finales.append(h)
            return NodoArbol(operador.etiqueta, hijos_finales)

        # Caso 5: nodo con múltiples hijos sin operador reconocible
        return NodoArbol(nodo.etiqueta, hijos_simplificados)

    def _encontrar_operador(self,
                            hijos: list[NodoArbol]) -> NodoArbol | None:
        """Busca el primer nodo hoja entre los hijos que sea un operador reconocido.
        Argumentos: hijos: Lista de nodos hijos ya simplificados. devuelve:El nodo operador si se encuentra, None en caso contrario."""
        for hijo in hijos:
            if hijo.es_hoja() and hijo.etiqueta in _OPERADORES:
                return hijo
        return None