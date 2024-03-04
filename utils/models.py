from typing import List

from gino import Gino
from gino.schema import GinoSchemaVisitor
import sqlalchemy as sa
from config import POSTGRES_URI

db = Gino()

class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = ' '.join(f'{name}={value!r}' for name, value in values.items())
        return f'<{model} {values_str}>'

class Event(BaseModel):
    __tablename__ = 'event'

    id_event = db.Column(db.BigInteger, primary_key=True, nullable=False)
    event_name = db.Column(db.String)


class Test(BaseModel):
    __tablename__ = 'test'
    id_test = db.Column(db.BigInteger, primary_key=True, nullable=False)
    id_event = db.Column(db.BigInteger)
    token = db.Column(db.BigInteger)
    lifetime = db.Column(db.String)
    end_time = db.Column(db.DateTime(timezone=True))
    bound_time = db.Column(db.BigInteger)


class Questions(BaseModel):
    __tablename__ = 'questions'
    id_quest = db.Column(db.BigInteger, primary_key=True, nullable=False)
    id_test = db.Column(db.BigInteger)
    type = db.Column(db.BigInteger)
    variants = db.Column(db.String)
    text = db.Column(db.String)
    correct_answer = db.Column(db.String)


class User(BaseModel):
    __tablename__ = 'user'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    events = db.Column(db.ARRAY(db.BigInteger))
    status = db.Column(db.String)


class Results(BaseModel):
    __tablename__ = 'results'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    id_test = db.Column(db.BigInteger)
    id_user = db.Column(db.BigInteger)
    result = db.Column(db.String)


async def create_tables():
    await db.set_bind(POSTGRES_URI)
    await db.gino.create_all()