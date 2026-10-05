import inspect

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QFormLayout,
    QMessageBox,
)

from registry.entity_registry import ENTITY_REGISTRY
from factories.entity_factory import EntityFactory


class EntityForm(QDialog):

    def __init__(self, database, case_id, entity=None, parent=None):
        super().__init__(parent)

        self.database = database
        self.case_id = case_id
        self.entity = entity

        self.property_inputs = {}

        self.setWindowTitle("Add Entity")
        self.resize(500, 600)

        self.setup_ui()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def setup_ui(self):

        layout = QVBoxLayout()
        self.setLayout(layout)

        # -----------------------------
        # Title
        # -----------------------------

        title = QLabel(
            "Edit the entity associated with this investigation."
            if self.entity
            else
            "Create an entity for this investigation."
        )
        title.setObjectName("formTitle")

        description = QLabel(
            "Create an entity for this investigation."
        )
        description.setObjectName("formDescription")

        layout.addWidget(title)
        layout.addWidget(description)

        # -----------------------------
        # Basic entity information
        # -----------------------------

        basic_form = QFormLayout()

        # Category
        category_label = QLabel("Category:")

        self.category_combo = QComboBox()

        self.category_combo.addItems(
            ENTITY_REGISTRY.keys()
        )

        basic_form.addRow(
            category_label,
            self.category_combo
        )

        # Entity Type
        entity_type_label = QLabel("Entity Type:")

        self.entity_type_combo = QComboBox()

        basic_form.addRow(
            entity_type_label,
            self.entity_type_combo
        )

        # Label
        label_label = QLabel("Label:")

        self.label_input = QLineEdit()

        self.label_input.setPlaceholderText(
            "Example: PETER"
        )

        basic_form.addRow(
            label_label,
            self.label_input
        )

        layout.addLayout(basic_form)

        # -----------------------------
        # Properties
        # -----------------------------

        properties_title = QLabel("Properties")
        properties_title.setObjectName(
            "formSectionTitle"
        )

        layout.addWidget(properties_title)

        self.properties_layout = QFormLayout()

        layout.addLayout(
            self.properties_layout
        )

        layout.addStretch()

        # -----------------------------
        # Buttons
        # -----------------------------

        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.cancel_button.setObjectName(
            "secondaryButton"
        )

        self.create_button = QPushButton(
            "Save Changes" if self.entity else "Create Entity"
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

        # -----------------------------
        # Signals
        # -----------------------------

        self.category_combo.currentTextChanged.connect(
            self.category_changed
        )

        self.entity_type_combo.currentTextChanged.connect(
            self.entity_type_changed
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

        self.create_button.clicked.connect(
            self.create_entity
        )

        # -----------------------------
        # Initial population
        # -----------------------------

        if self.entity:
            self.load_entity()
        else:
            self.category_changed(
                self.category_combo.currentText()
            )

    # --------------------------------------------------
    # Category changed
    # --------------------------------------------------

    def category_changed(self, category):

        self.entity_type_combo.blockSignals(
            True
        )

        self.entity_type_combo.clear()

        if category not in ENTITY_REGISTRY:
            self.entity_type_combo.blockSignals(
                False
            )
            return

        entity_types = list(
            ENTITY_REGISTRY[category].keys()
        )

        self.entity_type_combo.addItems(
            entity_types
        )

        self.entity_type_combo.blockSignals(
            False
        )

        if entity_types:
            self.entity_type_changed(
                entity_types[0]
            )

    # --------------------------------------------------
    # Entity type changed
    # --------------------------------------------------

    def entity_type_changed(self, entity_type):

        self.clear_property_fields()

        category = self.category_combo.currentText()

        if not category:
            return

        if not entity_type:
            return

        if category not in ENTITY_REGISTRY:
            return

        if entity_type not in ENTITY_REGISTRY[category]:
            return

        entity_class = ENTITY_REGISTRY[
            category
        ][entity_type]

        signature = inspect.signature(
            entity_class.__init__
        )

        for parameter_name, parameter in signature.parameters.items():

            if parameter_name == "self":
                continue

            if parameter_name == "label":
                continue

            input_field = QLineEdit()

            input_field.setPlaceholderText(
                parameter_name.replace(
                    "_",
                    " "
                ).title()
            )

            self.property_inputs[
                parameter_name
            ] = input_field

            self.properties_layout.addRow(
                parameter_name.replace(
                    "_",
                    " "
                ).title() + ":",
                input_field
            )

    # --------------------------------------------------
    # Clear properties
    # --------------------------------------------------

    def clear_property_fields(self):

        self.property_inputs.clear()

        while self.properties_layout.count():

            item = (
                self.properties_layout.takeAt(0)
            )

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

    # --------------------------------------------------
    # Create Entity
    # --------------------------------------------------

    def create_entity(self):

        category = (
            self.category_combo.currentText()
        )

        entity_type = (
            self.entity_type_combo.currentText()
        )

        label = (
            self.label_input.text().strip()
        )

        # Validate label
        if not label:

            QMessageBox.warning(
                self,
                "Missing Label",
                "Please enter an entity label."
            )

            return

        properties = {}

        for (
            property_name,
            input_field
        ) in self.property_inputs.items():

            value = (
                input_field.text().strip()
            )

            if not value:

                QMessageBox.warning(
                    self,
                    "Missing Property",
                    f"Please enter "
                    f"{property_name.replace('_', ' ')}."
                )

                return

            properties[property_name] = value

        try:

            if self.entity is None:

                # Create new entity
                entity = EntityFactory.create(
                    category,
                    entity_type,
                    label,
                    properties
                )

                self.database.create_entity(
                    entity,
                    self.case_id,
                    category
                )

            else:

                # Update existing entity
                entity = EntityFactory.create(
                    category,
                    entity_type,
                    label,
                    properties
                )
    
                # Preserve the existing identity
                entity.entity_id = self.entity["entity_id"]
    
                self.database.update_entity(
                    entity,
                    category
                )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Error",
                f"Could not save entity:\n\n{error}"
            )

            return

        self.accept()

    def load_entity(self):

        category = self.entity["category"]
        entity_type = self.entity["entity_type"]

        category_index = (
            self.category_combo.findText(category)
        )
    
        if category_index >= 0:
            self.category_combo.setCurrentIndex(
                category_index
            )
    
        self.category_changed(category)
    
        entity_type_index = (
            self.entity_type_combo.findText(
                entity_type
            )
        )
    
        if entity_type_index >= 0:
            self.entity_type_combo.setCurrentIndex(
                entity_type_index
            )
    
        self.entity_type_changed(entity_type)
    
        self.label_input.setText(
            self.entity["label"]
        )
    
        properties = self.entity["properties"]
    
        for property_name, value in properties.items():
        
            input_field = self.property_inputs.get(
                property_name
            )
    
            if input_field:
                input_field.setText(
                    str(value)
                )
