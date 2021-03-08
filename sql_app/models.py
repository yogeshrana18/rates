# Third Party
from sqlalchemy import String, Column, ForeignKey, DateTime, Integer
# Local
from .database import Base


class Port(Base):
    __tablename__ = 'ports'
    code = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    parent_slug = Column(String, ForeignKey('regions.slug'), nullable=False)


class Region(Base):
    __tablename__ = 'regions'
    slug = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    parent_slug = Column(String, ForeignKey('regions.slug'), nullable=True)


class Price(Base):
    __tablename__ = 'prices'
    orig_code = Column(String(), ForeignKey('ports.code'), primary_key=True)
    dest_code = Column(String(), ForeignKey('ports.code'), primary_key=True)
    day = Column(DateTime, primary_key=True)
    price = Column(Integer, primary_key=True, autoincrement=False)