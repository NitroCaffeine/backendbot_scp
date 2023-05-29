from faunadbConnect import faunadbConnect 
from faunadb import query as q

#from streamFaunadb import main_stream, list

xp_verify_update_level_class_title = [
    {'xp': 400, 'title': 'Researcher', 'class': 'D'},
    {'xp': 1600, 'title': 'Security Officer', 'class': 'C'},
    {'xp': 2200, 'title': 'Tactical Response Officer', 'class': 'B'},
    {'xp': 5600,  'title': 'Mobile Task Force Operative', 'class': 'A'}
]

class PlayerDBProcedures(faunadbConnect):
    def __init__(self) -> None:
        pass

    def verify_player_exists(self, player_discord_id):
        query = q.exists(q.match(q.index("player_by_discord_id"), player_discord_id))   #verifica se o player existe no faunadb                
        response = self.client.query(query)
        return response
        
    def verify_player_exists_in_guild(self, player_discord_id, player_guild_id ): 
        try: 
            query = q.if_( q.exists(q.match(q.index("player_by_discord_and_guild_id"), player_discord_id, player_guild_id)), 
                                       q.get(q.match(q.index("player_by_discord_and_guild_id"), player_discord_id, player_guild_id)),
                                       q.abort("player not found")
                                    ),
            response = self.client.query(query)

            return response[0]
        except Exception as e:
            return e.args[0]

    async def add_player(self, player_discord_id, name, guild_id, level, class_name, title) -> str:   
        try:            
                # verifca se o player já existe naquele servidor
                query = q.if_(self.verify_player_exists_in_guild(player_discord_id,guild_id ),
                            q.abort("Player já existe"),

                            q.create(q.collection("Player"), 
                                    {"data": {
                                        "player_discord_id": player_discord_id,
                                        "name": name,
                                        "guild_id": guild_id,
                                        "scpoints": 0,
                                        "current_xp": 0,
                                        "level": level,
                                        "class_name": class_name,
                                        "title": title
                                    }
                                    
                    }
                    )
                            
                )  
                await self.client.query(query)
                
                #return "Inserido com sucesso"
        except Exception as e:
            return e.args[0]
    

    async def update_xp_player(self, document):
        try:
            query = q.let({
                "doc": document, 
                "ref": q.select(["ref"], q.var("doc")),
                "old_value_xp": q.select(["data","current_xp"], q.var("doc")),
            },
                q.update(
                    q.var("ref"),
                    {
                        "data": {
                            "current_xp": q.add(q.var("old_value_xp"), 10)
                        }
                    }
                ),
            q.select(["data","current_xp"], q.var("doc"))
            )

            response = await self.client.query(query)
            for dict in xp_verify_update_level_class_title:
                if response["data"]["current_xp"] == dict['xp']:  #verifica se a xp atual do player corresponde a xp mínima para passar pra um determinado level
                    await self.update_level_class_title_player(document, dict['class'], dict['title'])
                    break

            
          
        except Exception as e:
            return e.args[0]
    
    
    async def update_level_class_title_player(self, document, class_, title):
        try: 
            query  = q.let(
                {
                    "doc": document, 
                    "ref": q.select(["ref"], q.var("doc")),
                    "old_level_value": q.select(["data","level"], q.var("doc"))
                },
                q.update(
                    q.var("ref"),
                    {
                        "data": {
                            "level": q.add(q.var("old_level_value"), 1),
                            "class_name": class_,
                            "title": title
                        }
                    }
                )
            )
            await self.client.query(query)
           

        except Exception as e:
            return e.args[0]
        
    async def update_player_scpoints(self, document, scp_documentID):
        try :
            query = q.let(
                
                {
                    "doc": document, 
                    "old_scpoints" : q.select(["data", "scpoints"], q.var("doc")),
                    "scp_value" : q.select(["data", "scpoints"],q.get(q.ref(q.collection("SCP"), scp_documentID))),
                                 
                },

                q.update(
                    q.select(["ref"], q.var("doc")),
                    {
                        "data": {
                            "scpoints": q.add(q.var("old_scpoints"), q.var("scp_value"))
                        }
                    }
                )
            
            )

            await self.client.query(query)
            # print(response)
            # return response
        
        except Exception as e:
            return e.args[0]
        
        
    async def update_player_scps(self, player_discord_id, player_guild_id, scp_documentID):
        try:
            query = q.let({
                 "doc": self.verify_player_exists_in_guild(player_discord_id, player_guild_id), 
                 "containsField": q.contains_field("scplist", q.select("data", q.var("doc"))),
                 "ref": q.select(["ref"], q.var("doc"))          
            }, 
                
            q.if_(
                    q.var("containsField"),
                    q.let({
                                "old_value_scplist": q.select(["data","scplist"], q.var("doc")), 
                                "scp_not_exists_in_player_list" : q.is_empty(q.filter_( q.lambda_("i", q.equals(q.var("i"), scp_documentID)),q.var("old_value_scplist")))      
                    },
                        q.update(
                            q.var("ref"),
                            {
                                "data": {
                                    "scplist": q.if_(q.var("scp_not_exists_in_player_list"),
                                                
                                                    q.append(q.var("old_value_scplist"), [scp_documentID]),
                                                    q.abort("already exists"))
                                }
                            }
                        )
                        
                        
                    ),
                    q.update(
                            q.var("ref"),
                            {
                                "data": {
                                    "scplist": [scp_documentID]
                                }
                            }
                    )

                ),

            q.var("doc")
            
            )
                        
            document = await self.client.query(query)
            await self.update_xp_player(document)
            print("exec")
            await self.update_player_scpoints(document, scp_documentID)

        except Exception as e:
            return e.args[0]
        
    def show_player_ranking(self,qtd): 
        
        try:
            collection_data =[]
            
            query = q.select("data", q.paginate(q.match(q.index("player_sort_by_scpoints_desc")), size=qtd))
            response = self.client.query(query)

            #print(response)
            for i in response: 

                
                    new_query = q.get(q.ref(q.collection("Player"), i[1].id()))
                    new_response = self.client.query(new_query)
                    collection_data.append(new_response['data'])
                
            
            return collection_data


        except Exception as e:
            return e.args[0]
    
    def get_player_scps(self, player_discord_id, player_guild_id):
        try:
            query = q.let(
                    {
                    "doc": self.verify_player_exists_in_guild(player_discord_id, player_guild_id),
                    "containsField": q.contains_field("scplist", q.select("data", q.var("doc"))),
                    "ref": q.select(["ref"], q.var("doc")),
                    },
                    q.if_(
                        q.var("containsField"),
                        q.let(
                            {       
                            "scplist": q.select(["data","scplist"], q.var("doc")),
                            "scplist_size": q.count(q.var("scplist")),
                            #"scplist_paginate": q.paginate(q.var("scplist"), size=q.var("scplist_size")),
                            "scp_result":  q.map_(q.lambda_("ref_scp", q.select("data", q.get(q.ref(q.collection("SCP"), q.var("ref_scp"))))), q.var("scplist"))
                            },
                           
                            q.var("scp_result")
                        ),
                        []
                    ),
            )

            response = self.client.query(query)
            return response
           
        except Exception as e: 
              return e
        
 
 
obj = PlayerDBProcedures()
#addplayer 
#print(obj.add_player("2", "beatriz", "23"))
#print(obj.verify_player_exists_in_guild("221","45"))
#print(obj.get_player_scps("21","45"))
#print(obj.update_player_scps("221","45", "365097077591507024"))
#obj.update_xp_player("12345", "guild_id_12389")
#print(obj.verify_xp_player(5678, 123))

#obj.update_player_scps(123456, 123, 8888)
#obj.add_player("12345", "teste 2", "guild_id_12389", 0, 'SLA',"TITULO")

#from streamFaunadb import action
#testeobj.verify_player(12345)
# print(testeobj.teste) #.client
# selecionar o document via index 
# q.get(q.match(q.index("player_by_discord_id"), 12345))
#atualizar o campo scplits(caso exista) com o valor anterior + um novo valor, caso não exista criar o campo e adicionar o valor informado
# q.update(q.select("ref", q.get(q.match(q.index("player_by_discord_id"), 12345))), {
#  
# }