from PyQt6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget
)

from app.repository import ExperimentRepository


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.repository = ExperimentRepository()
        self.selected_experiment_id = None

        self.setWindowTitle("Research Experiment Manager")
        self.resize(1100, 700)

        self.build_ui()
        self.load_experiments()


    def build_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)

        # -------------------------
        # Title
        # -------------------------

        title = QLabel("Research Experiment Manager")

        title.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        main_layout.addWidget(title)

        # -------------------------
        # Form
        # -------------------------

        form_layout = QFormLayout()

        self.experiment_name_input = QLineEdit()
        self.experiment_name_input.setPlaceholderText(
            "Example: Image Classification Test"
        )

        self.researcher_input = QLineEdit()
        self.researcher_input.setPlaceholderText(
            "Example: Shefali Mandal"
        )

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText(
            "Example: Computer Vision"
        )

        self.measurement_input = QLineEdit()
        self.measurement_input.setPlaceholderText(
            "Example: 94.5"
        )

        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText(
            "Example: %, ms, MB"
        )

        self.status_input = QComboBox()
        self.status_input.addItems(
            [
                "Planned",
                "In Progress",
                "Completed"
            ]
        )

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText(
            "Enter experiment notes"
        )
        self.notes_input.setMaximumHeight(90)

        form_layout.addRow(
            "Experiment:",
            self.experiment_name_input
        )

        form_layout.addRow(
            "Researcher:",
            self.researcher_input
        )

        form_layout.addRow(
            "Category:",
            self.category_input
        )

        form_layout.addRow(
            "Measurement:",
            self.measurement_input
        )

        form_layout.addRow(
            "Unit:",
            self.unit_input
        )

        form_layout.addRow(
            "Status:",
            self.status_input
        )

        form_layout.addRow(
            "Notes:",
            self.notes_input
        )

        main_layout.addLayout(form_layout)

        # -------------------------
        # Buttons
        # -------------------------

        button_layout = QHBoxLayout()

        self.save_button = QPushButton(
            "Save Experiment"
        )

        self.update_button = QPushButton(
            "Update Experiment"
        )

        self.delete_button = QPushButton(
            "Delete Experiment"
        )

        self.clear_button = QPushButton(
            "Clear Form"
        )

        self.save_button.clicked.connect(
            self.save_experiment
        )

        self.update_button.clicked.connect(
            self.update_experiment
        )

        self.delete_button.clicked.connect(
            self.delete_experiment
        )

        self.clear_button.clicked.connect(
            self.clear_form
        )

        button_layout.addWidget(
            self.save_button
        )

        button_layout.addWidget(
            self.update_button
        )

        button_layout.addWidget(
            self.delete_button
        )

        button_layout.addWidget(
            self.clear_button
        )

        main_layout.addLayout(button_layout)

        # -------------------------
        # Search + filter
        # -------------------------

        filter_layout = QHBoxLayout()

        search_label = QLabel("Search:")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search experiment, researcher, category, or notes"
        )

        status_label = QLabel("Status:")

        self.status_filter = QComboBox()

        self.status_filter.addItems(
            [
                "All",
                "Planned",
                "In Progress",
                "Completed"
            ]
        )

        filter_layout.addWidget(
            search_label
        )

        filter_layout.addWidget(
            self.search_input,
            1
        )

        filter_layout.addWidget(
            status_label
        )

        filter_layout.addWidget(
            self.status_filter
        )

        main_layout.addLayout(
            filter_layout
        )

        # Search changes
        self.search_input.textChanged.connect(
            self.on_search_changed
        )

        # Status changes
        self.status_filter.currentIndexChanged.connect(
            self.on_status_changed
        )

        # -------------------------
        # Table
        # -------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(7)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Experiment",
                "Researcher",
                "Category",
                "Measurement",
                "Unit",
                "Status"
            ]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.cellClicked.connect(
            self.load_selected_row
        )

        main_layout.addWidget(
            self.table
        )


    # -------------------------
    # Search changed
    # -------------------------

    def on_search_changed(self, text):

        self.load_experiments()


    # -------------------------
    # Status changed
    # -------------------------

    def on_status_changed(self, index):

        selected_status = (
            self.status_filter.currentText()
        )

        print(
            "STATUS FILTER:",
            selected_status
        )

        self.load_experiments()


    # -------------------------
    # Get form data
    # -------------------------

    def get_form_data(self):

        experiment_name = (
            self.experiment_name_input
            .text()
            .strip()
        )

        researcher = (
            self.researcher_input
            .text()
            .strip()
        )

        category = (
            self.category_input
            .text()
            .strip()
        )

        unit = (
            self.unit_input
            .text()
            .strip()
        )

        if not experiment_name:
            raise ValueError(
                "Experiment name is required."
            )

        if not researcher:
            raise ValueError(
                "Researcher is required."
            )

        if not category:
            raise ValueError(
                "Category is required."
            )

        if not unit:
            raise ValueError(
                "Unit is required."
            )

        try:

            measurement_value = float(
                self.measurement_input.text()
            )

        except ValueError:

            raise ValueError(
                "Measurement must be a number."
            )

        return {
            "experiment_name":
                experiment_name,

            "researcher":
                researcher,

            "category":
                category,

            "measurement_value":
                measurement_value,

            "unit":
                unit,

            "status":
                self.status_input.currentText(),

            "notes":
                self.notes_input
                .toPlainText()
                .strip()
        }


    # -------------------------
    # Save
    # -------------------------

    def save_experiment(self):

        try:

            data = self.get_form_data()

            self.repository.create_experiment(
                **data
            )

            self.clear_form()
            self.load_experiments()

            QMessageBox.information(
                self,
                "Saved",
                "Experiment saved successfully."
            )

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )


    # -------------------------
    # Load / filter
    # -------------------------

    def load_experiments(self):

        search_text = (
            self.search_input
            .text()
            .strip()
        )

        status_filter = (
            self.status_filter
            .currentText()
            .strip()
        )

        print(
            "SEARCH:",
            repr(search_text)
        )

        print(
            "STATUS:",
            repr(status_filter)
        )

        experiments = (
            self.repository
            .get_all_experiments(
                search_text=search_text,
                status_filter=status_filter
            )
        )

        print(
            "RESULTS:",
            [
                (
                    x.id,
                    x.experiment_name,
                    x.status
                )
                for x in experiments
            ]
        )

        self.table.clearContents()

        self.table.setRowCount(
            len(experiments)
        )

        for row, experiment in enumerate(
            experiments
        ):

            values = [
                experiment.id,
                experiment.experiment_name,
                experiment.researcher,
                experiment.category,
                experiment.measurement_value,
                experiment.unit,
                experiment.status
            ]

            for column, value in enumerate(
                values
            ):

                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(
                        str(value)
                    )
                )


    # -------------------------
    # Select row
    # -------------------------

    def load_selected_row(
        self,
        row,
        column
    ):

        id_item = self.table.item(
            row,
            0
        )

        if id_item is None:
            return

        experiment_id = int(
            id_item.text()
        )

        experiment = (
            self.repository
            .get_experiment(
                experiment_id
            )
        )

        if experiment is None:
            return

        self.selected_experiment_id = (
            experiment.id
        )

        self.experiment_name_input.setText(
            experiment.experiment_name
        )

        self.researcher_input.setText(
            experiment.researcher
        )

        self.category_input.setText(
            experiment.category
        )

        self.measurement_input.setText(
            str(
                experiment.measurement_value
            )
        )

        self.unit_input.setText(
            experiment.unit
        )

        self.status_input.setCurrentText(
            experiment.status
        )

        self.notes_input.setPlainText(
            experiment.notes
        )


    # -------------------------
    # Update
    # -------------------------

    def update_experiment(self):

        if self.selected_experiment_id is None:

            QMessageBox.information(
                self,
                "Select Experiment",
                "Select a row before updating."
            )

            return

        try:

            data = self.get_form_data()

            self.repository.update_experiment(
                experiment_id=(
                    self.selected_experiment_id
                ),
                **data
            )

            self.clear_form()
            self.load_experiments()

            QMessageBox.information(
                self,
                "Updated",
                "Experiment updated successfully."
            )

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Invalid Input",
                str(error)
            )


    # -------------------------
    # Delete
    # -------------------------

    def delete_experiment(self):

        if self.selected_experiment_id is None:

            QMessageBox.information(
                self,
                "Select Experiment",
                "Select a row before deleting."
            )

            return

        answer = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this experiment?"
        )

        if (
            answer
            != QMessageBox.StandardButton.Yes
        ):
            return

        try:

            self.repository.delete_experiment(
                self.selected_experiment_id
            )

            self.clear_form()
            self.load_experiments()

            QMessageBox.information(
                self,
                "Deleted",
                "Experiment deleted successfully."
            )

        except ValueError as error:

            QMessageBox.warning(
                self,
                "Delete Error",
                str(error)
            )


    # -------------------------
    # Clear form
    # -------------------------

    def clear_form(self):

        self.selected_experiment_id = None

        self.experiment_name_input.clear()
        self.researcher_input.clear()
        self.category_input.clear()
        self.measurement_input.clear()
        self.unit_input.clear()

        self.status_input.setCurrentText(
            "Planned"
        )

        self.notes_input.clear()

        self.table.clearSelection()