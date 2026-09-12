# Research Experiment Manager

Research Experiment Manager is a desktop application built with Python and PyQt6 for managing research experiment records. It supports creating, viewing, updating, deleting, searching, and filtering experiment data through a native graphical interface.

## Features

- Create, update, and delete experiment records
- Search experiments by name, researcher, category, or notes
- Filter experiments by status
- Input validation for required fields and measurement values
- PostgreSQL database support through SQLAlchemy ORM
- SQLite fallback for local testing and CI environments
- Application logging
- Database error handling
- Automated testing with pytest
- Continuous integration with GitHub Actions

## Technology Stack

- Python
- PyQt6
- SQLAlchemy
- PostgreSQL
- SQLite
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
