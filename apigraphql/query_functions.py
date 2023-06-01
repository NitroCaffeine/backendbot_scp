import sys
sys.path.append("database")

#from .schema import SCP, Player
from database.playerProcedures import PlayerDBProcedures as PlayerDB
from database.scpProcedures import ScpDBProcedures as SCPDB


scpdb = SCPDB()
playerdb = PlayerDB()


async def get_all_scp_schema():
        scplist = await scpdb.get_all_scp()
        return scplist

async def get_scp_byItem_schema(item: str):
        scp = await scpdb.get_scp_by_item(item=item)
        return scp

async def get_ranking_scp_schema(qtd: int):  #qtd = top10 or top100 
        scp = await scpdb.get_ranking_scp(qtd)
        return scp

async def get_player_ranking_schema(qtd: int):
        playerlist = await playerdb.get_player_ranking(qtd)
       

        return playerlist

async def get_player_scps(player_discord_id: str, player_guild_id: str):
        player_scps = await playerdb.get_player_scps(player_discord_id, player_guild_id)
        return player_scps

async def get_player_in_guild(player_discord_id: str, player_guild_id: str):
        player = await playerdb.get_player_in_guild(player_discord_id, player_guild_id)
        return player['data']