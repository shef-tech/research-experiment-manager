from sqlalchemy import or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal
from app.logger import get_logger
from app.models import Experiment


logger = get_logger(__name__)


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

        try:
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

            logger.info(
                "Created experiment id=%s name=%s",
                experiment.id,
                experiment.experiment_name
            )

            return experiment

        except SQLAlchemyError:
            logger.exception(
                "Database error while creating experiment"
            )

            raise RuntimeError(
                "Could not save the experiment."
            )


    def get_all_experiments(
        self,
        search_text="",
        status_filter="All"
    ):

        try:
            search_text = search_text.strip()
            status_filter = status_filter.strip()

            with SessionLocal() as session:

                statement = select(
                    Experiment
                )

                if search_text:

                    pattern = f"%{search_text}%"

                    statement = statement.where(
                        or_(
                            Experiment.experiment_name.ilike(
                                pattern
                            ),
                            Experiment.researcher.ilike(
                                pattern
                            ),
                            Experiment.category.ilike(
                                pattern
                            ),
                            Experiment.notes.ilike(
                                pattern
                            )
                        )
                    )

                if status_filter != "All":

                    statement = statement.where(
                        Experiment.status
                        == status_filter
                    )

                statement = statement.order_by(
                    Experiment.id.asc()
                )

                experiments = session.scalars(
                    statement
                ).all()

                return list(experiments)

        except SQLAlchemyError:
            logger.exception(
                "Database error while loading experiments"
            )

            raise RuntimeError(
                "Could not load experiments."
            )


    def get_experiment(
        self,
        experiment_id
    ):

        try:
            with SessionLocal() as session:

                return session.get(
                    Experiment,
                    experiment_id
                )

        except SQLAlchemyError:
            logger.exception(
                "Database error while loading experiment id=%s",
                experiment_id
            )

            raise RuntimeError(
                "Could not load the experiment."
            )


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

        try:
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

                logger.info(
                    "Updated experiment id=%s",
                    experiment.id
                )

                return experiment

        except SQLAlchemyError:
            logger.exception(
                "Database error while updating experiment id=%s",
                experiment_id
            )

            raise RuntimeError(
                "Could not update the experiment."
            )


    def delete_experiment(
        self,
        experiment_id
    ):

        try:
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

                logger.info(
                    "Deleted experiment id=%s",
                    experiment_id
                )

        except SQLAlchemyError:
            logger.exception(
                "Database error while deleting experiment id=%s",
                experiment_id
            )

            raise RuntimeError(
                "Could not delete the experiment."
            )