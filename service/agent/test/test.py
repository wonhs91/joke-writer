# %%
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from association_agent import agent as association_agent
from joke_agent import agent as joke_agent
from state import JokeMaterials

# %% Association Agent Test

association_test_state = {
  'keywords': ['AI', 'Joke'],
}
config = {'configurable': {'thread_id': 1}}

association_response = association_agent.invoke(association_test_state, config=config)
association_response 


# %% Joke Agent Test

joke_test_state = {
  'joke_material': JokeMaterials(materials={'AI': 'Robot overlords', 'Joke': 'Timing and delivery'}),
}

joke_response = joke_agent.invoke(joke_test_state, config=config)
joke_response



# %%
