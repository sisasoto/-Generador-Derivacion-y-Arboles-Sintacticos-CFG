"""Define la clase Produccion, que representa una regla de producción de la forma A → α, donde A es un no-terminal y α es una secuencia de símbolos (terminales y/o no-terminales)."""
from modelo.simbolo import Simbolo #importamos la clase Simbolo para usarla en la definición de Produccion
class Produccion:

    def __init__(self, izquierda: Simbolo, derecha: list[Simbolo]) -> None:
        """Constructor que recibe izq que es un objeto de simbolo y der que es una lista de objetos de simbolo.
            izquierda: El no-terminal que se expande.
            derecha: La lista de símbolos resultante de la expansión."""
        self._izquierda: Simbolo = izquierda
        self._derecha: list[Simbolo] = derecha

    @property
    def izquierda(self) -> Simbolo:
        #Retorna el no-terminal del lado izquierdo no modifiable.
        return self._izquierda

    @property
    def derecha(self) -> list[Simbolo]:
        #Retorna la lista de símbolos del lado derecho.
        return self._derecha

    def __repr__(self) -> str:
        rhs = " ".join(s.nombre for s in self._derecha) #Es un generador. Recorre la lista y transforma cada elemento. para cada simbolo s en derecha, toma su nombre y lo une con espacios.
        return f"Produccion({self._izquierda.nombre} → {rhs})" #Me generea el objeto Produccion con el Strinn. ejemplo: Produccion(E → E + T)
    
    def __eq__(self, other: object) -> bool: #Compara dos producciones por su izquierda y derecha.
        if isinstance(other, Produccion):
            return (self._izquierda == other._izquierda and
                    self._derecha == other._derecha)
        return False