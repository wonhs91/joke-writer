# %%
from llm_model import llm
from langgraph.graph import StateGraph, START, END
from operator import add
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

class State(TypedDict):
  start: str
  agent1_state: Annotated[list[str], add] = []
  agent2_state: Annotated[list[str], add] = []


# %%
  
def agent1_start(state):
  return {
    'agent1_state': ["This is Start of Agent 1"]
  }

def agent1_process(state):
  
  return {
    'agent1_state': ["Agent 1 processed"]
  }

def agent1_end(state):
  return {
    'agent1_state': ["Agent 1 Ended"]
  }

builder = StateGraph(State)
builder.add_node(agent1_start)
builder.add_node(agent1_process)
builder.add_node(agent1_end)

builder.add_edge(START, 'agent1_start')
builder.add_edge('agent1_start', 'agent1_process')
builder.add_edge('agent1_process', 'agent1_end')
builder.add_edge('agent1_end', END)

memory = MemorySaver()
agent1 = builder.compile(memory)

from IPython.display import display, Image
display(Image(agent1.get_graph().draw_mermaid_png()))

# %%
def agent2_start(state):
  return {
    'agent2_state': ["This is Start of Agent 2"]
  }

def agent2_process(state):
  return {
    'agent2_state': ["Agent 2 processed"]
  }

def agent2_end(state):
  return {
    'agent2_state': ["Agent 2 Ended"]
  }

builder2 = StateGraph(State)
builder2.add_node(agent2_start)
builder2.add_node(agent2_process)
builder2.add_node(agent2_end)

builder2.add_edge(START, 'agent2_start')
builder2.add_edge('agent2_start', 'agent2_process')
builder2.add_edge('agent2_process', 'agent2_end')
builder2.add_edge('agent2_end', END)

agent2 = builder2.compile(memory)
display(Image(agent2.get_graph().draw_mermaid_png()))



# %%
config = {'configurable': {'thread_id': 1}}
agent1_output = agent1.invoke({'start': ['GO! Agent 1!']}, config=config)
# %%
agent2_output = agent2.invoke({'start': ['GO! Agent 2!']}, config=config)
# %%
agent1_output, agent2_output
# %%
for snapshot in list(agent2.get_state_history(config)):
  print(snapshot.values)
# %%
