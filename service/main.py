from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from agent import joke_writer_agent, Associations
from pydantic import BaseModel
import logging
import uuid
from collections import defaultdict

app = FastAPI()

thread_store = defaultdict(dict)

class Keywords(BaseModel):
  keywords: list[str]



@app.post("/joke-writer/associations")
async def joke_writer(keywords: list[str]):
  state = {
    'keywords': keywords
  }
  thread_id = str(uuid.uuid4())
  config = {'configurable': {'thread_id': thread_id}}
  thread_store[thread_id] = {'config': config, 'initial_state': state}  
  retries = 2
  while retries > 0:
    try: 
      response = joke_writer_agent.invoke(state, config)
      break
    except Exception as e:
      retries -= 1
      logging.error(f'there was an error while getting keywords associations. number of retries remaining: {retries}')
      logging.error(e)

  thread_store[thread_id]['association_response'] = response 

  return {"thread_id": uuid.uuid4(), 'response': response}

@app.post("/joke-writer/joke/{thread_id}")
async def write_joke(thread_id: str, keywords_associations: list[Associations]):
  picked_associations = []
  
  for association in keywords_associations:
    try:
      picked_associations.append(Associations(keyword=association.keyword, associations=association.associations))
    except Exception as e:
      logging.error(f'there was an error while parsing user input.')
      logging.error(e)
  
  config = thread_store.get(thread_id).get('config', None)
  
  retries = 2
  while retries > 0:
    try: 
      joke_writer_agent.update_state(config=config, values={'picked_associations': picked_associations}, as_node="human_pick_associations")
      response = joke_writer_agent.invoke(None, config)
      break
    except Exception as e:
      retries -= 1
      logging.error(f'there was an error while joke writing. number of retries remaining: {retries}')
      logging.error(e)
    
  return response
  