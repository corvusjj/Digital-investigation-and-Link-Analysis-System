import math

import networkx as nx

from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
)
from PyQt6.QtGui import QBrush, QColor
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
)

from graph.graph_node import GraphNode
from graph.graph_edge import GraphEdge


class GraphView(QGraphicsView):

    entity_selected_signal = pyqtSignal(str)

    def __init__(
        self,
        investigation_graph,
        parent=None
    ):
        super().__init__(parent)

        self.investigation_graph = investigation_graph

        self.scene = QGraphicsScene(self)

        self.setScene(self.scene)

        self.nodes = {}
        self.edges = []

        self.setup_view()
        self.setup_scene()

    # --------------------------------------------------
    # View setup
    # --------------------------------------------------

    def setup_view(self):

        self.setRenderHint(
            self.renderHints().Antialiasing
        )

        self.setDragMode(
            QGraphicsView.DragMode.ScrollHandDrag
        )

        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )

        self.setBackgroundBrush(
            QBrush(
                QColor("#15171c")
            )
        )

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

    # --------------------------------------------------
    # Scene setup
    # --------------------------------------------------

    def setup_scene(self):

        self.scene.setSceneRect(
            -2000,
            -2000,
            4000,
            4000
        )

    # --------------------------------------------------
    # Build graph
    # --------------------------------------------------

    def build_graph(self):

        self.clear_graph()

        graph = self.investigation_graph.get_graph()

        if graph.number_of_nodes() == 0:
            return

        self.create_nodes(graph)

        self.create_edges(graph)

        self.layout_nodes(graph)

        self.fit_graph()

    # --------------------------------------------------
    # Create nodes
    # --------------------------------------------------

    def create_nodes(self, graph):

        for entity_id, data in graph.nodes(data=True):

            node = GraphNode(
                entity_id=entity_id,
                label=data["label"],
                entity_type=data["entity_type"],
                category=data["category"]
            )

            node.signals.clicked.connect(
                self.entity_selected
            )

            self.scene.addItem(node)

            self.nodes[entity_id] = node

    # --------------------------------------------------
    # Create edges
    # --------------------------------------------------

    def create_edges(self, graph):

        for source_id, target_id, data in graph.edges(
            data=True
        ):

            source_node = self.nodes.get(
                source_id
            )

            target_node = self.nodes.get(
                target_id
            )

            if source_node is None:
                continue

            if target_node is None:
                continue

            edge = GraphEdge(
                source_node=source_node,
                target_node=target_node,
                relation_type=data[
                    "relation_type"
                ]
            )

            self.scene.addItem(edge)

            source_node.edges.append(edge)
            target_node.edges.append(edge)

            self.edges.append(edge)

    # --------------------------------------------------
    # Layout
    # --------------------------------------------------

    def layout_nodes(self, graph):

        positions = nx.spring_layout(
            graph,
            seed=42,
            k=2.5,
            iterations=100
        )

        for entity_id, position in positions.items():

            node = self.nodes.get(
                entity_id
            )

            if node is None:
                continue

            x = position[0] * 700
            y = position[1] * 700

            node.setPos(
                x,
                y
            )

        self.update_edges()

    # --------------------------------------------------
    # Update edges
    # --------------------------------------------------

    def update_edges(self):

        for edge in self.edges:

            edge.update_position()

    # --------------------------------------------------
    # Clear
    # --------------------------------------------------

    def clear_graph(self):

        self.scene.clear()

        self.nodes.clear()
        self.edges.clear()

    # --------------------------------------------------
    # Fit graph
    # --------------------------------------------------

    def fit_graph(self):

        if not self.nodes:
            return

        self.fitInView(
            self.scene.itemsBoundingRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )

    # --------------------------------------------------
    # Zoom
    # --------------------------------------------------

    def wheelEvent(self, event):

        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:

            factor = zoom_in_factor

        else:

            factor = zoom_out_factor

        self.scale(
            factor,
            factor
        )

    # --------------------------------------------------
    # Double click
    # --------------------------------------------------

    def mouseDoubleClickEvent(self, event):

        if (
            event.button()
            == Qt.MouseButton.MiddleButton
        ):

            self.fit_graph()

            return

        super().mouseDoubleClickEvent(
            event
        )

    # --------------------------------------------------
    # Zoom
    # --------------------------------------------------

    def zoom_in(self):

        self.scale(
            1.2,
            1.2
        )

    def zoom_out(self):

        self.scale(
            1 / 1.2,
            1 / 1.2
        )

    def entity_selected(
        self,
        entity_id
    ):

        self.highlight_entity(
            entity_id
        )
    
        self.entity_selected_signal.emit(
            entity_id
        )

    def highlight_entity(
        self,
        entity_id
    ):

        # =========================================
        # RESET EVERYTHING
        # =========================================
    
        for node in self.nodes.values():
        
            node.set_highlighted(
                False
            )
    
        for edge in self.edges:
        
            edge.set_highlighted(
                False
            )
    
        # =========================================
        # FIND SELECTED NODE
        # =========================================
    
        selected_node = self.nodes.get(
            entity_id
        )
    
        if selected_node is None:
            return
    
        # =========================================
        # HIGHLIGHT SELECTED NODE
        # =========================================
    
        selected_node.set_highlighted(
            True
        )
    
        # =========================================
        # HIGHLIGHT CONNECTED NODES + EDGES
        # =========================================
    
        for edge in self.edges:
        
            if (
                edge.source_node
                is selected_node
                or
                edge.target_node
                is selected_node
            ):
    
                edge.set_highlighted(
                    True
                )
    
                if (
                    edge.source_node
                    is not selected_node
                ):
    
                    edge.source_node.set_highlighted(
                        True
                    )
    
                if (
                    edge.target_node
                    is not selected_node
                ):
    
                    edge.target_node.set_highlighted(
                        True
                    )