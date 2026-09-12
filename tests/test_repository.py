import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.repository as repository_module
from app.database import Base
from app.repository import ExperimentRepository


@pytest.fixture
def test_repository(monkeypatch):
    engine = create_engine(
        "sqlite:///:memory:"
    )

    Base.metadata.create_all(
        bind=engine
    )

    TestSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False
    )

    monkeypatch.setattr(
        repository_module,
        "SessionLocal",
        TestSessionLocal
    )

    return ExperimentRepository()


def test_create_experiment(
    test_repository
):
    experiment = (
        test_repository.create_experiment(
            experiment_name="Image Classification Test",
            researcher="Shefali Mandal",
            category="Computer Vision",
            measurement_value=94.5,
            unit="%",
            status="Completed",
            notes="Test experiment"
        )
    )

    assert experiment.id is not None

    assert (
        experiment.experiment_name
        == "Image Classification Test"
    )

    assert (
        experiment.status
        == "Completed"
    )


def test_get_experiment(
    test_repository
):
    created = (
        test_repository.create_experiment(
            experiment_name="Database Test",
            researcher="Shefali Mandal",
            category="Database Systems",
            measurement_value=40.0,
            unit="ms",
            status="In Progress",
            notes=""
        )
    )

    found = (
        test_repository.get_experiment(
            created.id
        )
    )

    assert found is not None

    assert (
        found.experiment_name
        == "Database Test"
    )


def test_update_experiment(
    test_repository
):
    created = (
        test_repository.create_experiment(
            experiment_name="API Test",
            researcher="Shefali Mandal",
            category="Software Engineering",
            measurement_value=500,
            unit="requests",
            status="Planned",
            notes=""
        )
    )

    updated = (
        test_repository.update_experiment(
            experiment_id=created.id,
            experiment_name="API Load Test",
            researcher="Shefali Mandal",
            category="Software Engineering",
            measurement_value=850,
            unit="requests",
            status="Completed",
            notes="Updated test"
        )
    )

    assert (
        updated.experiment_name
        == "API Load Test"
    )

    assert (
        updated.measurement_value
        == 850
    )

    assert (
        updated.status
        == "Completed"
    )


def test_delete_experiment(
    test_repository
):
    created = (
        test_repository.create_experiment(
            experiment_name="Temporary Test",
            researcher="Shefali Mandal",
            category="Testing",
            measurement_value=1,
            unit="run",
            status="Planned",
            notes=""
        )
    )

    experiment_id = created.id

    test_repository.delete_experiment(
        experiment_id
    )

    deleted = (
        test_repository.get_experiment(
            experiment_id
        )
    )

    assert deleted is None


def test_filter_by_status(
    test_repository
):
    test_repository.create_experiment(
        experiment_name="Completed Test",
        researcher="Shefali Mandal",
        category="Computer Vision",
        measurement_value=95,
        unit="%",
        status="Completed",
        notes=""
    )

    test_repository.create_experiment(
        experiment_name="Planned Test",
        researcher="Shefali Mandal",
        category="Software Engineering",
        measurement_value=100,
        unit="records",
        status="Planned",
        notes=""
    )

    results = (
        test_repository.get_all_experiments(
            search_text="",
            status_filter="Completed"
        )
    )

    assert len(results) == 1

    assert (
        results[0].status
        == "Completed"
    )


def test_search_by_category(
    test_repository
):
    test_repository.create_experiment(
        experiment_name="Vision Test",
        researcher="Shefali Mandal",
        category="Computer Vision",
        measurement_value=92,
        unit="%",
        status="Completed",
        notes=""
    )

    test_repository.create_experiment(
        experiment_name="Database Test",
        researcher="Shefali Mandal",
        category="Database Systems",
        measurement_value=40,
        unit="ms",
        status="In Progress",
        notes=""
    )

    results = (
        test_repository.get_all_experiments(
            search_text="Computer Vision",
            status_filter="All"
        )
    )

    assert len(results) == 1

    assert (
        results[0].category
        == "Computer Vision"
    )