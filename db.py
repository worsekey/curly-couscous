from sqlalchemy import (Date,
                        Float,
                        Column,
                        Integer,
                        String,
                        ForeignKey,
                        create_engine
                        )
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    tuser_id = Column(String(12))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer(), primary_key=True)
    cat_name = Column(String(50))
    tuser_id = Column(String(12))

    # time = relationship('Time', cascade='all, delete', backref='category', passive_deletes=True)


class Time(Base):
    __tablename__ = 'time_track'

    id = Column(Integer(), primary_key=True)
    cat_id = Column(String(), ForeignKey('category.id', ondelete='CASCADE'))
    start_date = Column(Date())
    start_time = Column(Float())
    stop_date = Column(Date())
    stop_time = Column(Float())
    time_delta = Column(Float())


engine = create_engine('sqlite:///db_2.sqlite')
Base.metadata.create_all(engine)
