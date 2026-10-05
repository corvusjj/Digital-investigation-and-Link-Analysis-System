from PyQt6.QtCore import (
    QObject,
    Qt,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QBrush,
    QPen,
    QFont,
    QColor,
)
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsTextItem,
)

class GraphNodeSignals(QObject):

    clicked = pyqtSignal(str)

class GraphNode(QGraphicsRectItem):

    WIDTH = 200
    HEIGHT = 100

    def __init__(
        self,
        entity_id,
        label,
        entity_type,
        category
    ):
        super().__init__(
            0,
            0,
            self.WIDTH,
            self.HEIGHT
        )

        self.signals = GraphNodeSignals()

        self.entity_id = entity_id
        self.label = label
        self.entity_type = entity_type
        self.category = category

        self.edges = []
        self.highlighted = False
        self.dimmed = False

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable,
            True
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            True
        )

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges,
            True
        )

        self.setAcceptHoverEvents(True)

        self.setup_style()
        self.setup_text()

    def setup_style(self):
        self.setBrush(
            QBrush(Qt.GlobalColor.transparent)
        )

        self.setPen(
            QPen(
                Qt.GlobalColor.transparent
            )
        )

    def setup_text(self):

        # -----------------------------------------
        # Entity type
        # -----------------------------------------

        self.type_text = QGraphicsTextItem(
            self.entity_type,
            self
        )

        self.type_text.setFont(
            QFont(
                "Arial",
                8,
                QFont.Weight.Bold
            )
        )

        self.type_text.setDefaultTextColor(
            QColor("#9ca3af")
        )

        self.type_text.setPos(
            16,
            10
        )

        # -----------------------------------------
        # Entity label
        # -----------------------------------------

        self.label_text = QGraphicsTextItem(
            self.label,
            self
        )

        self.label_text.setFont(
            QFont(
                "Arial",
                12,
                QFont.Weight.Bold
            )
        )

        self.label_text.setDefaultTextColor(
            QColor("#f9fafb")
        )

        self.label_text.setPos(
            16,
            34
        )

        self.label_text.setTextWidth(
            self.WIDTH - 32
        )

        self.update_text_visibility()

    def update_text_visibility(self):

        if self.dimmed:
            text_color = QColor(
                "#555b66"
            )

            type_color = QColor(
                "#4b515c"
            )

        else:
            text_color = QColor(
                "#f9fafb"
            )

            type_color = QColor(
                "#9ca3af"
            )

        self.label_text.setDefaultTextColor(
            text_color
        )

        self.type_text.setDefaultTextColor(
            type_color
        )

    def paint(
        self,
        painter,
        option,
        widget=None
    ):

        painter.setRenderHint(
            painter.RenderHint.Antialiasing
        )
    
        rect = self.rect()
    
        # =========================================
        # NODE BACKGROUND
        # =========================================
    
        if self.isSelected():
        
            background_color = QColor(
                "#343a46"
            )
    
            border_color = QColor(
                "#ffffff"
            )
    
            border_width = 2
    
        elif self.highlighted:
        
            background_color = QColor(
                "#2a2e36"
            )
    
            border_color = self.get_category_color()
    
            border_width = 2

        elif self.dimmed:

            background_color = QColor(
                "#15171b"
            )

            border_color = QColor(
                "#25282e"
            )

            border_width = 1
    
        else:
        
            background_color = QColor(
                "#20232a"
            )
    
            border_color = QColor(
                "#3a3f4b"
            )
    
            border_width = 1
    
        painter.setBrush(
            QBrush(
                background_color
            )
        )
    
        painter.setPen(
            QPen(
                border_color,
                border_width
            )
        )
    
        painter.drawRoundedRect(
            rect,
            10,
            10
        )
    
        # =========================================
        # CATEGORY ACCENT
        # =========================================
    
        accent_color = self.get_category_color()
    
        painter.setBrush(
            QBrush(
                accent_color
            )
        )
    
        painter.setPen(
            QPen(
                Qt.PenStyle.NoPen
            )
        )
    
        painter.drawRoundedRect(
            0,
            0,
            4,
            self.HEIGHT,
            2,
            2
        )

    def get_category_color(self):

        colors = {
            "PEOPLE": "#4f8cff",
            "DIGITAL IDENTITY": "#a56cff",
            "COMPUTING": "#22c55e",
            "COMMUNICATION": "#f59e0b",
            "LOCATION": "#ef4444",
            "CRIMINAL": "#dc2626",
            "FINANCIAL": "#14b8a6",
            "OTHER": "#6b7280",
        }

        return QColor(
            colors.get(
                self.category,
                "#6b7280"
            )
        )

    def itemChange(self, change, value):

        result = super().itemChange(
            change,
            value
        )

        if (
            change
            == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged
        ):

            for edge in getattr(
                self,
                "edges",
                []
            ):
                edge.update_position()

        return result

    def mousePressEvent(self, event):

        if (
            event.button()
            == Qt.MouseButton.LeftButton
        ):
            self.signals.clicked.emit(
                self.entity_id
            )

        super().mousePressEvent(event)

    def set_highlighted(self, highlighted):
        self.highlighted = highlighted
        self.update()

    def set_dimmed(self, dimmed):
        self.dimmed = dimmed
        self.update_text_visibility()
        self.update()
    