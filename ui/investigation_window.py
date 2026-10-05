from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QFrame,
    QFormLayout
)

from ui.entity_form import EntityForm
from ui.relation_form import RelationForm
from graph.investigation_graph import InvestigationGraph
from graph.graph_view import GraphView

class InvestigationWindow(QMainWindow):
    def __init__(self, database, case, parent=None):
        super().__init__(parent)

        self.database = database
        self.case = case

        self.investigation_graph = InvestigationGraph()

        self.setWindowTitle(
            f"{case.case_name} - Investigation"
        )

        self.resize(1400, 850)
        self.setup_ui()
        self.load_entities()
        self.load_relationships()
        self.build_graph()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # =====================================
        # SIDEBAR
        # =====================================

        sidebar = QWidget()
        sidebar.setObjectName("sidebar")

        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        # Case header
        case_label = QLabel(self.case.case_name)
        case_label.setObjectName("workspaceCaseName")

        case_id_label = QLabel(
            f"ID: {self.case.case_id}"
        )
        case_id_label.setObjectName("workspaceCaseId")

        sidebar_layout.addWidget(case_label)
        sidebar_layout.addWidget(case_id_label)

        sidebar_layout.addSpacing(25)

        # Navigation buttons
        self.entities_button = QPushButton("Entities")
        self.entities_button.setObjectName("navigationButton")

        self.relationships_button = QPushButton(
            "Relationships"
        )
        self.relationships_button.setObjectName(
            "navigationButton"
        )

        self.graph_button = QPushButton("Graph")
        self.graph_button.setObjectName(
            "navigationButton"
        )

        sidebar_layout.addWidget(
            self.entities_button
        )

        sidebar_layout.addWidget(
            self.relationships_button
        )

        sidebar_layout.addWidget(
            self.graph_button
        )

        sidebar_layout.addStretch()

        # Back button
        self.back_button = QPushButton(
            "← Back to Cases"
        )
        self.back_button.setObjectName(
            "backButton"
        )

        sidebar_layout.addWidget(
            self.back_button
        )

        # =====================================
        # CONTENT
        # =====================================

        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName(
            "workspaceContent"
        )

        # Pages
        self.entities_page = self.create_entities_page()
        self.relationships_page = (
            self.create_relationships_page()
        )
        self.graph_page = self.create_graph_page()

        self.content_stack.addWidget(
            self.entities_page
        )

        self.content_stack.addWidget(
            self.relationships_page
        )

        self.content_stack.addWidget(
            self.graph_page
        )

        # =====================================
        # MAIN LAYOUT
        # =====================================

        main_layout.addWidget(sidebar)
        main_layout.addWidget(
            self.content_stack,
            1
        )

        # =====================================
        # NAVIGATION
        # =====================================

        self.entities_button.clicked.connect(
            lambda: self.content_stack.setCurrentIndex(0)
        )

        self.relationships_button.clicked.connect(
            lambda: self.content_stack.setCurrentIndex(1)
        )

        self.graph_button.clicked.connect(
            lambda: self.content_stack.setCurrentIndex(2)
        )

        self.entity_list.itemClicked.connect(
            self.select_entity
        )

        self.add_entity_button.clicked.connect(
            self.open_entity_form
        )

        self.edit_entity_button.clicked.connect(
            self.edit_entity
        )

        self.delete_entity_button.clicked.connect(
            self.delete_entity
        )

        self.relationship_list.itemClicked.connect(
            self.select_relationship
        )

        self.add_relation_button.clicked.connect(
            self.open_relation_form
        )

        self.delete_relation_button.clicked.connect(
            self.delete_relation
        )

        self.edit_relation_button.clicked.connect(
            self.edit_relation
        )

        self.back_button.clicked.connect(
            self.back_to_cases
        )

    def load_entities(self):
        self.entity_list.clear()

        entities = self.database.get_entities(
            self.case.case_id
        )

        for entity in entities:
            item = QListWidgetItem(
                f"{entity['entity_type']}    •    "
                f"{entity['label']}    •    "
                f"{entity['date_created']}"
            )

            item.setData(1, entity["entity_id"])

            self.entity_list.addItem(item)

    def select_entity(self, item):
        entity_id = item.data(1)

        entity = self.database.get_entity(entity_id)

        if entity is None:
            return

        self.edit_entity_button.setEnabled(True)
        self.delete_entity_button.setEnabled(True)

    def open_entity_form(self):
        dialog = EntityForm(
            database=self.database,
            case_id=self.case.case_id,
            parent=self
        )

        if dialog.exec():
            self.load_entities()
            self.build_graph()

    def edit_entity(self):

        current_item = self.entity_list.currentItem()

        if current_item is None:
            return

        entity_id = current_item.data(1)

        entity = self.database.get_entity(
            entity_id
        )

        if entity is None:
            return

        dialog = EntityForm(
            database=self.database,
            case_id=self.case.case_id,
            entity=entity,
            parent=self
        )

        if dialog.exec():
            self.load_entities()
            self.build_graph()

    def delete_entity(self):

        current_item = self.entity_list.currentItem()
    
        if current_item is None:
            return
    
        entity_id = current_item.data(1)
    
        entity = self.database.get_entity(
            entity_id
        )
    
        if entity is None:
            return
    
        result = QMessageBox.question(
            self,
            "Delete Entity",
            (
                f"Are you sure you want to delete "
                f"'{entity['label']}'?"
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )
    
        if result != QMessageBox.StandardButton.Yes:
            return
    
        self.database.delete_entity(
            entity_id
        )
    
        self.load_entities()
        self.build_graph()
    
        self.edit_entity_button.setEnabled(False)
        self.delete_entity_button.setEnabled(False)

    def load_relationships(self):
        self.relationship_list.clear()

        relationships = self.database.get_relations(
            self.case.case_id
        )

        for relation in relationships:
            source = self.database.get_entity(
                relation["source_id"]
            )

            target = self.database.get_entity(
                relation["target_id"]
            )

            if source is None or target is None:
                continue

            item = QListWidgetItem(
                f"{source['label']}    "
                f"→  {relation['relation_type']}  →    "
                f"{target['label']}"
            )

            item.setData(
                1,
                relation["relation_id"]
            )

            self.relationship_list.addItem(item)

    def select_relationship(self, item):
        relation_id = item.data(1)

        relation = self.database.get_relation(
            relation_id
        )

        if relation is None:
            return

        self.edit_relation_button.setEnabled(True)
        self.delete_relation_button.setEnabled(True)

    def open_relation_form(self):
        dialog = RelationForm(
            database=self.database,
            case_id=self.case.case_id,
            parent=self
        )

        if dialog.exec():
            self.load_relationships()
            self.build_graph()

    def delete_relation(self):
        current_item = self.relationship_list.currentItem()

        if current_item is None:
            return

        relation_id = current_item.data(1)

        relation = self.database.get_relation(
            relation_id
        )

        if relation is None:
            return

        result = QMessageBox.question(
            self,
            "Delete Relationship",
            "Are you sure you want to delete this relationship?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if result != QMessageBox.StandardButton.Yes:
            return

        self.database.delete_relation(
            relation_id
        )

        self.load_relationships()
        self.build_graph()

        self.edit_relation_button.setEnabled(False)
        self.delete_relation_button.setEnabled(False)

    def edit_relation(self):
        current_item = self.relationship_list.currentItem()

        if current_item is None:
            return

        relation_id = current_item.data(1)

        relation = self.database.get_relation(
            relation_id
        )

        if relation is None:
            return

        dialog = RelationForm(
            database=self.database,
            case_id=self.case.case_id,
            relation=relation,
            parent=self
        )

        if dialog.exec():
            self.load_relationships()
            self.build_graph()

    def build_graph(self):
        entities = self.database.get_entities(
            self.case.case_id
        )

        relationships = self.database.get_relations(
            self.case.case_id
        )

        self.investigation_graph.build(
            entities,
            relationships
        )

        self.graph_view.build_graph()

    def reset_graph_layout(self):

        self.graph_view.build_graph()

    # =========================================
    # ENTITIES PAGE
    # =========================================

    def create_entities_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)

        # Header
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel("Entities")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Manage the entities associated with this investigation."
        )
        description.setObjectName("pageDescription")

        title_layout.addWidget(title)
        title_layout.addWidget(description)

        self.add_entity_button = QPushButton("+ Add Entity")
        self.add_entity_button.setObjectName("primaryButton")

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.add_entity_button)

        layout.addLayout(header_layout)

        # Entity list
        self.entity_list = QListWidget()
        self.entity_list.setObjectName("entityList")

        layout.addWidget(self.entity_list)

        # Bottom buttons
        button_layout = QHBoxLayout()

        self.edit_entity_button = QPushButton("Edit")
        self.edit_entity_button.setObjectName("secondaryButton")
        self.edit_entity_button.setEnabled(False)

        self.delete_entity_button = QPushButton("Delete")
        self.delete_entity_button.setObjectName("dangerButton")
        self.delete_entity_button.setEnabled(False)

        button_layout.addStretch()
        button_layout.addWidget(self.edit_entity_button)
        button_layout.addWidget(self.delete_entity_button)

        layout.addLayout(button_layout)

        return page

    # =========================================
    # RELATIONSHIPS PAGE
    # =========================================

    def create_relationships_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        page.setLayout(layout)

        # Header
        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel("Relationships")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Manage the relationships between entities in this investigation."
        )
        description.setObjectName("pageDescription")

        title_layout.addWidget(title)
        title_layout.addWidget(description)

        self.add_relation_button = QPushButton("+ Add Relationship")
        self.add_relation_button.setObjectName("primaryButton")

        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.add_relation_button)

        layout.addLayout(header_layout)

        # Relationship list
        self.relationship_list = QListWidget()
        self.relationship_list.setObjectName("relationshipList")

        layout.addWidget(self.relationship_list)

        # Bottom buttons
        button_layout = QHBoxLayout()

        self.edit_relation_button = QPushButton("Edit")
        self.edit_relation_button.setObjectName("secondaryButton")
        self.edit_relation_button.setEnabled(False)

        self.delete_relation_button = QPushButton("Delete")
        self.delete_relation_button.setObjectName("dangerButton")
        self.delete_relation_button.setEnabled(False)

        button_layout.addStretch()
        button_layout.addWidget(self.edit_relation_button)
        button_layout.addWidget(self.delete_relation_button)

        layout.addLayout(button_layout)

        return page

    # =========================================
    # GRAPH PAGE
    # =========================================

    def create_graph_page(self):

        page = QWidget()

        layout = QVBoxLayout()
        page.setLayout(layout)

        # =========================================
        # HEADER
        # =========================================

        header_layout = QHBoxLayout()

        title_layout = QVBoxLayout()

        title = QLabel("Graph")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Visualize and analyze the relationships "
            "within this investigation."
        )
        description.setObjectName("pageDescription")

        title_layout.addWidget(title)
        title_layout.addWidget(description)

        header_layout.addLayout(title_layout)

        header_layout.addStretch()

        # =========================================
        # GRAPH CONTROLS
        # =========================================

        self.fit_graph_button = QPushButton(
            "Fit Graph"
        )

        self.fit_graph_button.setObjectName(
            "secondaryButton"
        )

        self.zoom_in_button = QPushButton(
            "+"
        )

        self.zoom_in_button.setObjectName(
            "zoomButton"
        )

        self.zoom_out_button = QPushButton(
            "−"
        )

        self.zoom_out_button.setObjectName(
            "zoomButton"
        )

        self.reset_layout_button = QPushButton(
            "Reset Layout"
        )

        self.reset_layout_button.setObjectName(
            "secondaryButton"
        )

        header_layout.addWidget(
            self.fit_graph_button
        )

        header_layout.addWidget(
            self.zoom_out_button
        )

        header_layout.addWidget(
            self.zoom_in_button
        )

        header_layout.addWidget(
            self.reset_layout_button
        )

        layout.addLayout(header_layout)

        # =========================================
        # GRAPH VIEW
        # =========================================

        self.graph_view = GraphView(
            self.investigation_graph
        )

        self.graph_view.entity_selected_signal.connect(
            self.show_entity_details
        )

        # =========================================
        # GRAPH + DETAILS
        # =========================================

        graph_content_layout = QHBoxLayout()

        # -----------------------------------------
        # Graph
        # -----------------------------------------

        graph_content_layout.addWidget(
            self.graph_view,
            1
        )

        # -----------------------------------------
        # Entity Details
        # -----------------------------------------

        self.entity_details_panel = self.create_entity_details_panel()

        graph_content_layout.addWidget(
            self.entity_details_panel
        )

        layout.addLayout(
            graph_content_layout,
            1
        )

        # =========================================
        # BUTTON CONNECTIONS
        # =========================================

        self.fit_graph_button.clicked.connect(
            self.graph_view.fit_graph
        )

        self.zoom_in_button.clicked.connect(
            self.graph_view.zoom_in
        )

        self.zoom_out_button.clicked.connect(
            self.graph_view.zoom_out
        )

        self.reset_layout_button.clicked.connect(
            self.reset_graph_layout
        )

        return page

    def create_entity_details_panel(self):

        panel = QFrame()

        panel.setObjectName(
            "entityDetailsPanel"
        )

        panel.setMinimumWidth(280)
        panel.setMaximumWidth(360)

        layout = QVBoxLayout()

        panel.setLayout(layout)

        # =====================================
        # TITLE
        # =====================================

        title = QLabel(
            "Entity Details"
        )

        title.setObjectName(
            "formTitle"
        )

        layout.addWidget(title)

        description = QLabel(
            "Select an entity in the graph "
            "to inspect its details."
        )

        description.setObjectName(
            "formDescription"
        )

        description.setWordWrap(True)

        layout.addWidget(
            description
        )

        # =====================================
        # ENTITY TYPE
        # =====================================

        self.details_type = QLabel(
            "—"
        )

        self.details_type.setObjectName(
            "detailsType"
        )

        layout.addWidget(
            self.details_type
        )

        # =====================================
        # ENTITY LABEL
        # =====================================

        self.details_label = QLabel(
            "No entity selected"
        )

        self.details_label.setObjectName(
            "detailsLabel"
        )

        self.details_label.setWordWrap(True)

        layout.addWidget(
            self.details_label
        )

        # =====================================
        # BASIC INFORMATION
        # =====================================

        basic_title = QLabel(
            "Information"
        )

        basic_title.setObjectName(
            "formSectionTitle"
        )

        layout.addWidget(
            basic_title
        )

        form_layout = QFormLayout()

        self.details_id = QLabel("—")
        self.details_created = QLabel("—")

        self.details_id.setWordWrap(True)

        form_layout.addRow(
            "Entity ID:",
            self.details_id
        )

        form_layout.addRow(
            "Created:",
            self.details_created
        )

        layout.addLayout(
            form_layout
        )

        # =====================================
        # PROPERTIES
        # =====================================

        properties_title = QLabel(
            "Properties"
        )

        properties_title.setObjectName(
            "formSectionTitle"
        )

        layout.addWidget(
            properties_title
        )

        self.details_properties = QLabel(
            "—"
        )

        self.details_properties.setWordWrap(
            True
        )

        layout.addWidget(
            self.details_properties
        )

        layout.addStretch()

        return panel

    def show_entity_details(
        self,
        entity_id
    ):

        entity = self.database.get_entity(
            entity_id
        )
    
        if entity is None:
            return
    
        self.details_type.setText(
            entity["entity_type"]
        )
    
        self.details_label.setText(
            entity["label"]
        )
    
        self.details_id.setText(
            entity["entity_id"]
        )
    
        self.details_created.setText(
            entity["date_created"]
        )
    
        properties = entity.get(
            "properties",
            {}
        )
    
        if not properties:
        
            self.details_properties.setText(
                "No properties."
            )
    
            return
    
        property_lines = []
    
        for key, value in properties.items():
        
            property_lines.append(
                f"<b>{key}</b>: {value}"
            )
    
        self.details_properties.setText(
            "<br>".join(property_lines)
        )

    def back_to_cases(self):
        self.parent().show()
        self.close()
