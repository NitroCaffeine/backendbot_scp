
import operator
import typing

from strawberry.schema.config import StrawberryConfig
from enum import Enum
import sys

import uvicorn

sys.path.append("database")
from typing import Any, Optional, List, Any
import strawberry
from strawberry.asgi import GraphQL
import asyncio

from database.scpProcedures import ScpDBProcedures as SCPDB
from database.playerProcedures import PlayerDBProcedures as PlayerDB

@strawberry.type
class SCP:
    item: str
    name: str
    object_class: str
    image: str
    scpoints: int
    claims: int


@strawberry.type
class Guild:
    id: str
    name: str


@strawberry.enum
class PlayerClass(Enum):
    classA= 'Class A'
    classB= 'Class B'
    classC='Class C'
    classD = 'Class D'
    classE = 'Class E'

@strawberry.enum
class PlayerLevel(Enum):
    level1= 1
    level2= 2
    level3= 3
    level4 = 4
    level5 = 5

@strawberry.enum 
class PlayerTitle(Enum):
    ContainmentSpecialist = 'Containment Specialist'
    Researcher= 'Researcher'
    SecurityOfficer= ' Security Officer'
    TacticalResponseOfficer = 'Tactical Response Officer'
    SiteDirector = 'Site Director'
    O5CouncilMember = 'O5 Council Member'
    MobileTaskForceOperative = 'Mobile Task Force Operative'

@strawberry.type
class Player:
    id: str
    name: str
    scpoints: Optional[int]
    title: PlayerTitle
    current_xp: Optional[int]
    level: PlayerLevel
    class_name: PlayerClass
    scps: Optional[List[SCP]]
    guild: Guild




scpdb = SCPDB()
playerdb = PlayerDB()


@strawberry.type
class Query:
  
        
    @strawberry.field
    def get_guild_schema(self) -> Guild:
        return Guild(id=1, name="Test Guild")
        
    @strawberry.field
    async def get_all_scp_schema(self) -> list[SCP]:
        scplist = await scpdb.get_all_scp()
        return scplist
    
    @strawberry.field
    async def get_scp_byItem_schema(self, item: str) -> SCP:
         scp = await scpdb.get_scp_by_id(item=item)
         return scp
    
    @strawberry.field
    async def get_ranking_scp_schema(self, qtd: int) -> list[SCP]:  #qtd = top10 or top100 
         scp = await scpdb.get_ranking_scp(qtd)
         return scp
    
    

@strawberry.type
class Mutation:
    
    

    @strawberry.mutation
    async def add_player_schema(
        self,
        player_discord_id: str,
        name: str,
        guild_id: str,
        level: str = PlayerLevel.level1.value,  # Usando o valor primitivo do enum
        class_name: str = PlayerClass.classE.value,  # Usando o valor primitivo do enum
        title: str = PlayerTitle.ContainmentSpecialist.value,  # Usando o valor primitivo do enum
    ) -> None:
         #consertar o negócio aqui 
        
        try:
            await playerdb.add_player(
                player_discord_id=player_discord_id,
                name=name,
                guild_id=guild_id,
                level=level,
                class_name=class_name,
                title=title
            )
        except:
            return 'Erro ao inserir'
    
    
    @strawberry.mutation
    async def update_player_scps(self, player_discord_id: str, player_guild_id: str, scp_documentID: str) -> None:
        try:
            await playerdb.update_player_scps(player_discord_id, player_guild_id, scp_documentID) #chamar todas as funções aqui         
        except:
            return 'Erro ao inserir'
       


        #return "Inserido com sucesso"
        
       


  






def default_resolver(root, field):  #strawberry não permite o retorno de dicionários por padrão para isso é necessário fazer essa config
    try:
        return operator.getitem(root, field)
    except KeyError:
        return getattr(root, field)

config = StrawberryConfig(
    default_resolver=default_resolver
)



def main():
    schema = strawberry.Schema(query=Query, mutation=Mutation,config=config)
    app = GraphQL(schema)
    uvicorn.run(app, host="0.0.0.0", port=8000)    


schema = strawberry.Schema(query=Query, mutation=Mutation,config=config)
