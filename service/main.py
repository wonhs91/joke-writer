from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from agent import joke_writer_agent, Associations
from pydantic import BaseModel
import logging
import uuid
from collections import defaultdict

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
)

thread_store = defaultdict(dict)

class KeywordsReq(BaseModel):
  keywords: list[str]

class PickedAssociationsReq(BaseModel):
  picked_associations: list[Associations]

@app.post("/api/joke-writer/associations")
async def joke_writer(keywords: KeywordsReq):
  state = keywords.model_dump()
  thread_id = str(uuid.uuid4())
  config = {'configurable': {'thread_id': thread_id}}
  thread_store[thread_id] = {'config': config, 'initial_state': state}  
  retries = 2
  while True:
    try: 
      # response = joke_writer_agent.invoke(state, config)
      break
    except Exception as e:
      if (retries == 0):
        raise HTTPException(status_code=500, detail="There was an error while getting keywords associations.")
      retries -= 1
      logging.error(f'there was an error while getting keywords associations. number of retries remaining: {retries}')
      logging.error(e)
  response = {
    "keywords": [
      "string"
    ],
    "keywords_associations": [
      {
        "keyword": "string",
        "associations": [
          "Musical connections: Strings as musical instruments (violins, guitars), famous string quartets, or a string of bad luck.",
          "Fishing and knots: Fishing lines, knot-tying challenges, or the frustration of getting a knot stuck in your line.",
          "Garden humor: Garden strings for twining plants, gardening mishaps involving strings (e.g., accidentally tying yourself to a trellis).",
          "Language and words: The phrase “ing along’ from jazz music, linguistic concepts like strings (as in string theory), or the annoyance of typing out repetitive sentences.",
          "Food and cooking: Spaghetti with meatballs (a classic “ing–like dish), string cheese, or the frustration of trying to cook a turkey without drying it out into a “ing.’.",
          "Silly associations: A giant, talking string figure, a string of failed attempts at becoming a superhero.",
          "Clichés and idioms: The phrase “ing along,’ pulling strings from behind the scenes, or the idea that someone is “twisting your arm‗ into doing something."
        ]
      },
      {
        "keyword": "Not String",
        "associations": [
          "111Musical connections: Strings as musical instruments (violins, guitars), famous string quartets, or a string of bad luck.",
          "222Fishing and knots: Fishing lines, knot-tying challenges, or the frustration of getting a knot stuck in your line.",
          "333Garden humor: Garden strings for twining plants, gardening mishaps involving strings (e.g., accidentally tying yourself to a trellis).",
          "444Language and words: The phrase “ing along’ from jazz music, linguistic concepts like strings (as in string theory), or the annoyance of typing out repetitive sentences.",
          "555Food and cooking: Spaghetti with meatballs (a classic “ing–like dish), string cheese, or the frustration of trying to cook a turkey without drying it out into a “ing.’.",
          "666Silly associations: A giant, talking string figure, a string of failed attempts at becoming a superhero.",
          "777Clichés and idioms: The phrase “ing along,’ pulling strings from behind the scenes, or the idea that someone is “twisting your arm‗ into doing something."
        ]
      }
    ]
  }
  thread_store[thread_id]['association_response'] = response 

  return {"thread_id": uuid.uuid4(), 'agent_response': response}

@app.post("/joke-writer/joke/{thread_id}")
async def write_joke(thread_id: str, picked_associations_req: PickedAssociationsReq):
  keywords_associations = []
  
  for keyword_association in picked_associations_req.picked_associations:
    try:
      keywords_associations.append(Associations(keyword=keyword_association.keyword, associations=keyword_association.associations))
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
  