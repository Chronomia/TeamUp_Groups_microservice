import strawberry
import typing
from config.db import conn
from models.group import teamup_group_data


"""
Resource Model, Query Model for GraphQL API response 
"""

@strawberry.type
class Group:
    group_id: str
    group_name: str
    founder: str
    city: str
    state: str
    category: str
    intro: str
    policy: str

@strawberry.type
class Query:
    @strawberry.field
    def group(self, group_id: str) -> Group:
        return conn.execute(teamup_group_data.select().where(teamup_group_data.c.group_id == group_id)).fetchone()
    @strawberry.field
    def groups(self) -> typing.List[Group]:
        return conn.execute(teamup_group_data.select()).fetchall()