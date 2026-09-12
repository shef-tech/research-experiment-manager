# Research Experiment Manager

Research Experiment Manager is a desktop application for storing and managing research experiment records. The application provides a graphical interface for creating, viewing, updating, deleting, searching, and filtering experiment data.

The project demonstrates desktop application development, relational database integration, automated testing, and continuous integration using Python.

## Features

- Create, view, update, and delete experiment records
- Search experiments by experiment name, researcher, category, or notes
- Filter experiments by status: Planned, In Progress, or Completed
- Validate required fields and numerical measurements
- Store experiment data in PostgreSQL using SQLAlchemy ORM
- Use SQLite as a fallback database for testing and CI environments
- Log application and database operations
- Handle database errors
- Run automated tests with pytest
- Automatically run tests on pushes and pull requests using GitHub Actions

## Technologies

- Python
- PyQt6
- PostgreSQL
- SQLite
- SQLAlchemy ORM
- psycopg
- pytest
- Git
- GitHub Actions

## Project Structure

```text
research_experiment_manager/
├── .github/
│   └── workflows/
│       └── tests.yml
├── app/
│   ├── database.py
│   ├── gui.py
│   ├── logger.py
│   ├── models.py
│   └── repository.py
├── tests/
│   ├── test_models.py
│   └── test_repository.py
├── main.py
├── requirements.txt
└── README.md
```

## Database Configuration

The application uses PostgreSQL when database credentials are available through environment variables.

Create a `.env` file in the project root:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=research_experiments
DB_USER=postgres
DB_PASSWORD=your_password
```

The `.env` file is excluded from Git version control so database credentials are not committed to the repository.

## Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/shef-tech/research-experiment-manager.git
cd research-experiment-manager
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment and install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

## Running Tests

Run the automated test suite with:

```bash
python -m pytest -v
```

The test suite covers model validation and repository operations including creating, retrieving, updating, deleting, searching, and filtering experiment records.

## Continuous Integration

GitHub Actions automatically runs the test suite whenever code is pushed to the repository or a pull request is created.

This helps verify that changes do not break existing functionality.
