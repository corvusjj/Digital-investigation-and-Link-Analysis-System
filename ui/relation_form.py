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
        relation=None,
        parent=None
    ):
        super().__init__(parent)

        self.database = database
        self.case_id = case_id
        self.relation = relation

        self.setWindowTitle("Add Relationship")
        self.resize(500, 350)

        self.setup_ui()
        self.load_entities()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel(
            "Edit Relationship"
            if self.relation
            else
            "Add Relationship"
        )
        title.setObjectName("formTitle")

        description = QLabel(
            "Edit the relationship between entities "
            "in this investigation."
            if self.relation
            else
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
            "Save Changes"
            if self.relation
            else
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
        
            if self.relation is None:
            
                # Create new relationship
                relation = RelationFactory.create(
                    relation_type,
                    source_id,
                    target_id
                )
    
                self.database.create_relation(
                    relation,
                    self.case_id
                )
    
            else:
            
                # Update existing relationship
                self.database.update_relation(
                    self.relation["relation_id"],
                    relation_type,
                    source_id,
                    target_id
                )
    
        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not save relationship:\n\n"
                f"{error}"
            )
            return
    
        self.accept()

    def load_relation(self):
        relation_type = self.relation["relation_type"]
        source_id = self.relation["source_id"]
        target_id = self.relation["target_id"]

        relation_type_index = (
            self.relation_type_combo.findText(
                relation_type
            )
        )

        if relation_type_index >= 0:
            self.relation_type_combo.setCurrentIndex(
                relation_type_index
            )

        source_index = (
            self.source_combo.findData(
                source_id
            )
        )

        if source_index >= 0:
            self.source_combo.setCurrentIndex(
                source_index
            )

        target_index = (
            self.target_combo.findData(
                target_id
            )
        )

        if target_index >= 0:
            self.target_combo.setCurrentIndex(
                target_index
            )