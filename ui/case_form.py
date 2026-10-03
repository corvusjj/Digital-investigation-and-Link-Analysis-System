from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)

from models.case import Case


class CaseForm(QDialog):
    def __init__(self, database, case=None, parent=None):
        super().__init__(parent)

        self.database = database
        self.case = case

        if self.case:
            self.setWindowTitle("Edit Case")
        else:
            self.setWindowTitle("Create New Case")

        self.setMinimumWidth(500)

        self.setup_ui()

        if self.case:
            self.load_case()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Case name
        self.case_name_input = QLineEdit()
        self.case_name_input.setPlaceholderText(
            "Enter case name"
        )

        # Case type
        self.case_type_input = QComboBox()

        self.case_type_input.addItems([
            "Missing Person",
            "Cybercrime",
            "Fraud",
            "Theft",
            "Homicide",
            "Drug Investigation",
            "Financial Investigation",
            "Digital Investigation",
            "Other"
        ])

        # Description
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Enter a description of the investigation..."
        )
        self.description_input.setMinimumHeight(120)

        # Investigator
        self.investigator_input = QLineEdit()
        self.investigator_input.setPlaceholderText(
            "Enter investigator name"
        )

        form_layout.addRow(
            "Case Name:",
            self.case_name_input
        )

        form_layout.addRow(
            "Case Type:",
            self.case_type_input
        )

        form_layout.addRow(
            "Description:",
            self.description_input
        )

        form_layout.addRow(
            "Investigator:",
            self.investigator_input
        )

        # Buttons
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("secondaryButton")

        if self.case:
            self.create_button = QPushButton("Save Changes")
        else:
            self.create_button = QPushButton("Create Case")

        self.create_button.setObjectName("primaryButton")
        self.create_button.setObjectName("primaryButton")

        button_layout = QHBoxLayout()

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.create_button)

        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # Signals
        self.cancel_button.clicked.connect(self.reject)
        self.create_button.clicked.connect(self.save_case)

    def save_case(self):
        case_name = self.case_name_input.text().strip()
        case_type = self.case_type_input.currentText()
        description = self.description_input.toPlainText().strip()
        investigator = self.investigator_input.text().strip()

        if not case_name:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter a case name."
            )
            return

        if self.case:
            # UPDATE EXISTING CASE

            self.case.case_name = case_name
            self.case.case_type = case_type
            self.case.description = description
            self.case.investigator = investigator

            self.database.update_case(self.case)

        else:
            # CREATE NEW CASE

            case = Case(
                case_name=case_name,
                case_type=case_type,
                description=description,
                investigator=investigator
            )

            self.database.create_case(case)

        self.accept()

    def load_case(self):
        self.case_name_input.setText(
            self.case.case_name
        )

        index = self.case_type_input.findText(
            self.case.case_type
        )

        if index >= 0:
            self.case_type_input.setCurrentIndex(index)

        self.description_input.setPlainText(
            self.case.description
        )

        self.investigator_input.setText(
            self.case.investigator
        )
    