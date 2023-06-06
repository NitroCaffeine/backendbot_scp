
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


if __name__ == "__main__":
  uvicorn.run("server.api:app", host="0.0.0.0", port=8000, reload=True)



