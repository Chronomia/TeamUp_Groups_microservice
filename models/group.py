from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import String
from sqlalchemy import MetaData

meta = MetaData()

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
