from application.extensions import db
from sqlalchemy import Column

relationship = db.relationship
backref = db.backref
joinedload = db.joinedload
selectinload = db.selectinload

text_type = str
binary_type = bytes
string_types = (str,)
unicode = str
basestring = (str, bytes)


class SurrogatePKMixin(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {"extend_existing": True}

    id = Column(db.Integer, primary_key=True, autoincrement=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            return cls.query.get(int(record_id))
        return None


class TimeStampedMixin(object):
    __table_args__ = {"extend_existing": True}

    created_at = Column(db.DateTime(timezone=True), server_default=db.func.now())
    modified_at = Column(
        db.DateTime, server_default=db.func.now(), onupdate=db.func.now()
    )


class DeleteMixin(object):
    __table_args__ = {"extend_existing": True}

    deleted = db.Column("deleted", db.Boolean, default=False)

    @classmethod
    def delete_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            )
        ):
            obj = cls.query.get(int(record_id))
            obj.deleted = True
            obj.save()
        return None


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

    def mark_deleted(self, commit=True):
        self.deleted = True
        return commit and self.save() or self


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


def reference_col(
    tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None
):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name), **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs
    )
