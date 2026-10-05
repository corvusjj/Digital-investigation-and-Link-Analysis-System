import math

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import (
    QBrush,
    QFont,
    QPainter,
    QPen,
    QPolygonF,
)
from PyQt6.QtWidgets import (
    QGraphicsItem,
    QGraphicsLineItem,
    QGraphicsTextItem,
)


class GraphEdge(QGraphicsLineItem):

    def __init__(
        self,
        source_node,
        target_node,
        relation_type,
    ):
        super().__init__()

        self.source_node = source_node
        self.target_node = target_node
        self.relation_type = relation_type

        self.setZValue(-1)

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            True
        )

        self.setAcceptHoverEvents(True)

        self.setup_label()
        self.update_position()

    def setup_label(self):

        self.label = QGraphicsTextItem(
            self.relation_type
        )

        self.label.setFont(
            QFont(
                "Arial",
                8,
                QFont.Weight.Bold
            )
        )

        self.label.setDefaultTextColor(
            Qt.GlobalColor.lightGray
        )

        self.label.setParentItem(self)

    def update_position(self):

        source_center = self.source_node.sceneBoundingRect().center()
        target_center = self.target_node.sceneBoundingRect().center()

        self.setLine(
            source_center.x(),
            source_center.y(),
            target_center.x(),
            target_center.y()
        )

        self.update_label_position()

        self.update()

    def update_label_position(self):

        line = self.line()

        midpoint = QPointF(
            (line.x1() + line.x2()) / 2,
            (line.y1() + line.y2()) / 2
        )

        label_rect = self.label.boundingRect()

        self.label.setPos(
            midpoint.x() - label_rect.width() / 2,
            midpoint.y() - label_rect.height() / 2
        )

    def paint(
        self,
        painter,
        option,
        widget=None
    ):

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        line = self.line()

        if line.length() == 0:
            return

        # --------------------------------------------------
        # Line style
        # --------------------------------------------------

        if self.isSelected():

            pen = QPen(
                Qt.GlobalColor.white,
                3
            )

        else:

            pen = QPen(
                Qt.GlobalColor.gray,
                2
            )

        painter.setPen(pen)

        painter.drawLine(line)

        # --------------------------------------------------
        # Arrowhead
        # --------------------------------------------------

        self.draw_arrowhead(
            painter,
            line
        )

    def draw_arrowhead(
        self,
        painter,
        line
    ):

        end = line.p2()

        dx = line.dx()
        dy = line.dy()

        angle = math.atan2(
            dy,
            dx
        )

        arrow_size = 10

        angle1 = angle + math.pi * 0.8
        angle2 = angle - math.pi * 0.8

        point1 = QPointF(
            end.x() + arrow_size * math.cos(angle1),
            end.y() + arrow_size * math.sin(angle1)
        )

        point2 = QPointF(
            end.x() + arrow_size * math.cos(angle2),
            end.y() + arrow_size * math.sin(angle2)
        )

        arrow_head = QPolygonF([
            end,
            point1,
            point2
        ])

        if self.isSelected():

            painter.setBrush(
                QBrush(
                    Qt.GlobalColor.white
                )
            )

        else:

            painter.setBrush(
                QBrush(
                    Qt.GlobalColor.gray
                )
            )

        painter.setPen(
            Qt.PenStyle.NoPen
        )

        painter.drawPolygon(
            arrow_head
        )

    def itemChange(self, change, value):

        if (
            change
            == QGraphicsItem.GraphicsItemChange.ItemPositionChange
        ):
    
            for edge in getattr(
                self,
                "edges",
                []
            ):
                edge.update_position()
    
        return super().itemChange(
            change,
            value
        )