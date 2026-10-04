from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMessageBox
)

from ui.case_form import CaseForm
from ui.investigation_window import InvestigationWindow

class MainWindow(QMainWindow):
    def __init__(self, database):
        super().__init__()

        self.database = database

        self.setWindowTitle("Digital Investigation System")
        self.resize(1200, 750)

        self.setup_ui()
        self.load_cases()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # =====================================
        # LEFT SIDE - CASE LIST
        # =====================================

        left_layout = QVBoxLayout()

        cases_label = QLabel("MY CASES")
        cases_label.setObjectName("sectionTitle")

        self.case_list = QListWidget()
        self.case_list.setObjectName("caseList")

        self.new_case_button = QPushButton("+  Create New Case")
        self.new_case_button.setObjectName("primaryButton")

        left_layout.addWidget(cases_label)
        left_layout.addWidget(self.case_list)
        left_layout.addWidget(self.new_case_button)

        # =====================================
        # RIGHT SIDE - CASE DETAILS
        # =====================================

        right_layout = QVBoxLayout()

        self.case_title = QLabel("Select a case")
        self.case_title.setObjectName("caseTitle")

        self.case_type = QLabel("")
        self.case_type.setObjectName("caseType")

        self.case_description = QLabel(
            "Select an existing case from the list "
            "or create a new investigation."
        )
        self.case_description.setWordWrap(True)
        self.case_description.setObjectName("caseDescription")

        self.case_status = QLabel("")
        self.case_status.setObjectName("caseStatus")

        self.case_investigator = QLabel("")
        self.case_investigator.setObjectName("caseInfo")

        self.case_date_opened = QLabel("")
        self.case_date_opened.setObjectName("caseInfo")

        self.case_id = QLabel("")
        self.case_id.setObjectName("caseId")

        self.open_case_button = QPushButton("Open Case")
        self.open_case_button.setObjectName("primaryButton")
        self.open_case_button.setEnabled(False)

        self.edit_case_button = QPushButton("Edit Case")
        self.edit_case_button.setObjectName("secondaryButton")
        self.edit_case_button.setEnabled(False)

        self.delete_case_button = QPushButton("Delete Case")
        self.delete_case_button.setObjectName("dangerButton")
        self.delete_case_button.setEnabled(False)

        right_layout.addWidget(self.case_title)
        right_layout.addWidget(self.case_type)
        right_layout.addSpacing(15)
        right_layout.addWidget(self.case_description)
        right_layout.addSpacing(20)
        right_layout.addWidget(self.case_status)
        right_layout.addWidget(self.case_investigator)
        right_layout.addWidget(self.case_date_opened)
        right_layout.addWidget(self.case_id)

        right_layout.addStretch()

        right_layout.addWidget(self.open_case_button)

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.edit_case_button)
        button_layout.addWidget(self.delete_case_button)

        right_layout.addLayout(button_layout)

        # =====================================
        # MAIN LAYOUT
        # =====================================

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

        # =====================================
        # SIGNALS
        # =====================================

        self.new_case_button.clicked.connect(
            self.open_case_form
        )

        self.case_list.itemClicked.connect(
            self.display_case
        )

        self.edit_case_button.clicked.connect(
            self.edit_case
        )

        self.delete_case_button.clicked.connect(
            self.delete_case
        )

        self.open_case_button.clicked.connect(
            self.open_investigation
        )

    # =========================================
    # LOAD CASES
    # =========================================

    def load_cases(self):
        self.case_list.clear()

        cases = self.database.get_cases()

        for case in cases:
            item = QListWidgetItem(
                f"{case.case_name}  •  {case.status}"
            )

            item.setData(
                1,
                case.case_id
            )

            self.case_list.addItem(item)

    # =========================================
    # DISPLAY CASE
    # =========================================

    def display_case(self, item):
        case_id = item.data(1)

        case = self.database.get_case(case_id)
    
        if case is None:
            return
    
        self.show_case_details(case)

    # =========================================
    # CREATE CASE
    # =========================================

    def open_case_form(self):
        dialog = CaseForm(
            database=self.database,
            parent=self
        )

        if dialog.exec():
            self.load_cases()

    # =========================================
    # EDIT CASE
    # =========================================

    def edit_case(self):
        current_item = self.case_list.currentItem()

        if current_item is None:
            return

        case_id = current_item.data(1)
        case = self.database.get_case(case_id)

        if case is None:
            return

        dialog = CaseForm(
            database=self.database,
            case=case,
            parent=self
        )

        if dialog.exec():
            self.load_cases()

            updated_case = self.database.get_case(case_id)

            if updated_case:
                self.show_case_details(updated_case)

    def delete_case(self):
        current_item = self.case_list.currentItem()

        if current_item is None:
            return

        case_id = current_item.data(1)

        case = self.database.get_case(case_id)

        if case is None:
            return

        result = QMessageBox.question(
            self,
            "Delete Case",
            (
                f"Are you sure you want to delete "
                f"'{case.case_name}'?"
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        if result == QMessageBox.StandardButton.Yes:
            self.database.delete_case(case_id)

            self.clear_case_details()
            self.load_cases()

    def clear_case_details(self):
        self.case_title.setText("Select a case")
        self.case_type.setText("")

        self.case_description.setText(
            "Select an existing case "
            "or create a new investigation."
        )

        self.case_status.setText("")
        self.case_investigator.setText("")
        self.case_date_opened.setText("")
        self.case_id.setText("")

        self.open_case_button.setEnabled(False)
        self.edit_case_button.setEnabled(False)
        self.delete_case_button.setEnabled(False)

    def show_case_details(self, case):
        self.case_title.setText(
            case.case_name
        )

        self.case_type.setText(
            case.case_type
        )

        self.case_description.setText(
            case.description
            or "No description provided."
        )

        self.case_status.setText(
            f"Status: {case.status}"
        )

        self.case_investigator.setText(
            f"Investigator: "
            f"{case.investigator or 'Not specified'}"
        )

        self.case_date_opened.setText(
            f"Date Opened: "
            f"{case.date_opened}"
        )

        self.case_id.setText(
            f"Case ID: {case.case_id}"
        )

        self.open_case_button.setEnabled(True)
        self.edit_case_button.setEnabled(True)
        self.delete_case_button.setEnabled(True)    

    def open_investigation(self):
        current_item = self.case_list.currentItem()

        if current_item is None:
            return

        case_id = current_item.data(1)

        case = self.database.get_case(case_id)

        if case is None:
            return

        self.investigation_window = InvestigationWindow(
            database=self.database,
            case=case,
            parent=self
        )

        self.investigation_window.show()
        self.hide()
