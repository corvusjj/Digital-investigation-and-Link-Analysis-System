import math

from PyQt6.QtWidgets import QGraphicsRectItem
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

        self.highlighted = False

        self.setZValue(-1)

        self.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable,
            True
        )

        self.setAcceptHoverEvents(True)

        self.setup_label()
        self.update_position()

    def setup_label(self):

        self.label_background = QGraphicsRectItem(
            self
        )

        self.label_background.setBrush(
            QBrush(
                Qt.GlobalColor.darkGray
            )
        )

        self.label_background.setPen(
            QPen(Qt.PenStyle.NoPen)
        )

        self.label_background.setZValue(1)

        self.label = QGraphicsTextItem(
            self.relation_type,
            self
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

        self.label.setZValue(2)

    def update_position(self):

        source_rect = self.source_node.sceneBoundingRect()
        target_rect = self.target_node.sceneBoundingRect()

        source_center = source_rect.center()
        target_center = target_rect.center()

        dx = target_center.x() - source_center.x()
        dy = target_center.y() - source_center.y()

        if dx == 0 and dy == 0:
            return

        # Find where the line intersects the source node
        source_scale = self.get_rect_intersection(
            source_rect,
            dx,
            dy
        )

        # Find where the line intersects the target node
        target_scale = self.get_rect_intersection(
            target_rect,
            -dx,
            -dy
        )

        source_point = QPointF(
            source_center.x() + dx * source_scale,
            source_center.y() + dy * source_scale
        )

        target_point = QPointF(
            target_center.x() - dx * target_scale,
            target_center.y() - dy * target_scale
        )

        self.setLine(
            source_point.x(),
            source_point.y(),
            target_point.x(),
            target_point.y()
        )

        self.update_label_position()

        self.update()

    def get_rect_intersection(
        self,
        rect,
        dx,
        dy
    ):
        half_width = rect.width() / 2
        half_height = rect.height() / 2

        if dx == 0:
            return half_height / abs(dy)

        if dy == 0:
            return half_width / abs(dx)

        scale_x = half_width / abs(dx)
        scale_y = half_height / abs(dy)

        return min(
            scale_x,
            scale_y
        )

    def update_label_position(self):

        line = self.line()

        midpoint = QPointF(
            (line.x1() + line.x2()) / 2,
            (line.y1() + line.y2()) / 2
        )

        label_rect = self.label.boundingRect()

        padding = 4

        self.label_background.setRect(
            midpoint.x()
            - label_rect.width() / 2
            - padding,

            midpoint.y()
            - label_rect.height() / 2
            - padding / 2,

            label_rect.width()
            + padding * 2,

            label_rect.height()
            + padding
        )

        self.label.setPos(
            midpoint.x()
            - label_rect.width() / 2,

            midpoint.y()
            - label_rect.height() / 2
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
        elif self.highlighted:

            pen = QPen(
                Qt.GlobalColor.lightGray,
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

            brush = QBrush(
                Qt.GlobalColor.white
            )

        else:

            brush = QBrush(
                Qt.GlobalColor.gray
            )

        painter.setBrush(brush)

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

    def set_highlighted(self, highlighted):

        self.highlighted = highlighted

        self.update()