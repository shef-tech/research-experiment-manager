from sqlalchemy import or_, select

from app.database import SessionLocal
from app.models import Experiment


class ExperimentRepository:

    def create_experiment(
        self,
        experiment_name,
        researcher,
        category,
        measurement_value,
        unit,
        status,
        notes
    ):

        experiment = Experiment(
            experiment_name=experiment_name.strip(),
            researcher=researcher.strip(),
            category=category.strip(),
            measurement_value=measurement_value,
            unit=unit.strip(),
            status=status.strip(),
            notes=notes.strip()
        )

        experiment.validate()

        with SessionLocal() as session:

            session.add(experiment)

            session.commit()

            session.refresh(experiment)

        return experiment


    def get_all_experiments(
        self,
        search_text="",
        status_filter="All"
    ):

        search_text = search_text.strip()
        status_filter = status_filter.strip()

        with SessionLocal() as session:

            statement = select(
                Experiment
            )

            # Search
            if search_text:

                pattern = f"%{search_text}%"

                statement = statement.where(
                    or_(
                        Experiment.experiment_name.ilike(pattern),
                        Experiment.researcher.ilike(pattern),
                        Experiment.category.ilike(pattern),
                        Experiment.notes.ilike(pattern)
                    )
                )

            # Status filter
            if status_filter != "All":

                statement = statement.where(
                    Experiment.status == status_filter
                )

            statement = statement.order_by(
                Experiment.id.asc()
            )

            experiments = session.scalars(
                statement
            ).all()

            return list(experiments)


    def get_experiment(
        self,
        experiment_id
    ):

        with SessionLocal() as session:

            experiment = session.get(
                Experiment,
                experiment_id
            )

            return experiment


    def update_experiment(
        self,
        experiment_id,
        experiment_name,
        researcher,
        category,
        measurement_value,
        unit,
        status,
        notes
    ):

        with SessionLocal() as session:

            experiment = session.get(
                Experiment,
                experiment_id
            )

            if experiment is None:

                raise ValueError(
                    "Experiment not found."
                )

            experiment.experiment_name = (
                experiment_name.strip()
            )

            experiment.researcher = (
                researcher.strip()
            )

            experiment.category = (
                category.strip()
            )

            experiment.measurement_value = (
                measurement_value
            )

            experiment.unit = (
                unit.strip()
            )

            experiment.status = (
                status.strip()
            )

            experiment.notes = (
                notes.strip()
            )

            experiment.validate()

            session.commit()

            session.refresh(
                experiment
            )

            return experiment


    def delete_experiment(
        self,
        experiment_id
    ):

        with SessionLocal() as session:

            experiment = session.get(
                Experiment,
                experiment_id
            )

            if experiment is None:

                raise ValueError(
                    "Experiment not found."
                )

            session.delete(
                experiment
            )

            session.commit()