"""Define la clase HiloDerivacion, que hereda de QThread.
Ejecuta en un hilo separado todo el trabajo pesado:
  - Construcción del árbol con NLTK (a través de ArbolDerivacion)
  - Extracción de los pasos de derivación
  - Construcción del AST
Emite señales PyQt5 al terminar o al encontrar un error, para que VentanaPrincipal actualice la interfaz sin bloquearla."""

from PyQt5.QtCore import QThread, pyqtSignal #ultimos para el hilo y para las señales
from modelo.gramatica import Gramatica
from arboles.arbol_derivacion import ArbolDerivacion
from arboles.nodo_arbol import NodoArbol
from arboles.constructor_ast import ConstructorAST
from derivacion.derivacion_izquierda import DerivacionIzquierda
from derivacion.derivacion_derecha import DerivacionDerecha


class HiloDerivacion(QThread):
    """Hilo de trabajo que calcula la derivación y los árboles.
señales:resultado_listo: Emitido con (pasos, raiz_arbol, raiz_ast) al terminar.
error_ocurrido:  Emitido con un mensaje de error si falla."""

    # Señal emitida al completar el trabajo:
    # (pasos: list[str], raiz_derivacion: NodoArbol, raiz_ast: NodoArbol)
    resultado_listo = pyqtSignal(list, object, object)

    # Señal emitida si ocurre cualquier error
    error_ocurrido = pyqtSignal(str)

    def __init__(self,
                 gramatica: Gramatica,
                 expresion: str,
                 tipo_derivacion: str,
                 parent=None) -> None:
        #Constructor que recibe gram,expre,tipderi y parent que es la que gestiona la memoria
        super().__init__(parent)
        self._gramatica: Gramatica = gramatica
        self._expresion: str = expresion
        self._tipo: str = tipo_derivacion

    def run(self) -> None:
        """
        Método ejecutado en el hilo secundario.
        Construye el árbol, calcula la derivación y el AST.
        Emite resultado_listo o error_ocurrido según el resultado.
        """
        try:
            # 1. Construir el árbol de derivación usando NLTK (encapsulado)
            arbol = ArbolDerivacion(self._gramatica, self._expresion)
            raiz: NodoArbol = arbol.raiz  # Lanza ValueError si no hay árbol

            # 2. Calcular los pasos de derivación según el tipo elegido
            if self._tipo == "izquierda":
                derivador = DerivacionIzquierda()
            else:
                derivador = DerivacionDerecha()

            pasos: list[str] = derivador.derivar(raiz)

            # 3. Construir el AST simplificado
            constructor = ConstructorAST()
            raiz_ast: NodoArbol = constructor.construir(raiz)

            # 4. Emitir la señal con los tres resultados
            self.resultado_listo.emit(pasos, raiz, raiz_ast)

        except ValueError as e:
            self.error_ocurrido.emit(str(e))
        except RuntimeError as e:
            self.error_ocurrido.emit(str(e))
        except Exception as e:
            self.error_ocurrido.emit(f"Error inesperado: {e}")