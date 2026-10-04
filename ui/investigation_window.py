from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
)


class InvestigationWindow(QMainWindow):
    def __init__(self, database, case, parent=None):
        super().__init__(parent)

        self.database = database
        self.case = case

        self.setWindowTitle(
            f"{case.case_name} - Investigation"
        )

        self.resize(1400, 850)
        self.setup_ui()

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

        self.back_button.clicked.connect(
            self.back_to_cases
        )

    # =========================================
    # ENTITIES PAGE
    # =========================================

    def create_entities_page(self):
        page = QWidget()

        layout = QVBoxLayout()
        page.setLayout(layout)

        title = QLabel("Entities")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Manage the entities associated with this investigation."
        )
        description.setObjectName("pageDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        return page

    # =========================================
    # RELATIONSHIPS PAGE
    # =========================================

    def create_relationships_page(self):
        page = QWidget()

        layout = QVBoxLayout()
        page.setLayout(layout)

        title = QLabel("Relationships")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Manage relationships between investigation entities."
        )
        description.setObjectName("pageDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        return page

    # =========================================
    # GRAPH PAGE
    # =========================================

    def create_graph_page(self):
        page = QWidget()

        layout = QVBoxLayout()
        page.setLayout(layout)

        title = QLabel("Graph")
        title.setObjectName("pageTitle")

        description = QLabel(
            "Visualize and analyze the relationships "
            "within this investigation."
        )
        description.setObjectName("pageDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        return page

    def back_to_cases(self):
        self.parent().show()
        self.close()
