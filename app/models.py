from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class Experiment(Base):

    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    experiment_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    researcher: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    measurement_value: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    unit: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    notes: Mapped[str] = mapped_column(
        Text,
        default=""
    )


    def validate(self):

        if not self.experiment_name.strip():
            raise ValueError(
                "Experiment name is required."
            )

        if not self.researcher.strip():
            raise ValueError(
                "Researcher name is required."
            )

        if not self.category.strip():
            raise ValueError(
                "Category is required."
            )

        if not self.unit.strip():
            raise ValueError(
                "Unit is required."
            )

        if self.status not in {
            "Planned",
            "In Progress",
            "Completed"
        }:
            raise ValueError(
                "Status must be Planned, In Progress, or Completed."
            )