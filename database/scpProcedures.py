
import asyncio
import random
from faunadbConnect import faunadbConnect
from faunadb import query as q
from operator import itemgetter

class ScpDBProcedures(faunadbConnect):
    def __init__(self) -> None:
        pass

    async def  get_all_scp(self): #fazer função recursiva
        try:
            query = q.map_(
                    q.lambda_("doc", q.select("data", q.get(q.var("doc")))),
                    q.paginate(q.match(q.index("all_scps")), size=999))
        
            response = self.client.query(query)
            data = response["data"]
            return data
    
        except Exception as e:
            return []
    
    
    async def get_scp_by_item(self, item):
        try:
            query = q.map_(q.lambda_("doc", q.select("data", q.get(q.var("doc")))), q.paginate(q.match(q.index("scp_by_item"),item)))
            response = self.client.query(query)
            return response["data"][0]
        except Exception as e:
            return "Não encontrado"
    
    async def get_ranking_scp(self, qtd: int):
    
        try:
                        
            collection_data =[]
                        
            query = q.let( {
                            "list": q.paginate(q.match(q.index("scp_sort_by_scpoints_desc")), size=qtd),
                            "map": q.select("data", q.map_(q.lambda_("ref", q.var("ref")), q.var("list"))),
                            
                        }, q.var("map"))
            response = self.client.query(query)

                    
            for i in response: 

                        new_query = q.get(q.ref(q.collection("SCP"), i[1].id()))
                        new_response = self.client.query(new_query)
                        collection_data.append(new_response["data"])
                        
            return collection_data
        except Exception as e:
            return e
    
    async def random_scp(self):
        try:
             all_scp = self.get_all_scp()
             return random.choice(all_scp)
        except Exception as e:
            return e
    

    async def update_scp_claims(self, scp_documentID):
        try:
            query = q.update(q.ref(q.collection("SCP"), scp_documentID), {"data": {"claims": q.add(q.select(["data", "claims"], q.get(q.ref(q.collection("SCP"), scp_documentID))), 1)}})
            await self.client.query(query)

            return 'alterado com sucesso'
        except Exception as e:
            return e
          
            




            # query = q.map_(q.lambda_("ref", q.get(q.ref(["ref"][1].id()))),q.paginate(q.match(q.index("scps_by_scpoints")), size=qtd))
            # response = self.client.query(query)
            # result = response["data"]
            # data = sorted(result, key=itemgetter(3) ,reverse=True)[0:qtd]
            # for i in data: 
            #     list.append({
            #         'item': i[0],
            #         'name': i[1],
            #         'object_class': i[2],
            #         'scpoints': i[3]
            #     })
    
            # return list
        
       
    
# async def mains(): 
     
#   teste = ScpDBProcedures()
#   r = await teste.random_scp()
#   print(r)

# asyncio.run(mains())
#print(teste.get_ranking_scp(10))
# print(teste.get_ranking_scp(10))
#print(teste)
        
    



