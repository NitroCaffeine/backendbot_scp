import sys
sys.path.append("apigraphql")

from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import requests
from apigraphql.schema import schema



router = APIRouter()

data = "playerDiscordId, level, name, scpoints , currentXp, title, className"
data_scp = "item, name, scpoints, image, claims, objectClass"

@router.get("/player")
async def get_player(player_discord_id: str, player_guild_id: str, data:str = data):
    redirect_url = f"/graphql?query={{player(playerDiscordId: \"{player_discord_id}\", playerGuildId: \"{player_guild_id}\"){{ {data} }}}}"
    return RedirectResponse(url=redirect_url)

@router.get("/rank")
async def get_playerRank(qtd: int, data:str = data):
    redirect_url = f"/graphql?query={{playerRank(qtd: {qtd}){{ {data} }}}}"
    return RedirectResponse(url=redirect_url)

@router.get("/scps")
async def get_playerScps(player_discord_id: str, player_guild_id: str, data: str = data_scp):
    redirect_url = f"/graphql?query={{playerSCP(playerDiscordId: \"{player_discord_id}\", playerGuildId: \"{player_guild_id}\"){{ {data} }}}}"
    return RedirectResponse(url=redirect_url)




#mudar todos para uma query 
@router.post("/add")
async def post_player(player_discord_id: str, player_guild_id: str, name: str):
    query = f"""
       mutation {{
            addPlayer(playerDiscordId: "{player_discord_id}", playerGuildId: "{player_guild_id}", name: "{name}") {{
                playerDiscordId
                name
            }}
        }}
    """
    
    variables = {
        "playerDiscordId": player_discord_id,
        "playerGuildId": player_guild_id
    }

    result = await schema.execute(query, variable_values=variables)
    return result
    
    #r = requests.post(url="https://api.apigraphql.com/graphql", json={"query": query}

    #router.post("/graphql)
    

@router.put("/add/scp")
async def put_playerSCP(player_discord_id: str, player_guild_id: str, scp_documentID: int):
    # redirect_url = f"/graphql?mutation={{addPlayerSCP(playerDiscordId: \"{player_discord_id}\", playerGuildId: \"{player_guild_id}\", scpDocumentID: \"{scp_documentID}\")}}"
    # return RedirectResponse(url=redirect_url)

    query = f" mutation {{addPlayerSCP(playerDiscordId: {player_discord_id}, playerGuildId: {player_guild_id}, scpDocumentid: {scp_documentID} ) }}"

    data = {"query": query}

    response = requests.post(json=data) 
    
    result = response.json()

    return result