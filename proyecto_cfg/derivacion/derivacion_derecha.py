"""
En cada paso se expande el NO-TERMINAL más a la derecha de la
forma sentencial actual. Esto corresponde a un recorrido en
POSTORDEN INVERSO del árbol: hijos de derecha a izquierda, luego raíz.
"""
from derivacion.derivacion import Derivacion
from arboles.nodo_arbol import NodoArbol

class DerivacionDerecha(Derivacion):
    """
    Genera los pasos de la derivación derecha a partir del árbol.
    Estrategia:
        1. Empezamos con la forma sentencial inicial: [raiz].
        2. Buscamos el último no-terminal (nodo con hijos) de derecha a izquierda.
        3. Lo reemplazamos por sus hijos en la forma sentencial.
        4. Registramos el estado actual como un paso.
        5. Repetimos hasta que no haya más no-terminales.
    """
    def derivar(self, raiz: NodoArbol) -> list[str]:
        """
        Genera los pasos de la derivación derecha.

        Args:
            raiz: Raíz del árbol de derivación.

        Returns:
            Lista de strings con cada forma sentencial del proceso,
            comenzando con el símbolo inicial y terminando con la
            expresión completamente derivada.
        """
        pasos: list[str] = []

        # Estado inicial: solo el símbolo inicial
        forma_sentencial: list[NodoArbol] = [raiz]
        pasos.append(self._forma_sentencial(forma_sentencial))

        # Expandir iterativamente el último no-terminal de derecha a izquierda
        while True:
            idx = self._ultimo_no_terminal(forma_sentencial)
            if idx == -1:
                break  # Todos son terminales: derivación completa

            nodo = forma_sentencial[idx]
            # Reemplazar el no-terminal por sus hijos
            forma_sentencial = (
                forma_sentencial[:idx] +
                nodo.hijos +
                forma_sentencial[idx + 1:]
            )
            pasos.append(self._forma_sentencial(forma_sentencial))

        return pasos

    # ------------------------------------------------------------------
    # Método auxiliar
    # ------------------------------------------------------------------

    def _ultimo_no_terminal(self, forma: list[NodoArbol]) -> int:
        """
        Encuentra el índice del último no-terminal (nodo con hijos)
        en la forma sentencial actual.

        Args:
            forma: Lista de nodos de la forma sentencial.

        Returns:
            Índice del último no-terminal, o -1 si todos son terminales.
        """
        for i in range(len(forma) - 1, -1, -1):
            if not forma[i].es_hoja():
                return i
        return -1
