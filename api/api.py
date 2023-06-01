import sys
sys.path.append("apigraphql")
from fastapi import APIRouter

from apigraphql.schema import main, schema
from strawberry.fastapi import GraphQLRouter
from endpoints.scp import router as scpRouter
from endpoints.player import router as playerRouter

graphql_app = GraphQLRouter(schema)

graphql_app.include_router(scpRouter, prefix="/scp")
graphql_app.include_router(playerRouter, prefix="/player")

