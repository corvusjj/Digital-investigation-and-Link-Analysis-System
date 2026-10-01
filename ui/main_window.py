from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton
)

from ui.case_form import CaseForm

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

        # -------------------------
        # LEFT SIDE
        # -------------------------

        left_layout = QVBoxLayout()

        cases_label = QLabel("MY CASES")
        cases_label.setObjectName("sectionTitle")

        self.case_list = QListWidget()
        self.case_list.setObjectName("caseList")

        self.new_case_button = QPushButton("+  Create New Case")
        self.new_case_button.setObjectName("primaryButton")
        self.new_case_button.clicked.connect(
            self.open_case_form
        )

        left_layout.addWidget(cases_label)
        left_layout.addWidget(self.case_list)
        left_layout.addWidget(self.new_case_button)

        # -------------------------
        # RIGHT SIDE
        # -------------------------

        right_layout = QVBoxLayout()

        self.case_title = QLabel("Select a case")
        self.case_title.setObjectName("caseTitle")

        self.case_description = QLabel(
            "Select an existing case from the list "
            "or create a new investigation."
        )

        self.case_description.setWordWrap(True)
        self.case_description.setObjectName("caseDescription")

        right_layout.addWidget(self.case_title)
        right_layout.addWidget(self.case_description)
        right_layout.addStretch()

        # -------------------------
        # MAIN LAYOUT
        # -------------------------

        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 2)

    def open_case_form(self):
        dialog = CaseForm(
            database=self.database,
            parent=self
    )

        if dialog.exec():
            self.load_cases()

    def load_cases(self):
        self.case_list.clear()

        cases = self.database.get_cases()

        for case in cases:
            self.case_list.addItem(
                f"{case.case_name}  •  {case.status}"
            )