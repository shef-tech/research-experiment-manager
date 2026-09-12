import pytest

from app.models import Experiment


def test_valid_experiment():
    experiment = Experiment(
        experiment_name="Image Classification Test",
        researcher="Shefali Mandal",
        category="Computer Vision",
        measurement_value=94.5,
        unit="%",
        status="Completed",
        notes="Evaluated model accuracy."
    )

    experiment.validate()


def test_experiment_name_required():
    experiment = Experiment(
        experiment_name="",
        researcher="Shefali Mandal",
        category="Computer Vision",
        measurement_value=94.5,
        unit="%",
        status="Completed",
        notes=""
    )

    with pytest.raises(ValueError):
        experiment.validate()


def test_researcher_required():
    experiment = Experiment(
        experiment_name="Image Classification Test",
        researcher="",
        category="Computer Vision",
        measurement_value=94.5,
        unit="%",
        status="Completed",
        notes=""
    )

    with pytest.raises(ValueError):
        experiment.validate()


def test_category_required():
    experiment = Experiment(
        experiment_name="Image Classification Test",
        researcher="Shefali Mandal",
        category="",
        measurement_value=94.5,
        unit="%",
        status="Completed",
        notes=""
    )

    with pytest.raises(ValueError):
        experiment.validate()


def test_unit_required():
    experiment = Experiment(
        experiment_name="Image Classification Test",
        researcher="Shefali Mandal",
        category="Computer Vision",
        measurement_value=94.5,
        unit="",
        status="Completed",
        notes=""
    )

    with pytest.raises(ValueError):
        experiment.validate()


def test_invalid_status():
    experiment = Experiment(
        experiment_name="Image Classification Test",
        researcher="Shefali Mandal",
        category="Computer Vision",
        measurement_value=94.5,
        unit="%",
        status="Finished",
        notes=""
    )

    with pytest.raises(ValueError):
        experiment.validate()