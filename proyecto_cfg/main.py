"""Punto de entrada de la aplicación CFG Analyzer.
Inicializa la app PyQt5 y lanza la ventana principal.
Ejecución:python main.py"""
import sys #Acceso a la información del sistema
from PyQt5.QtWidgets import QApplication #Clase de PyQT5 para gestionar la aplicación
from interfaz.ventana_principal import VentanaPrincipal

def main() -> None:
    """Función principal: inicializa y ejecuta la aplicación."""
    app = QApplication(sys.argv) #lo necesita PyQT5
    app.setApplicationName("CFG Analyzer")
    app.setStyle("Fusion")  # Estilo moderno multiplataforma

    ventana = VentanaPrincipal() #Crea el objeto ventana. se contruye toda la interfaz internamente
    ventana.show() #Hace visible la pantalla

    sys.exit(app.exec_()) #Inicia el loop de eventos de la aplicación. La función exec_() bloquea hasta que la aplicación se cierre, y sys.exit asegura que el programa termine correctamente.

if __name__ == "__main__": #solo llama a main() si este archivo fue el que se ejecutó directamente
    main()