
#api em python com fastapi e geaphql, faunadb como database e bot em javascript
# from typing import Union

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}
import sys
import threading
sys.path.append("database")

#from threading import Thread
from schema import main
from database.streamFaunadb import main_stream

# Thread(target=main).start()
# Thread(target=main_stream).start()

thread1 = threading.Thread(target=main)
#thread2 = threading.Thread(target=main_stream)

# Inicia as threads
thread1.start()
#thread2.start()

#hread2.join()

# Aguarda a conclusão das threads
#thread1.join()
#thread2.join()