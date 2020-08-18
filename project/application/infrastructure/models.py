import enum
from application.infrastructure.common_model import Model, Column, db
from application.infrastructure.common_model import (
    TimeStampedMixin,
    DeleteMixin,
    SurrogatePKMixin,
)
from sqlalchemy.sql.schema import Index, UniqueConstraint


class Table(Model, SurrogatePKMixin, TimeStampedMixin, DeleteMixin):
    __tablename__ = "table"

    code = Column(db.String(250), unique=True)
    name = Column(db.String(10), nullable=False)
