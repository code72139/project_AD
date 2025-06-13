from app import db

class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        """Convierte el objeto a un diccionario."""
        data = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, db.DateTime):
                value = value.isoformat()
            data[column.name] = value
        return data
