from PyQt6.QtCore import Qt
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


class GraphNode(QGraphicsRectItem):

    WIDTH = 180
    HEIGHT = 90

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

        self.entity_id = entity_id
        self.label = label
        self.entity_type = entity_type
        self.category = category

        self.edges = []

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

        # Entity type
        self.type_text = QGraphicsTextItem(
            self.entity_type,
            self
        )

        self.type_text.setFont(
            QFont("Arial", 8, QFont.Weight.Bold)
        )

        self.type_text.setDefaultTextColor(
            Qt.GlobalColor.lightGray
        )

        self.type_text.setPos(
            12,
            10
        )

        # Entity label
        self.label_text = QGraphicsTextItem(
            self.label,
            self
        )

        self.label_text.setFont(
            QFont("Arial", 12, QFont.Weight.Bold)
        )

        self.label_text.setDefaultTextColor(
            Qt.GlobalColor.white
        )

        self.label_text.setPos(
            12,
            32
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

        # -----------------------------------------
        # Node background
        # -----------------------------------------

        painter.setBrush(
            QBrush(
                QColor("#20232a")
            )
        )

        painter.setPen(
            QPen(
                QColor("#3a3f4b"),
                1
            )
        )

        painter.drawRoundedRect(
            rect,
            10,
            10
        )

        # -----------------------------------------
        # Category accent
        # -----------------------------------------

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
            5,
            self.HEIGHT,
            3,
            3
        )

        # -----------------------------------------
        # Selection
        # -----------------------------------------

        if self.isSelected():

            painter.setBrush(
                Qt.BrushStyle.NoBrush
            )

            painter.setPen(
                QPen(
                    QColor("#ffffff"),
                    2
                )
            )

            painter.drawRoundedRect(
                rect.adjusted(
                    1,
                    1,
                    -1,
                    -1
                ),
                10,
                10
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