import sys

from database.database import Database

from PyQt6.QtWidgets import (
    QApplication, 
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QPushButton,
    QLabel
)

from factories.entity_factory import EntityFactory
from factories.relation_factory import RelationFactory
from graph.investigation_graph import InvestigationGraph

person1 = EntityFactory.create(
    "PEOPLE",
    "PERSON",
    "JOHN",
    {"full_name": "John Corbet",
      "alias": "programmer",
      "age": 3,
      "occupation": "student"}
)

person2 = EntityFactory.create(
    "PEOPLE",
    "PERSON",
    "PETER",
    {"full_name": "Peter Parker",
      "alias": "spidey",
      "age": 24,
      "occupation": "actor"}
)

person3 = EntityFactory.create(
    "PEOPLE",
    "PERSON",
    "BRUCE",
    {"full_name": "Bruce Dela Cruz",
      "alias": "dark night",
      "age": 42,
      "occupation": "police officer"}
)

relation1 = RelationFactory.create(
    "IS ASSOCIATED",
    person1.entity_id,
    person2.entity_id
)

investigation_graph = InvestigationGraph()

investigation_graph.add_entity(person1)
investigation_graph.add_entity(person2)
investigation_graph.add_relation(relation1)

print(investigation_graph.graph.nodes)

database = Database()
database.initialize()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Digital Investigation and Link Analysis System")
        self.resize(1200, 800)

        #Main container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #Main layout
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        #Entity list
        self.entity_list = QListWidget()

        #Buttons
        self.add_button = QPushButton("Add")
        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")

        #Right side
        self.entity_title = QLabel("Select an entity")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.entity_title)
        right_layout.addLayout(button_layout)

        #Main layout
        main_layout.addWidget(self.entity_list)
        main_layout.addLayout(right_layout)

app = QApplication(sys.argv)

with open("ui/styles.qss", "r") as file:
    app.setStyleSheet(file.read())

window = MainWindow()
window.show()

sys.exit(app.exec())

# ui module
# common relations properties
# dictionaries/ list for storing nodes
# mvc modules

# relation confidence
# properties={
#         "date": "2026-09-15",
#         "source": "Vehicle Registry",
#         "confidence": "HIGH",
#         "notes": "Registered owner"
#     }
