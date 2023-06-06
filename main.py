
import sys
from fastapi import FastAPI, Request
sys.path.append("api")
from strawberry.fastapi import GraphQLRouter
from apigraphql.schema import schema, main

from api.api import graphql_app
import uvicorn
#from api.endpoints.scp import router as scp



# graphql_app = GraphQLRouter(schema)
# graphql_app.include_router(scp, prefix="/scp")



app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
#app.add_websocket_route('/graphql', graphql_app)

# dados = "item , name"
# @app.get("/allSCP")
# async def read_item(request: Request):  
#     redirect_url = f"/graphql?query={{allScp{{item, name, scpoints, image, claims, objectClass}}}}"
#     return RedirectResponse(url=redirect_url)

# @app.get("/scpByItem/{item}")
# async def read_item(request: Request, item: str):
#     redirect_url = f"/graphql?query={{scpByItem(item: \"{item}\"){{{dados}}}}}"
#     return RedirectResponse(url=redirect_url)



uvicorn.run(app, host="0.0.0.0", port=8000)    
#
#main()

