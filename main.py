
import sys
from fastapi import FastAPI
sys.path.append("api")
#from strawberry.fastapi import GraphQLRouter
#from apigraphql.schema import schema, main

from api.api import graphql_app
import uvicorn


app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
#app.add_websocket_route('/graphql', graphql_app)


uvicorn.run(app, host="0.0.0.0", port=8000)    



