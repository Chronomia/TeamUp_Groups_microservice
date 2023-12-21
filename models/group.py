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
    Column('group_name', String),
    Column('founder', String),
    Column('city', String),
    Column('state', String)
    Column('category', String),
    Column('intro', String),
    Column('policy', String)
)

teamup_group_member_rel_data = Table(
    'teamup_group_member_rel', meta,
    Column('group_id', String),
    Column('username', String)
)