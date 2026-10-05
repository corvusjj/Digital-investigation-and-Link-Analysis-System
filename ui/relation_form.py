from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QFormLayout,
    QMessageBox,
)

from registry.relation_registry import RELATION_TYPES
from factories.relation_factory import RelationFactory

class RelationForm(QDialog):

    def __init__(
        self,
        database,
        case_id,
        parent=None
    ):
        super().__init__(parent)

        self.database = database
        self.case_id = case_id

        self.setWindowTitle("Add Relationship")
        self.resize(500, 350)

        self.setup_ui()
        self.load_entities()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Add Relationship")
        title.setObjectName("formTitle")

        description = QLabel(
            "Create a relationship between two entities "
            "in this investigation."
        )
        description.setObjectName("formDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        form = QFormLayout()

        # Relationship type
        self.relation_type_combo = QComboBox()

        self.relation_type_combo.addItems(
            RELATION_TYPES
        )

        form.addRow(
            "Relationship Type:",
            self.relation_type_combo
        )

        # Source entity
        self.source_combo = QComboBox()

        form.addRow(
            "Source Entity:",
            self.source_combo
        )

        # Target entity
        self.target_combo = QComboBox()

        form.addRow(
            "Target Entity:",
            self.target_combo
        )

        layout.addLayout(form)
        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName(
            "secondaryButton"
        )

        self.create_button = QPushButton(
            "Create Relationship"
        )
        self.create_button.setObjectName(
            "primaryButton"
        )

        button_layout.addStretch()
        button_layout.addWidget(
            self.cancel_button
        )
        button_layout.addWidget(
            self.create_button
        )

        layout.addLayout(button_layout)

        self.cancel_button.clicked.connect(
            self.reject
        )

        self.create_button.clicked.connect(
            self.create_relation
        )

    def load_entities(self):
        entities = self.database.get_entities(
            self.case_id
        )

        for entity in entities:
            display_text = (
                f"{entity['label']} "
                f"({entity['entity_type']})"
            )

            self.source_combo.addItem(
                display_text,
                entity["entity_id"]
            )

            self.target_combo.addItem(
                display_text,
                entity["entity_id"]
            )

    def create_relation(self):
        relation_type = (
            self.relation_type_combo.currentText()
        )

        source_id = (
            self.source_combo.currentData()
        )

        target_id = (
            self.target_combo.currentData()
        )

        if source_id is None or target_id is None:
            QMessageBox.warning(
                self,
                "Missing Entity",
                "Please select both a source "
                "and target entity."
            )
            return

        if source_id == target_id:
            QMessageBox.warning(
                self,
                "Invalid Relationship",
                "The source and target entities "
                "cannot be the same."
            )
            return

        try:
            relation = RelationFactory.create(
                relation_type,
                source_id,
                target_id
            )

            self.database.create_relation(
                relation,
                self.case_id
            )

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not create relationship:\n\n"
                f"{error}"
            )
            return

        self.accept()