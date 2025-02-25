# %%
from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.constants import Send
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
import logging

from agent.llm_model import llm
from agent.state import OverallState, KeysAssociations

def associations_generator(state):
  
  # 1. Get Associations from LLM
  sys_msg = """
  You are a joke-writing assistant.
  Given a keyword, brainstorm related topics to inspire humor.
  Start the response with "Keyword: "KEYWORD: [USER_GIVEN_KEYWORD]" where [USER_GIVEN_KEYWORD] is the input keyword, followed by a list of associations.

  Example:
  For the keyword “cat” the response should be:
  ```
  keyword: cat
  
  - cats playing the piano 
  - cat owners dressing their pets 
  - feline hairballs 
  - catnip obsession 
  - cat cafes 
  ```
  
  Only list associations without any headers.
  """
  req = f"keyword: {state['keyword']}"
  
  response = llm.invoke([
    SystemMessage(content=sys_msg),
    HumanMessage(content=req)
  ])
  
  # 2. Create KeysAssociations object from the LLM response
  retry = 3
  while retry != 0:
    try:
      keyword_associations = llm.with_structured_output(KeysAssociations).invoke(response.content) # response.content

      if not keyword_associations:
        raise ValueError(f"There was an error parsing llm output to KeysAssociations class for '{state['keyword']}'. Most likely because the llm.with_structured_output outputted 'None'.")
      break
    except Exception as e:
      retry -= 1
      logging.error(f"Error with '{state['keyword']}' (remaining retry: {retry})\n{e}")

  return {
    "keywords_associations": keyword_associations
  }

def send_generate_associations(state) -> Literal['associations_generator']:
  return [Send('associations_generator', {'keyword': keyword}) for keyword in state.get('keywords')]


builder = StateGraph(OverallState)
builder.add_node(associations_generator)

builder.add_conditional_edges(START, send_generate_associations)
builder.add_edge('associations_generator', END)

memory = MemorySaver()
agent = builder.compile()


# %%
def main():

  # Draw Graph
  from IPython.display import display, Image
  display(Image(agent.get_graph().draw_mermaid_png()))
  
  test_state = {'keywords': ["baby oil", 'patriarch']}
  config = {'configurable': {'thread_id': 1}}
  
  # Run agent
  response = agent.invoke(test_state, config)
  print(response)
  

if __name__ == "__main__":
  main()
 