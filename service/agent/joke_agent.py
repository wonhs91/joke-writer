# %%  Agent Building
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agent.llm_model import llm
from agent.state import OverallState

def joke_creator(state: OverallState):
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
  for keyword in state['joke_material'].materials.keys():
    req += f"Keyword: {keyword} Association: {state['joke_material'].materials[keyword]}\n"
    
  joke = llm.invoke([
    SystemMessage(sys_msg),
    HumanMessage(req)
  ]).content
  
  return {
    "joke": joke
  }

builder = StateGraph(OverallState)
builder.add_node(joke_creator)

builder.add_edge(START, 'joke_creator')
builder.add_edge('joke_creator', END)

memory = MemorySaver()
agent = builder.compile()


# %% Python Run Test

from agent.state import JokeMaterials

def main():
  # Draw Graph
  from IPython.display import display, Image
  display(Image(agent.get_graph().draw_mermaid_png()))
  
  materials = {
    "baby oil": "Diaper rash",
    "patriarch": "grumpy old men"
  }
  
  test_state = {
    'joke_material': JokeMaterials(materials=materials)
  }
  
  config = {'configurable': {'thread_id': 1}}
  
  response = agent.invoke(test_state, config=config)
  print(response)
  

if __name__ == "__main__":
  main()

