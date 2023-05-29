import os, sys
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient


#from SCP.scp import scpClass
#import json

from dotenv import load_dotenv


load_dotenv()

FAUNADB_KEY= os.getenv("FAUNADB_SERVER_KEY")

class faunadbConnect:
    _client  = FaunaClient(secret=FAUNADB_KEY)
   
    def __init__(self) -> None: 
        pass
   

    @property
    def client(self):
        return self._client 
       

def insert_scp_allData(client,*scpData):   # function to store all scp's data in faunadb, not more necessary
        for data in scpData:
            for item in data.items():
                try:
                    client.query(
                        q.create(
                            q.collection("SCP"),
                            {"data": item[1]}
                        )
                    )
                except:
                    print(f"SCP {item[0]} já existe no banco de dados ou deu ruim")
        


#scpData = scpClass().dict_scp
#connection= faunadbConnect().client
#insert_scp_allData(connection, scpData)


#json_object = json.dumps(dict_scp, indent = 9)
#with open ("scp_data.json", "w") as outfile:
    #outfile.write(json_object)

#print(json_object)

       

