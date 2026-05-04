"""
ventana_principal.py
--------------------
Interfaz estilo pastel/amigable: azul cielo, blanco, tipografía clara en español.
Incluye tooltip de ayuda para el formato de gramática y animación suave en botón.

Cambios aplicados:
  - Título de la app: "Generador de Árboles Sintácticos"
  - Encabezado: "Derivación y Árboles Sintácticos — Simon Soto"
  - Tamaños de fuente subidos de 10-11px a 12-13px proporcionalmente
  - QGroupBox::title sin fondo diferenciado (opción 3): título integrado
    al panel con CSS homogéneo, negrilla más visible
  - Sección de ayuda: sin "palabras clave", con rango <a-z> / <0-9>
  - Texto de pasos de derivación en fuente más grande (13px monoespaciado)
"""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QLineEdit,
    QRadioButton, QButtonGroup, QComboBox, QFileDialog,
    QSplitter, QScrollArea, QStatusBar, QGroupBox, QFrame,
    QMessageBox, QDialog, QToolTip
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor

from modelo.gramatica import Gramatica
from arboles.nodo_arbol import NodoArbol
from interfaz.lienzo_arbol import LienzoArbol
from interfaz.hilo_derivacion import HiloDerivacion


_GRAMATICAS_PREDEFINIDAS: dict[str, callable] = {
    "Expresiones aritméticas (a-z, 0-9, +, -, *, /, ())": Gramatica.expresiones_aritmeticas,
}

# ------------------------------------------------------------------
# Paleta azul cielo + blanco  (sin cambios de color)
# ------------------------------------------------------------------
_BG_APP      = "#DFF0F7"
_BG_PANEL    = "#FFFFFF"
_BG_INPUT    = "#F4FAFD"
_ACCENT      = "#4A9EC4"
_ACCENT_DARK = "#2E7DA6"
_ACCENT_SOFT = "#B8DCF0"
_BTN_GEN     = "#5BBF8A"
_BTN_GEN_H   = "#3DA672"
_TEXT_DARK   = "#1A3A4A"
_TEXT_MED    = "#4A7A8A"
_TEXT_LIGHT  = "#8AAABB"


# ------------------------------------------------------------------
# Botón Generar con pulso suave
# ------------------------------------------------------------------
class BotonPulso(QPushButton):
    def __init__(self, texto: str, parent=None):
        super().__init__(texto, parent)
        self._pulsando = False
        self._alpha = 255
        self._step = -6
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._aplicar_estilo_normal()

    def iniciar_pulso(self):
        self._pulsando = True
        self._timer.start(35)

    def detener_pulso(self):
        self._pulsando = False
        self._timer.stop()
        self._aplicar_estilo_normal()

    def _tick(self):
        self._alpha += self._step
        if self._alpha <= 140:
            self._step = 6
        elif self._alpha >= 255:
            self._step = -6
        a = self._alpha
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(91, 191, 138, {a});
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 13px;
                font-weight: bold;
            }}
        """)

    def _aplicar_estilo_normal(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {_BTN_GEN};
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px 16px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {_BTN_GEN_H};
            }}
            QPushButton:pressed {{
                background-color: #2E9060;
            }}
            QPushButton:disabled {{
                background-color: #B0CFC0;
                color: #FFFFFF;
            }}
        """)


# ------------------------------------------------------------------
# Ventana principal
# ------------------------------------------------------------------
class VentanaPrincipal(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self._gramatica: Gramatica | None = None
        self._hilo: HiloDerivacion | None = None
        self._configurar_ventana()
        self._construir_ui()

    def _configurar_ventana(self) -> None:
        # ✅ Título de la ventana actualizado
        self.setWindowTitle("Generador de Árboles Sintácticos")
        self.resize(1280, 820)
        self.setMinimumSize(900, 600)
        self.setStyleSheet(f"""
            QMainWindow, QWidget {{
                background-color: {_BG_APP};
                color: {_TEXT_DARK};
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }}
            QGroupBox {{
                background-color: {_BG_PANEL};
                border: 1.5px solid {_ACCENT_SOFT};
                border-radius: 12px;
                margin-top: 18px;
                padding: 12px 10px 10px 10px;
                font-size: 13px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 2px 6px;
                color: {_ACCENT_DARK};
                font-weight: 900;
                font-size: 13px;
                background-color: {_BG_PANEL};
                border: none;
            }}
            QPushButton {{
                background-color: {_ACCENT};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {_ACCENT_DARK}; }}
            QPushButton:pressed {{ background-color: #1D6080; }}
            QPushButton:disabled {{
                background-color: {_ACCENT_SOFT};
                color: white;
            }}
            QLineEdit {{
                background-color: {_BG_INPUT};
                border: 1.5px solid {_ACCENT_SOFT};
                border-radius: 8px;
                padding: 7px 10px;
                color: {_TEXT_DARK};
                font-size: 12px;
            }}
            QLineEdit:focus {{
                border-color: {_ACCENT};
            }}
            QTextEdit {{
                background-color: {_BG_INPUT};
                border: 1.5px solid {_ACCENT_SOFT};
                border-radius: 8px;
                padding: 6px;
                color: {_TEXT_DARK};
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }}
            QTextEdit:focus {{ border-color: {_ACCENT}; }}
            QComboBox {{
                background-color: {_BG_INPUT};
                border: 1.5px solid {_ACCENT_SOFT};
                border-radius: 8px;
                padding: 6px 10px;
                color: {_TEXT_DARK};
                font-size: 12px;
            }}
            QComboBox:hover {{ border-color: {_ACCENT}; }}
            QComboBox QAbstractItemView {{
                background-color: {_BG_PANEL};
                color: {_TEXT_DARK};
                selection-background-color: {_ACCENT_SOFT};
                border: 1px solid {_ACCENT_SOFT};
                border-radius: 6px;
                font-size: 12px;
            }}
            QComboBox::drop-down {{ border: none; width: 22px; }}
            QRadioButton {{
                color: {_TEXT_DARK};
                spacing: 10px;
                font-size: 12px;
                font-weight: bold;
                background-color: {_BG_INPUT};
                border: 1.5px solid {_ACCENT_SOFT};
                border-radius: 8px;
                padding: 8px 12px;
            }}
            QRadioButton:checked {{
                background-color: {_ACCENT_SOFT};
                border-color: {_ACCENT};
                color: {_ACCENT_DARK};
            }}
            QRadioButton:hover {{
                border-color: {_ACCENT};
            }}
            QRadioButton::indicator {{
                width: 14px; height: 14px;
                border: 2px solid {_ACCENT_SOFT};
                border-radius: 7px;
                background-color: white;
            }}
            QRadioButton::indicator:checked {{
                background-color: {_ACCENT};
                border-color: {_ACCENT};
            }}
            QLabel {{ color: {_TEXT_MED}; font-size: 12px; }}
            QScrollBar:vertical {{
                background: {_BG_APP}; width: 8px; border: none; border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {_ACCENT_SOFT}; border-radius: 4px; min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{ background: {_ACCENT}; }}
            QScrollBar:horizontal {{
                background: {_BG_APP}; height: 8px; border: none; border-radius: 4px;
            }}
            QScrollBar::handle:horizontal {{
                background: {_ACCENT_SOFT}; border-radius: 4px; min-width: 20px;
            }}
            QSplitter::handle {{ background-color: {_ACCENT_SOFT}; }}
            QStatusBar {{
                background-color: {_BG_PANEL};
                color: {_TEXT_LIGHT};
                font-size: 12px;
                border-top: 1px solid {_ACCENT_SOFT};
            }}
            QToolTip {{
                background-color: {_BG_PANEL};
                color: {_TEXT_DARK};
                border: 1.5px solid {_ACCENT_SOFT};
                border-radius: 8px;
                padding: 8px;
                font-size: 12px;
            }}
        """)

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _construir_ui(self) -> None:
        widget_central = QWidget()
        self.setCentralWidget(widget_central)

        layout_raiz = QVBoxLayout(widget_central)
        layout_raiz.setSpacing(0)
        layout_raiz.setContentsMargins(0, 0, 0, 0)
        layout_raiz.addWidget(self._construir_header())

        contenido = QWidget()
        lay = QHBoxLayout(contenido)
        lay.setContentsMargins(12, 10, 12, 10)
        lay.setSpacing(10)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self._construir_panel_izquierdo())
        splitter.addWidget(self._construir_panel_derecho())
        splitter.setSizes([340, 920])
        lay.addWidget(splitter)

        layout_raiz.addWidget(contenido, stretch=1)

        self._barra_estado = QStatusBar()
        self.setStatusBar(self._barra_estado)
        self._barra_estado.showMessage(
            "✨  Listo. Carga una gramática para comenzar."
        )

    def _construir_header(self) -> QWidget:
        header = QWidget()
        header.setFixedHeight(56)
        header.setStyleSheet(f"""
            background-color: {_BG_PANEL};
            border-bottom: 2px solid {_ACCENT_SOFT};
        """)
        layout = QHBoxLayout(header)
        layout.setContentsMargins(18, 0, 18, 0)

        ico = QLabel("✨")
        ico.setStyleSheet("font-size: 22px;")
        layout.addWidget(ico)

        # ✅ Encabezado actualizado
        titulo = QLabel("Derivación y Árboles Sintácticos  —  Simon Soto")
        titulo.setStyleSheet(f"""
            color: {_ACCENT_DARK};
            font-size: 15px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
        """)
        layout.addWidget(titulo)
        layout.addStretch()

        self._lbl_estado_header = QLabel("● Listo")
        self._lbl_estado_header.setStyleSheet(
            f"color: {_BTN_GEN}; font-size: 12px; font-weight: bold;"
        )
        layout.addWidget(self._lbl_estado_header)

        return header

    # ------ Panel izquierdo ------------------------------------------

    def _construir_panel_izquierdo(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 4, 0)
        layout.addWidget(self._grupo_gramatica())
        layout.addWidget(self._grupo_expresion())
        layout.addWidget(self._grupo_derivacion())
        layout.addStretch()
        return panel

    def _grupo_gramatica(self) -> QGroupBox:
        grupo = QGroupBox("📄  Gramática")
        layout = QVBoxLayout(grupo)
        layout.setSpacing(7)

        self._btn_cargar = QPushButton("📂  Cargar desde archivo…")
        self._btn_cargar.clicked.connect(self._cargar_archivo)
        layout.addWidget(self._btn_cargar)

        layout.addWidget(self._label("O seleccionar predefinida:"))
        self._combo_predefinidas = QComboBox()
        self._combo_predefinidas.addItem("— Elegir gramática predefinida —")
        for nombre in _GRAMATICAS_PREDEFINIDAS:
            self._combo_predefinidas.addItem(nombre)
        self._combo_predefinidas.currentIndexChanged.connect(self._cargar_predefinida)
        layout.addWidget(self._combo_predefinidas)

        # Fila: label + botón de ayuda
        fila_label = QHBoxLayout()
        lbl_contenido = self._label("Contenido de la gramática:")
        fila_label.addWidget(lbl_contenido)
        fila_label.addStretch()

        btn_ayuda = QPushButton("❓ ¿Cómo se escribe?")
        btn_ayuda.setStyleSheet(f"""
            QPushButton {{
                background-color: {_ACCENT_SOFT};
                color: {_ACCENT_DARK};
                border: none;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 11px;
                font-weight: bold;
            }}
            QPushButton:hover {{ background-color: {_ACCENT}; color: white; }}
        """)
        btn_ayuda.clicked.connect(self._mostrar_ayuda_gramatica)
        fila_label.addWidget(btn_ayuda)
        layout.addLayout(fila_label)

        self._txt_gramatica = QTextEdit()
        self._txt_gramatica.setPlaceholderText(
            "Carga un archivo o selecciona una gramática predefinida…\n\n"
            "Ejemplo:\n"
            "E -> E '+' T | T\n"
            "T -> T '*' F | F\n"
            "F -> '(' E ')' | 'x' | '5'"
        )
        self._txt_gramatica.setMinimumHeight(150)
        layout.addWidget(self._txt_gramatica)

        self._btn_usar_texto = QPushButton("✏️  Usar gramática del texto")
        self._btn_usar_texto.clicked.connect(self._cargar_desde_texto_manual)
        layout.addWidget(self._btn_usar_texto)

        return grupo

    def _grupo_expresion(self) -> QGroupBox:
        grupo = QGroupBox("🎯  Expresión objetivo")
        layout = QVBoxLayout(grupo)
        layout.setSpacing(7)
        layout.addWidget(self._label("Tokens separados por espacios  •  Ej: ( 5 * x ) + y"))
        self._txt_expresion = QLineEdit()
        self._txt_expresion.setPlaceholderText("ej:  ( 5 * x ) + y")
        layout.addWidget(self._txt_expresion)
        return grupo

    def _grupo_derivacion(self) -> QGroupBox:
        grupo = QGroupBox("⚙️  Opciones de Derivación")
        layout = QVBoxLayout(grupo)
        layout.setSpacing(8)

        layout.addWidget(self._label("Seleccionar tipo:"))

        self._radio_izquierda = QRadioButton("Derivación por la Izquierda")
        self._radio_izquierda.setChecked(True)
        self._radio_derecha = QRadioButton("Derivación por la Derecha")

        grupo_botones = QButtonGroup(self)
        grupo_botones.addButton(self._radio_izquierda)
        grupo_botones.addButton(self._radio_derecha)

        layout.addWidget(self._radio_izquierda)
        layout.addWidget(self._radio_derecha)

        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet(f"color: {_ACCENT_SOFT}; margin: 4px 0;")
        layout.addWidget(sep)

        self._btn_generar = BotonPulso("▶  Generar Derivación")
        self._btn_generar.setMinimumHeight(44)
        self._btn_generar.clicked.connect(self._generar_derivacion)
        layout.addWidget(self._btn_generar)

        return grupo

    # ------ Panel derecho --------------------------------------------

    def _construir_panel_derecho(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(4, 0, 0, 0)

        grp_pasos = QGroupBox("📋  Derivación Paso a Paso")
        lay_pasos = QVBoxLayout(grp_pasos)

        self._txt_pasos = QTextEdit()
        self._txt_pasos.setReadOnly(True)
        self._txt_pasos.setMinimumHeight(130)
        # ✅ Fuente más grande para los pasos de derivación
        self._txt_pasos.setStyleSheet(f"""
            QTextEdit {{
                background-color: {_BG_INPUT};
                border: 1.5px solid {_ACCENT_SOFT};
                border-radius: 8px;
                padding: 8px;
                color: {_TEXT_DARK};
                font-family: 'Courier New', monospace;
                font-size: 13px;
            }}
        """)
        self._txt_pasos.setPlaceholderText(
            "Los pasos de la derivación aparecerán aquí después de generar…"
        )
        lay_pasos.addWidget(self._txt_pasos)
        layout.addWidget(grp_pasos)

        splitter_arboles = QSplitter(Qt.Horizontal)

        grp_arbol = QGroupBox("🌳  Árbol de Derivación")
        lay_arbol = QVBoxLayout(grp_arbol)
        scroll_arbol = QScrollArea()
        scroll_arbol.setWidgetResizable(True)
        scroll_arbol.setStyleSheet("background-color: transparent; border: none;")
        self._lienzo_arbol = LienzoArbol()
        scroll_arbol.setWidget(self._lienzo_arbol)
        lay_arbol.addWidget(scroll_arbol)

        grp_ast = QGroupBox("🌳  AST (Árbol Sintáctico Abstracto)")
        lay_ast = QVBoxLayout(grp_ast)
        scroll_ast = QScrollArea()
        scroll_ast.setWidgetResizable(True)
        scroll_ast.setStyleSheet("background-color: transparent; border: none;")
        self._lienzo_ast = LienzoArbol()
        scroll_ast.setWidget(self._lienzo_ast)
        lay_ast.addWidget(scroll_ast)

        splitter_arboles.addWidget(grp_arbol)
        splitter_arboles.addWidget(grp_ast)
        layout.addWidget(splitter_arboles, stretch=1)

        return panel

    # ------------------------------------------------------------------
    # Utilidades de UI
    # ------------------------------------------------------------------

    def _label(self, texto: str) -> QLabel:
        lbl = QLabel(texto)
        lbl.setStyleSheet(f"""
            color: {_TEXT_MED};
            font-size: 12px;
            font-weight: bold;
            background-color: transparent;
        """)
        return lbl

    # ------------------------------------------------------------------
    # Popup de ayuda para el formato de gramática
    # ------------------------------------------------------------------

    def _mostrar_ayuda_gramatica(self) -> None:
        """Muestra un popup explicando el formato de gramática aceptado."""
        dlg = QDialog(self)
        dlg.setWindowTitle("¿Cómo escribir la gramática?")
        dlg.setMinimumWidth(540)
        dlg.setStyleSheet(f"""
            QDialog {{
                background-color: {_BG_PANEL};
                color: {_TEXT_DARK};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QLabel {{
                color: {_TEXT_DARK};
                font-size: 12px;
            }}
            QPushButton {{
                background-color: {_ACCENT};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 12px;
            }}
            QPushButton:hover {{ background-color: {_ACCENT_DARK}; }}
        """)

        layout = QVBoxLayout(dlg)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 16, 20, 16)

        def titulo(txt):
            lbl = QLabel(txt)
            # ✅ Títulos en negrilla y más grandes
            lbl.setStyleSheet(
                f"color: {_ACCENT_DARK}; font-weight: bold; font-size: 13px;"
            )
            return lbl

        def codigo(txt):
            lbl = QLabel(txt)
            lbl.setStyleSheet(f"""
                background-color: {_BG_INPUT};
                border: 1px solid {_ACCENT_SOFT};
                border-radius: 6px;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                color: {_TEXT_DARK};
            """)
            lbl.setWordWrap(True)
            return lbl

        def parrafo(txt):
            lbl = QLabel(txt)
            lbl.setWordWrap(True)
            lbl.setStyleSheet(f"color: {_TEXT_MED}; font-size: 12px; line-height: 1.4;")
            return lbl

        layout.addWidget(titulo("📋  Formato general"))
        layout.addWidget(parrafo(
            "Cada línea define una producción. El símbolo de la izquierda es un "
            "<b>no-terminal</b> (en mayúscula). El lado derecho va después de <b>-></b>. "
            "Las alternativas se separan con <b>|</b>."
        ))
        layout.addWidget(codigo(
            "NoTerminal -> símbolo1 símbolo2 | alternativa\n"
            "E -> E '+' T | E '-' T | T\n"
            "T -> T '*' F | F\n"
            "F -> '(' E ')' | 'x'"
        ))

        sep1 = QFrame(); sep1.setFrameShape(QFrame.HLine)
        sep1.setStyleSheet(f"color: {_ACCENT_SOFT};"); layout.addWidget(sep1)

        layout.addWidget(titulo("🔤  Terminales — cómo representarlos"))
        layout.addWidget(parrafo(
            "Los <b>terminales</b> van siempre entre <b>comillas simples</b>:"
        ))
        layout.addWidget(codigo(
            "Una letra:       'a'  'b'  'x'  'y'  'z'\n"
            "Un dígito:       '0'  '1'  '5'  '9'\n"
            "Un operador:     '+'  '-'  '*'  '/'\n"
            "Paréntesis:      '('  ')'"
        ))

        sep2 = QFrame(); sep2.setFrameShape(QFrame.HLine)
        sep2.setStyleSheet(f"color: {_ACCENT_SOFT};"); layout.addWidget(sep2)

        # ✅ Sección actualizada: sin "palabras clave", con rangos <a-z> / <0-9>
        layout.addWidget(titulo("🔠  ¿Quiero todas las letras o todos los dígitos?"))
        layout.addWidget(parrafo(
            "Puedes usar la notación de rango <b>&lt;a-z&gt;</b> o <b>&lt;0-9&gt;</b> "
            "como atajo — el sistema los expande automáticamente:"
        ))
        layout.addWidget(codigo(
            "# Todas las letras a-z como terminales:\n"
            "F -> '(' E ')' | <a-z>\n\n"
            "# Solo dígitos:\n"
            "F -> '(' E ')' | <0-9>\n\n"
            "# Letras Y dígitos juntos:\n"
            "F -> '(' E ')' | <a-z> | <0-9>"
        ))

        sep3 = QFrame(); sep3.setFrameShape(QFrame.HLine)
        sep3.setStyleSheet(f"color: {_ACCENT_SOFT};"); layout.addWidget(sep3)

        layout.addWidget(titulo("💡  Otros detalles"))
        layout.addWidget(parrafo(
            "• Las líneas que empiezan con <b>#</b> son comentarios y se ignoran.<br>"
            "• El <b>primer símbolo</b> que aparezca a la izquierda es el símbolo inicial.<br>"
            "• La expresión que ingreses debe tener los tokens <b>separados por espacios</b>:<br>"
            "  &nbsp;&nbsp;&nbsp;✅ Correcto:  <code>( 5 * x ) + y</code><br>"
            "  &nbsp;&nbsp;&nbsp;❌ Incorrecto: <code>(5*x)+y</code>"
        ))

        layout.addWidget(titulo("✏️  Ejemplo completo"))
        layout.addWidget(codigo(
            "# Gramática de expresiones aritméticas\n"
            "E -> E '+' T | E '-' T | T\n"
            "T -> T '*' F | T '/' F | F\n"
            "F -> '(' E ')' | <a-z> | <0-9>"
        ))

        btn_cerrar = QPushButton("Entendido  ✓")
        btn_cerrar.clicked.connect(dlg.accept)
        layout.addWidget(btn_cerrar, alignment=Qt.AlignRight)

        dlg.exec_()

    # ------------------------------------------------------------------
    # Slots
    # ------------------------------------------------------------------

    def _cargar_archivo(self) -> None:
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Abrir gramática", "",
            "Archivos de texto (*.txt);;Todos los archivos (*)"
        )
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            self._txt_gramatica.setPlainText(contenido)
            self._gramatica = Gramatica.desde_texto(contenido)
            valida, mensaje = self._gramatica.validar()
            if not valida:
                self._mostrar_error(f"Gramática inválida:\n{mensaje}")
                self._gramatica = None
                return
            self._barra_estado.showMessage(
                f"✅  Gramática cargada: {os.path.basename(ruta)}"
            )
        except ValueError as e:
            self._mostrar_error(f"Error de formato:\n{e}")
        except Exception as e:
            self._mostrar_error(f"No se pudo leer el archivo:\n{e}")

    def _cargar_predefinida(self, indice: int) -> None:
        if indice == 0:
            return
        nombre = self._combo_predefinidas.currentText()
        constructor = _GRAMATICAS_PREDEFINIDAS.get(nombre)
        if constructor is None:
            return
        try:
            self._gramatica = constructor()
            self._txt_gramatica.setPlainText(
                "# Gramática de expresiones aritméticas\n"
                "# Terminales: letras a-z, dígitos 0-9, operadores y paréntesis\n\n"
                "E -> E '+' T | E '-' T | T\n"
                "T -> T '*' F | T '/' F | F\n"
                "F -> '(' E ')' | <a-z> | <0-9>"
            )
            self._barra_estado.showMessage(f"✅  Gramática cargada: {nombre}")
        except Exception as e:
            self._mostrar_error(f"Error al cargar gramática predefinida:\n{e}")

    def _cargar_desde_texto_manual(self) -> None:
        texto = self._txt_gramatica.toPlainText().strip()
        if not texto:
            self._mostrar_error("El área de gramática está vacía.")
            return
        try:
            self._gramatica = Gramatica.desde_texto(texto)
            valida, mensaje = self._gramatica.validar()
            if not valida:
                self._mostrar_error(f"Gramática inválida:\n{mensaje}")
                self._gramatica = None
                return
            self._barra_estado.showMessage("✅  Gramática cargada desde el editor.")
        except ValueError as e:
            self._mostrar_error(f"Error de formato:\n{e}")

    def _generar_derivacion(self) -> None:
        if self._gramatica is None:
            self._mostrar_error("Primero carga una gramática.")
            return
        expresion = self._txt_expresion.text().strip()
        if not expresion:
            self._mostrar_error("Ingresa la expresión objetivo.")
            return

        tipo = "izquierda" if self._radio_izquierda.isChecked() else "derecha"
        self._btn_generar.setEnabled(False)
        self._btn_generar.iniciar_pulso()
        self._lbl_estado_header.setText("⏳ Calculando…")
        self._lbl_estado_header.setStyleSheet(
            f"color: {_ACCENT}; font-size: 12px; font-weight: bold;"
        )
        self._barra_estado.showMessage("⏳  Calculando derivación…")
        self._txt_pasos.setPlainText("Calculando, por favor espera…")

        self._hilo = HiloDerivacion(self._gramatica, expresion, tipo, self)
        self._hilo.resultado_listo.connect(self._mostrar_resultados)
        self._hilo.error_ocurrido.connect(self._mostrar_error_hilo)
        self._hilo.finished.connect(self._derivacion_terminada)
        self._hilo.start()

    def _derivacion_terminada(self) -> None:
        self._btn_generar.detener_pulso()
        self._btn_generar.setEnabled(True)
        self._lbl_estado_header.setText("● Listo")
        self._lbl_estado_header.setStyleSheet(
            f"color: {_BTN_GEN}; font-size: 12px; font-weight: bold;"
        )

    def _mostrar_resultados(self, pasos, raiz_arbol, raiz_ast) -> None:
        tipo = "izquierda" if self._radio_izquierda.isChecked() else "derecha"
        lineas = [f"Derivación por la {tipo}  ({len(pasos)-1} pasos)\n"]
        for i, paso in enumerate(pasos):
            prefijo = "   Inicio  ▸  " if i == 0 else f"   [{i:02d}]      ⇒  "
            lineas.append(prefijo + paso)
        self._txt_pasos.setPlainText("\n".join(lineas))
        self._lienzo_arbol.set_arbol(raiz_arbol)
        self._lienzo_ast.set_arbol(raiz_ast)
        self._barra_estado.showMessage(
            f"✅  Derivación completada — {len(pasos)-1} pasos generados."
        )

    def _mostrar_error_hilo(self, mensaje: str) -> None:
        self._mostrar_error(mensaje)
        self._txt_pasos.setPlainText(f"Error:\n{mensaje}")
        self._lienzo_arbol.set_arbol(None)
        self._lienzo_ast.set_arbol(None)
        self._barra_estado.showMessage("❌  Error al calcular la derivación.")

    def _mostrar_error(self, mensaje: str) -> None:
        QMessageBox.critical(self, "Error", mensaje)