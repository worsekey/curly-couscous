from sqlalchemy import (MetaData,
                        Table,
                        Column,
                        Integer,
                        Numeric,
                        String,
                        Float,
                        DateTime,
                        ForeignKey,
                        create_engine,
                        Date
                        )

metadata = MetaData()

user = Table('user', metadata,
             Column('id', Integer(), primary_key=True),
             Column('tuser_id', String(12))
             )

cats = Table('cats', metadata,
             Column('id', Integer(), primary_key=True),
             Column('cat_name', String(50)),
             Column('tuser_id', ForeignKey('user.tuser_id'))
             )
time_track = Table('time_track', metadata,
                   Column('id', Integer(), primary_key=True),
                   Column('cat_id', ForeignKey('cats.id')),
                   Column('start_date', Date()),
                   Column('start_time', Float()),
                   Column('stop_date', Date()),
                   Column('stop_time', Float()),
                   Column('time_delta', Float())
                   )

engine = create_engine('sqlite:///db.sqlite')
metadata.create_all(engine)