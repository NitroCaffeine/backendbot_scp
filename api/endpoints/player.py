
import sys
sys.path.append("apigraphql")

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from apigraphql.schema import schema



router = APIRouter()

data = "playerDiscordId, level, name, scpoints , currentXp, title, className"
data_scp = "item, name, scpoints, image, claims, objectClass"


# redirect_url = f"/graphql?query={{player(playerDiscordId: \"{player_discord_id}\", playerGuildId: \"{player_guild_id}\"){{ {data} }}}}"
    # return RedirectResponse(url=redirect_url)


@router.get("/{player_discord_id}/{player_guild_id}")
async def get_player(player_discord_id: str, player_guild_id: str, data:str = data):
    
    try:
        query = f""" query {{player(playerDiscordId: "{player_discord_id}", playerGuildId: "{player_guild_id}"){{ {data} }}}}"""
        variables= {
            "playerDiscordId": player_discord_id,
            "playerGuildId": player_guild_id
        }

        result = await schema.execute(query, variable_values=variables)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args)


  # redirect_url = f"/graphql?query={{playerRank(qtd: {qtd}){{ {data} }}}}"
    # return RedirectResponse(url=redirect_url)
@router.get("/rank/{qtd}")
async def get_playerRank(qtd: int, data:str = data):
  
    try:
        query = f""" query {{playerRank(qtd: {qtd}){{ {data} }}}}"""

        variables = {
            "qtd": qtd
        }
        result = await schema.execute(query, variable_values=variables)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args)


# redirect_url = f"/graphql?query={{playerSCP(playerDiscordId: \"{player_discord_id}\", playerGuildId: \"{player_guild_id}\"){{ {data} }}}}"
    # return RedirectResponse(url=redirect_url)

@router.get("{player_discord_id}/{player_guild_id}/scps")
async def get_playerScps(player_discord_id: str, player_guild_id: str, data: str = data_scp):
    
    try:
        query = f""" query {{
                playerSCP(playerDiscordId: "{player_discord_id}", playerGuildId: "{player_guild_id}") 
                {{  {data}   }}

        }}"""

        variables = {
            "playerDiscordId": player_discord_id,
            "playerGuildId": player_guild_id
        }
        result = await schema.execute(query, variable_values=variables)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args)




@router.post("{player_discord_id}/{player_guild_id}/add")
async def add_player(player_discord_id: str, player_guild_id: str, name: str):
    try:
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
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args)
        
    #r = requests.post(url="https://api.apigraphql.com/graphql", json={"query": query}

    #router.post("/graphql)
    

@router.put("{player_discord_id}/{player_guild_id}/add/scp")
async def update_playerSCP(player_discord_id: str, player_guild_id: str, scp_documentID: str):
   
    try:
        query = f"""
        mutation {{
                updatePlayerScp(playerDiscordId: "{player_discord_id}", playerGuildId: "{player_guild_id}", scpDocumentid: "{scp_documentID}") 
            }}
        """

        variables = {
            "playerDiscordId": player_discord_id,
            "playerGuildId": player_guild_id,
            "scpDocumentid": scp_documentID
        }

        result = await schema.execute(query, variable_values=variables)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args)

@router.put("{player_discord_id}/{player_guild_id}/xp")
async def update_playerXp(player_discord_id: str, player_guild_id: str):
    try:
        query = f"""
        mutation {{
                updatePlayerXp(playerDiscordId: "{player_discord_id}", playerGuildId: "{player_guild_id}") 
            }}
        """

        variables = {
            "playerDiscordId": player_discord_id,
            "playerGuildId": player_guild_id
        }

        result = await schema.execute(query, variable_values=variables)
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=e.args)