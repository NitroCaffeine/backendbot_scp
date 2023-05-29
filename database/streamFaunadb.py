from faunadbConnect import faunadbConnect 
from faunadb import query as q
#import asyncio 


def main_stream():
    client = faunadbConnect().client
    options= { "fields": [ 'action', 'document' ]}

    collection_ref= client.query(q.documents(q.collection("Player")))
        
    def on_start(event):

        print("started stream at %s"%(event.txn))

    def on_set(event):
        print("on_set event at %s"%(event.txn))
        #print("set event: %s"%(event.event['action']))
        
        action = event.event['action']
        list.append(action)

    def on_error(event):
        print("Received error event %s"%(event))



    
    stream = client.stream(collection_ref, options, on_start, on_error, None, None, on_set)

    stream.start()
    stream.join()
    
list = []

