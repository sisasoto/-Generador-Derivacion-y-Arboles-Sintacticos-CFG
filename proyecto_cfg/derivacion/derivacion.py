"""Define la clase abstracta Derivacion. Establece el contrato que debencumplir todas las subclases.
Usa el módulo abc de Python para forzar la implementación del método abstracto `derivar` en todas las clases hijas."""

from abc import ABC, abstractmethod
from arboles.nodo_arbol import NodoArbol

class Derivacion(ABC):
    """Clase base abstracta para los dos tipos de derivación CFG. Define la interfaz común y provee utilidades compartidas para
    reconstruir los pasos de derivación a partir de un árbol de NodoArbol."""
    @abstractmethod
    def derivar(self, raiz: NodoArbol) -> list[str]:
        """ Genera la lista de pasos de derivación a partir del árbol. Cada string es un paso de la derivación
        Argumentos:
        raiz: La raíz del árbol de derivación construido por ArbolDerivacion.
        DEvuelve: Lista de strings, uno por cada paso de la derivación."""
        ...#no tiene cuerpo
        
    # Métodos utilitarios compartidos por las subclases


    def _hoja_o_etiqueta(self, nodo: NodoArbol) -> str:
        #Retorna la etiqueta del nodo. Si es hoja (terminal), retorna directamente su etiqueta; si tiene hijos, retorna la etiqueta como no-terminal.
        return nodo.etiqueta

    def _es_terminal(self, nodo: NodoArbol) -> bool:
        #Determina si un nodo es terminal (no tiene hijos). Argumento: Nodo a evaluar y devuelve tru si no tiene hijos.
        return len(nodo.hijos) == 0

    def _forma_sentencial(self, nodos: list[NodoArbol]) -> str:
        """ Convierte una lista de nodos en una cadena legible de la forma sentencial actual, separando los símbolos con espacios.
        Recibe: nodos: Lista de nodos que representan la forma sentencial. Devuelve: String con los símbolos separados por espacio."""
        return " ".join(n.etiqueta for n in nodos) #Generador extrayendo la etiqueta de cada nodo