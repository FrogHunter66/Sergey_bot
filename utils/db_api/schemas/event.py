from utils.models import BaseModel
from sqlalchemy import Column, BigInteger, String, sql


class Event(BaseModel):
    __tablename__ = 'event'
    id_event = Column(BigInteger, primary_key=True, nullable=False)
    event_name = Column(String)
    query: sql.select
