import sys
sys.path.append("apigraphql")

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from apigraphql.schema import schema

router = APIRouter()


data = "item, name, scpoints, image, claims, objectClass"

@router.get("/all")
async def get_allscp(data: str = data):  
    # redirect_url = f"/graphql?query={{allScp{{ {data} }}}}"
    # return RedirectResponse(url=redirect_url)
    try:
            query = f"""
                    query {{allScp     
                    {{ 
                        {data} 
                    }}
                }}
            """

            result = await schema.execute(query)
            return result
           
    except Exception as e:
          raise HTTPException(status_code=404, detail=e.args)

@router.get("/{item}")
async def get_scpByItem(item: str, data: str = data):
    # redirect_url = f"/graphql?query={{scpByItem(item: \"{item}\"){{ {data} }}}}"
    # return RedirectResponse(url=redirect_url)

    try:
            query = f""" 
                
                query {{scpByItem(item: "{item}")               
                    {{ 
                        {data} 
                    
                    }}
                
                }}
            """

            variables = { 
                 "item": item
            }
        
            result = await schema.execute(query, variable_values=variables)
            return result
    except Exception as e:
            raise HTTPException(status_code=404, detail=e.args)

@router.get("/rank/{qtd}")
async def get_rankingScp(qtd: int = 10, data: str = data):
    # redirect_url = f"/graphql?query={{scpRank(qtd: {qtd}){{ {data} }}}}"
    # return RedirectResponse(url=redirect_url)
    try:
            query = f""" 
                query {{scpRank(qtd: {qtd})
                    {{ 
                        {data} 
                    }}
                }}
            """

            variables = { 
                 "qtd": qtd
            }
        
            result = await schema.execute(query, variable_values=variables)
            return result
    except Exception as e:
            raise HTTPException(status_code=404, detail=e.args)
    


@router.get("/random")
async def get_randomScp(data: str = data):
    try:
        query = f"""
                    query {{randomScp     
                    {{ 
                        {data}
                    }}
                }}
            """
    
        result = await schema.execute(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    
@router.put("/{scp_document_id}/claim")
async def update_scp_claims(scp_document_id: str, data:str = data):
    try:
        query = f"""
            mutation {{
                updateScpClaims(scpDocumentid: "{scp_document_id}") {{
                    {data}
                }}
            }}
        """ 

        variables = {
             "scpDocumentid": scp_document_id
        }
        
        result = await schema.execute(query,variable_values=variables)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)
    




