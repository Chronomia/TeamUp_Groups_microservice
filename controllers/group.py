
from fastapi import APIRouter
import strawberry
from type.group import Query
from strawberry.asgi import GraphQL

graphql_router = APIRouter()
schema = strawberry.Schema(Query)
graphql_app = GraphQL(schema)

graphql_router.add_route('/graphql', graphql_app)