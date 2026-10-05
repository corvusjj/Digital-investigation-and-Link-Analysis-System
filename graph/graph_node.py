from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPen, QFont
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

        # Main card
        painter.setBrush(
            QBrush(
                Qt.GlobalColor.darkGray
            )
        )

        painter.setPen(
            QPen(
                Qt.GlobalColor.gray,
                1
            )
        )

        painter.drawRoundedRect(
            rect,
            10,
            10
        )

        # Selection border
        if self.isSelected():

            painter.setPen(
                QPen(
                    Qt.GlobalColor.white,
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