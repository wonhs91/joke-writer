from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import logging
import uuid
from collections import defaultdict

from agent import association_agent, joke_agent, KeysAssociations, JokeMaterials

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

class ThreadData(BaseModel):
  config: dict = {}
  associations_result: dict = {}
  joke_result: dict = {}
  

thread_store = defaultdict(Dict[str, ThreadData])

class associationsReqBody(BaseModel):
  keywords: list[str]
  
@app.post("/api/joke-writer/associations")
async def joke_writer(req_body: associationsReqBody):
  state = req_body.model_dump()
  
  thread_id = str(uuid.uuid4())
  config = {'configurable': {'thread_id': thread_id}}
  thread_store[thread_id] = ThreadData(config=config)
  
  retries = 2
  while True:
    try: 
      return_state = association_agent.invoke(state, config)
      break
    except Exception as e:
      if (retries == 0):
        raise HTTPException(status_code=500, detail="There was an error while getting keywords associations.")
      retries -= 1
      logging.error(f'there was an error while getting keywords associations. number of retries remaining: {retries}\n{e}')

  response = {"thread_id": thread_id }
  response.update(return_state['keywords_associations'])
  return response

@app.post("/api/joke-writer/joke/{thread_id}")
async def write_joke(thread_id: str, joke_materials: Dict[str, str]):
  
  try:
    state = {
    'joke_material': JokeMaterials(materials=joke_materials)
    }
  except Exception as e:
    raise HTTPException(status_code=400, detail="Invalid joke materials. Make sure to be in the format {'keyword': 'association'}.")

  
  thread_data = thread_store.get(thread_id, None)
  
  if not thread_data:
    raise HTTPException(status_code=400, detail="Invalid thread id.")
  
  
  retries = 2
  while retries > 0:
    try: 
      return_state = joke_agent.invoke(state, thread_data.config)
      break
    except Exception as e:
      retries -= 1
      logging.error(f'there was an error while joke writing. number of retries remaining: {retries}\n{e}')
  
  return return_state
  