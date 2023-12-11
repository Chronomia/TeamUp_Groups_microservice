from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String, Integer
from sqlalchemy import MetaData

meta = MetaData()

"""
Model for sqlalchemy engine
"""

teamup_group_data = Table(
    'teamup_group_data', meta, 
    Column('group_id', String),
    Column('groupname', String),
    Column('organizer', String),
    Column('location', String),
    Column('category', String),
    Column('intro', String),
    Column('policy', String)
)

teamup_group_user_data = Table(
    'teamup_group_user_data', meta,
    Column('group_id', String),
    Column('username', String)
)

teamup_group_event_data = Table(
    'teamup_group_event_data', meta,
    Column('group_id', String),
    Column('event_id', Integer)
)