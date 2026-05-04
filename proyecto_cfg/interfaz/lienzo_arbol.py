#lienzo_arbol.py — Nodos pastel suaves: rosa (terminales), azul lavanda (no-terminales).

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt
from arboles.nodo_arbol import NodoArbol

_RADIO_NODO  = 26        
_SEP_H       = 62        # Separación horizontal 
_SEP_V       = 76        # Separación vertical
_MARGEN      = 48

# Qcolor es la clase que permite representar los colores
_COLOR_NT        = QColor("#B5D5F5")   # Azul lavanda pastel (no-terminales)
_COLOR_NT_BORDE  = QColor("#7AAAD0")   # Azul medio
_COLOR_T         = QColor("#F9C8D4")   # Rosa pastel (terminales)
_COLOR_T_BORDE   = QColor("#E08090")   # Rosa oscuro
_COLOR_TEXTO     = QColor("#2A4A5A")   # Azul oscuro (texto legible)
_COLOR_LINEA     = QColor("#A8C8E0")   # Azul suave (líneas)
_COLOR_FONDO     = QColor("#F0F8FF")   # Blanco azulado (fondo canvas)


class LienzoArbol(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._raiz: NodoArbol | None = None
        self._posiciones: dict[int, tuple[int, int]] = {} #Guarda las posicion de cada nodo con un id y la coordenadas
        self.setMinimumSize(400, 300)
        self.setStyleSheet(f"background-color: {_COLOR_FONDO.name()}; border-radius: 8px;")

    def set_arbol(self, raiz: NodoArbol | None) -> None: #Recibe el arbol, guarda la raiz y calcula las posiciones de los nodos para el dibujo. Luego actualiza el lienzo.
        self._raiz = raiz
        self._posiciones = {}
        if raiz is not None:
            self._calcular_posiciones()
            if self._posiciones:
                max_x = max(x for x, _ in self._posiciones.values()) + _RADIO_NODO + _MARGEN #recorre las coordenadas y extrae la x para calcular el tamaño maximo
                max_y = max(y for _, y in self._posiciones.values()) + _RADIO_NODO + _MARGEN
                self.setMinimumSize(max(400, max_x), max(300, max_y))
        self.update()

    def _calcular_posiciones(self) -> None:
        if not self._raiz:
            return
        hojas = self._listar_hojas(self._raiz)
        idx = {id(h): i for i, h in enumerate(hojas)}
        self._asignar(self._raiz, idx, 0)
        self._centrar()

    def _listar_hojas(self, n: NodoArbol) -> list: #Recolecta las hojas en orden izq a der
        if n.es_hoja():
            return [n]
        r = []
        for h in n.hijos:
            r.extend(self._listar_hojas(h))
        return r

    def _asignar(self, n: NodoArbol, idx: dict, nivel: int) -> int:
        y = nivel * _SEP_V + _MARGEN
        if n.es_hoja():
            x = _MARGEN + idx.get(id(n), 0) * _SEP_H + _SEP_H // 2
        else:
            xs = [self._asignar(h, idx, nivel + 1) for h in n.hijos]
            x = sum(xs) // len(xs)
        self._posiciones[id(n)] = (x, y)
        return x

    def _centrar(self) -> None:
        if not self._posiciones:
            return
        ancho = max(self.width(), 400)
        min_x = min(x for x, _ in self._posiciones.values())
        max_x = max(x for x, _ in self._posiciones.values())
        off = (ancho - (max_x - min_x)) // 2 - min_x
        self._posiciones = {k: (x + off, y) for k, (x, y) in self._posiciones.items()}

    def paintEvent(self, event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), _COLOR_FONDO)

        if self._raiz is None:
            painter.setPen(QColor("#B0C8D8"))
            painter.setFont(QFont("Segoe UI", 11))   # ✅ Texto vacío más grande
            painter.drawText(self.rect(), Qt.AlignCenter,
                             "Sin árbol generado\nGenera una derivación para visualizar")
            return

        self._calcular_posiciones()
        self._dibujar_lineas(painter, self._raiz)
        self._dibujar_nodos(painter, self._raiz)

    def resizeEvent(self, event) -> None:
        self.update()
        super().resizeEvent(event)

    def _dibujar_lineas(self, painter: QPainter, nodo: NodoArbol) -> None:
        if id(nodo) not in self._posiciones:
            return
        px, py = self._posiciones[id(nodo)]
        pen = QPen(_COLOR_LINEA, 2)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        for hijo in nodo.hijos:
            if id(hijo) in self._posiciones:
                cx, cy = self._posiciones[id(hijo)]
                painter.drawLine(px, py, cx, cy)
            self._dibujar_lineas(painter, hijo)

    def _dibujar_nodos(self, painter: QPainter, nodo: NodoArbol) -> None:
        if id(nodo) not in self._posiciones:
            return
        x, y = self._posiciones[id(nodo)]

        if nodo.es_hoja():
            color_fill  = _COLOR_T
            color_borde = _COLOR_T_BORDE
        else:
            color_fill  = _COLOR_NT
            color_borde = _COLOR_NT_BORDE

        # Sombra suave
        painter.setBrush(QBrush(QColor(0, 0, 0, 18)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(x - _RADIO_NODO + 2, y - _RADIO_NODO + 3,
                             _RADIO_NODO * 2, _RADIO_NODO * 2)

        # Nodo
        painter.setBrush(QBrush(color_fill))
        painter.setPen(QPen(color_borde, 2))
        painter.drawEllipse(x - _RADIO_NODO, y - _RADIO_NODO,
                             _RADIO_NODO * 2, _RADIO_NODO * 2)

        painter.setPen(QPen(_COLOR_TEXTO))
        painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
        painter.drawText(x - _RADIO_NODO, y - _RADIO_NODO,
                          _RADIO_NODO * 2, _RADIO_NODO * 2,
                          Qt.AlignCenter, nodo.etiqueta)

        for hijo in nodo.hijos:
            self._dibujar_nodos(painter, hijo)
