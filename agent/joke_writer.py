# %%
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
from typing import Dict, List, Annotated, Literal
from pydantic import BaseModel, Field, field_validator
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, AnyMessage
from langgraph.constants import Send
from operator import add
import json
import logging

llm = ChatOllama(model='llama3.2')
# llm = ChatGroq(model="llama-3.1-70b-versatile")


# States
class Associations(BaseModel):
  """Please use this Model to to store the keyword and the associations"""
  keyword: str = Field(description="given keyword")
  associations: list[str] = Field(description="a list of ALL the associations of the keyword. Only add associations to the list")
  
  @field_validator('associations', mode="before")
  def check_associations(cls, associations):
    if isinstance(associations, str):
      try:
        associations = json.loads(associations)
      except Exception as e:
        raise ValueError("association is not a list, nor a string of list")
    return associations
  
  class Config:
    json_schema_extra  = {
      "example": {
        "keyword": "baby oil",
        "associations":  ["'Oil slick' comments (comparing someone's skin to being too shiny or greasy)"
                       "'Slick' as a term for someone trying to be smooth or charming",
                       "Tanning beds", "Smooth", "sleek",
                       "Baby oil in cooking or baking (a humorous twist on using it for skin care)"
                       ]
      },
      "example 2": {
        "keyword": "phone",
        "associations": ["Steve Jobs (co-founder of Apple and iPhone developer)",
                    "Meeting rooms with conference phones",
                    "'Hang up on someone' (to end a conversation abruptly)",
                    "Social media obsession",
                    "reach out", "get in touch", "call back", 
                    "Using a phone in a place with no signal (e.g., wilderness or a bunker)"
                    ]
      }
    }
    

class State(TypedDict):
  keywords: list[str]
  keywords_associations: Annotated[list[Associations], add]
  picked_associations: list[Associations]
  jokes: str


# %%
# Nodes and Edges
# User will provide keywords

def associations_generator(state): # do I need to provide input state type?
  # sys_msg = """
  # You are a joke-writing assistant. Given a keyword, brainstorm related topics to inspire humor. For each category, suggest relevant items:

  # Famous People/Characters: Identify well-known figures or stereotypes associated with the keyword.
  # Relevant Places: Suggest locations tied to the keyword (e.g., a gym for “fitness”).
  # Clichés & Sayings: List common phrases or stereotypes connected to the keyword.
  # Associated Objects: Identify items closely related to the keyword.
  # Current Events/Trends: Include any recent events or trends that might apply.
  # Related Words: Provide related words or phrases for potential wordplay.
  # Unexpected Associations: Suggest opposites or surprising connections for contrast.
  
  # Example Format: For “cat,” you might suggest famous cats (Garfield), places (veterinary clinics), clichés (nine lives), objects (scratching post), or unexpected associations (cats and cucumbers).
  
  # , including well-known figures or stereotypes, locations tied to the keyword, common phrases or clichés, closely related items, recent events or trends, related words or phrases for wordplay, and unexpected or contrasting connections.
  # """
  
  sys_msg = """
  You are a joke-writing assistant. 
  Given a keyword, brainstorm related topics to inspire humor.
  Generate a list of relevant associations.

  Example: For “cat,” you might suggest famous cats (Garfield), veterinary clinics, clichés (nine lives), scratching posts, or unexpected associations (cats and cucumbers). 
  """
  req = f"keyword: {state['keyword']}"
  
  response = llm.invoke([
    SystemMessage(content=sys_msg),
    HumanMessage(content=req)
  ])
  
  retry = 3
  while retry != 0:
    try:
      keyword_association = llm.with_structured_output(Associations).invoke(response.content)

      if not keyword_association:
        raise ValueError("The Association object was not generated from the model.")
      break
    except Exception as e:
      retry -= 1
      logging.error(f"There was an error while parsing the Associations output (remaining retry: {retry})")
      logging.error(e)

  
  return {
    "keywords_associations": [keyword_association]
  }

def send_generate_associations(state) -> Literal['associations_generator']:
  return [Send('associations_generator', {'keyword': keyword}) for keyword in state.get('keywords')]
  
def human_pick_associations(state):
  """Human action node. Wait for human to pick two associations"""
  pass

def joke_creator(state):
  sys_msg = """
  You are a joke-writing assistant. Your task is to create a funny joke using two keywords and their given associations. Follow these steps:

  Understand the Keywords and Associations: Consider each keyword and its association, focusing on any traits, quirks, or clichés they suggest.

  Find a Humorous Connection: Look for an unexpected or clever link between the two concepts, using contrast or wordplay to add humor.

  Write a Concise Joke: Create a joke in one or two sentences, using the keywords and their associations for a clear setup and punchline.

  Example:

  Keyword: "Yoga" Association: [flexibility]
  Keyword: "Wi-Fi" Associatiot: [connection strength]
  Joke: “Why did the yoga instructor break up with their Wi-Fi? Because it just couldn’t hold a strong connection!”
  Use this format to make a joke for the keywords and associations provided.
  """

  req = ""
  for association in state['picked_associations']:
    req += f"Keyword: {association.keyword} Association: {association.associations}\n"
    
  jokes = llm.invoke([
    SystemMessage(sys_msg),
    HumanMessage(req)
  ])
  
  return {
    "jokes": jokes
  }

# %%
# Compile Graph
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

builder = StateGraph(State)
builder.add_node(associations_generator)
builder.add_node(human_pick_associations)
builder.add_node(joke_creator)

builder.add_conditional_edges(START, send_generate_associations)
builder.add_edge('associations_generator', 'human_pick_associations')
builder.add_edge('human_pick_associations', 'joke_creator')
builder.add_edge('joke_creator', END)

memory = MemorySaver()
agent = builder.compile(checkpointer=memory, interrupt_after=['human_pick_associations'])

def main():
   # %%
  # Draw Graph
  from IPython.display import display, Image

  display(Image(agent.get_graph().draw_mermaid_png()))

  # %%
  # TEST

  test_state = {
    'keywords': ["baby oil", 'patriarch']
  }
  config = {'configurable': {'thread_id': 1}}
  response = agent.invoke(test_state, config)

  picked_test = [
    Associations(keyword="baby oil", associations=["Slick' as a term for someone trying to be smooth or charming"]),
    Associations(keyword="phone", associations=["Steve Jobs (co-founder of Apple and iPhone developer)"])
  ]

  new_state = {
    'picked_associations': picked_test
  }

  agent.update_state(config=config, values=new_state)

  response = agent.invoke(None, config)

  print(response)

if __name__ == "__main__":
  main()
 