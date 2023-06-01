from fastapi import APIRouter
from fastapi.responses import RedirectResponse

router = APIRouter()


data = "item, name, scpoints, image, claims, objectClass"

@router.get("/all")
async def get_allscp(data: str = data):  
    redirect_url = f"/graphql?query={{allScp{{ {data} }}}}"
    return RedirectResponse(url=redirect_url)

@router.get("/{item}")
async def get_scpByItem(item: str, data: str = data):
    redirect_url = f"/graphql?query={{scpByItem(item: \"{item}\"){{ {data} }}}}"
    return RedirectResponse(url=redirect_url)

@router.get("/rank/{qtd}")
async def get_rankingScp(qtd: int, data: str = data):
    redirect_url = f"/graphql?query={{scpRank(qtd: {qtd}){{ {data} }}}}"
    return RedirectResponse(url=redirect_url)




