
import operator


from strawberry.schema.config import StrawberryConfig
from enum import Enum
import sys

import uvicorn

sys.path.append("database")
from typing import Optional, List, Union
import strawberry
from strawberry.asgi import GraphQL

from strawberry.fastapi import GraphQLRouter
from enum import Enum

from .mutation_functions import *
from .query_functions import *


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
    scps: Optional[List[str]] #list of strings that are the scps id documents
    player_guild_id: Guild




@strawberry.type
class Query:
  
    all_scp: list[SCP] = strawberry.field(resolver=get_all_scp_schema) 
    scp_by_item: SCP = strawberry.field(resolver=get_scp_byItem_schema)
    scpRank: list[SCP] = strawberry.field(resolver=get_ranking_scp_schema)
    randomScp: SCP = strawberry.field(resolver=get_random_scp_schema)
    player: Player = strawberry.field(resolver=get_player_in_guild)
    playerRank: list[Player] = strawberry.field(resolver=get_player_ranking_schema)
    playerSCP: list[SCP] = strawberry.field(resolver=get_player_scps)
    

@strawberry.type
class Mutation:
    
    addPlayer: Player = strawberry.mutation(resolver=add_player_schema)
    updatePlayerScp: str  = strawberry.mutation(resolver=update_player_scps_schema)
    updatePlayerXp: str = strawberry.mutation(resolver=update_player_xp_schema)
    updateScpClaims: SCP = strawberry.field(resolver=update_scp_claims_schema)
    #updateXpPlayer


def default_resolver(root, field):  #strawberry não permite o retorno de dicionários por padrão para isso é necessário fazer essa config
    try:
        return operator.getitem(root, field)
    except KeyError:
        return getattr(root, field)


# def default_resolver(root: dict, field: str) -> Union[str, int, dict, None]:
#     if isinstance(root, dict):
#         return root.get(field)
#     elif isinstance(root, list):
#         return [item.get(field) if item else None for item in root]
#     return None


config = StrawberryConfig(
    default_resolver=default_resolver
)



def main():
    # schema = strawberry.Schema(query=Query, mutation=Mutation,config=config)
    # app = GraphQL(schema)
    # uvicorn.run(app, host="0.0.0.0", port=8000)    
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation,config=config)

#graphql_app = GraphQLRouter(schema)