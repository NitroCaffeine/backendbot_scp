
import importlib
import operator


from strawberry.schema.config import StrawberryConfig
from enum import Enum
import sys

import uvicorn

sys.path.append("database")
from typing import Optional, List
import strawberry
from strawberry.asgi import GraphQL

from strawberry.fastapi import GraphQLRouter
from enum import Enum

from .mutation_functions import *
from .query_functions import *
# from .mutation_functions import *

# importlib.import_module(".query_functions", package="query_functions")
# importlib.import_module(".mutation_functions", package="mutation_functions")

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


# @strawberry.enum
# class PlayerClass(Enum):
#     classA= 'A'
#     classB= 'B'
#     classC='C'
#     classD = 'D'
#     classE = 'E'

# @strawberry.enum
# class PlayerLevel(Enum):
#     level1= 1
#     level2= 2
#     level3= 3
#     level4 = 4
#     level5 = 5

@strawberry.enum 
class PlayerTitle(Enum):
    ContainmentSpecialist: str = 'Containment Specialist'
    Researcher: str= 'Researcher'
    SecurityOfficer: str= ' Security Officer'
    TacticalResponseOfficer : str= 'Tactical Response Officer'
    SiteDirector : str= 'Site Director'
    O5CouncilMember : str= 'O5 Council Member'
    MobileTaskForceOperative: str = 'Mobile Task Force Operative'

@strawberry.type
class Player:
    player_discord_id: str
    name: str
    scpoints: Optional[int]
    title: PlayerTitle
    current_xp: Optional[int]
    level: int 
    class_name: str
    scps: Optional[List[SCP]]
    player_guild_id: Guild

    # @strawberry.field
    # def level(self) -> int:
    #     return self.level.value if isinstance(self.level, PlayerLevel) else self.level

    # @strawberry.field
    # def class_name(self) -> str:
    #     return self.class_name.value if isinstance(self.class_name, PlayerClass) else self.class_name


@strawberry.type
class Query:
  
    all_scp: list[SCP] = strawberry.field(resolver=get_all_scp_schema) 
    scp_by_item: SCP = strawberry.field(resolver=get_scp_byItem_schema)
    scpRank: list[SCP] = strawberry.field(resolver=get_ranking_scp_schema)
    player: Player = strawberry.field(resolver=get_player_in_guild)
    playerRank: list[Player] = strawberry.field(resolver=get_player_ranking_schema)
    playerSCP: list[SCP] = strawberry.field(resolver=get_player_scps)
    

@strawberry.type
class Mutation:
    
    addPlayer: Player = strawberry.mutation(resolver=add_player_schema)
    updatePlayerScp: str  = strawberry.mutation(resolver=update_player_scps_schema)


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

#graphql_app = GraphQLRouter(schema)