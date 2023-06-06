import sys

from database.scpProcedures import ScpDBProcedures as SCPDB
sys.path.append("database")

from database.playerProcedures import PlayerDBProcedures as PlayerDB
#from .schema import PlayerLevel, PlayerClass, PlayerTitle

playerdb = PlayerDB()
scpdb = SCPDB()

async def add_player_schema(
        player_discord_id: str,
        name: str,
        player_guild_id: str,
        level: int = 0,  # Usando o valor primitivo do enum
        class_name: str = 'E',  # Usando o valor primitivo do enum
        title: str = 'Containment Specialist',  # Usando o valor primitivo do enum
    ):
         #consertar o negócio aqui 
        
        # try:
            response = await playerdb.add_player(
                player_discord_id=player_discord_id,
                name=name,
                player_guild_id=player_guild_id,
                level=level,
                class_name=class_name,
                title=title
            )
            return response
           
        # except:
        #     return 'error'

async def update_player_scps_schema(player_discord_id: str, player_guild_id: str, scp_documentID: str):
        
            response = await playerdb.update_player_scps(player_discord_id, player_guild_id, scp_documentID)
           
            return response  

async def update_player_xp_schema(player_discord_id: str, player_guild_id:str) :
        response = await playerdb.update_xp_player(player_discord_id, player_guild_id)
        return response



async def update_scp_claims_schema(scp_documentID: str):
        response = await scpdb.update_scp_claims(scp_documentID)
        return response['data']

      