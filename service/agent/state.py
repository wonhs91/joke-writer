from typing import Dict, List, Annotated
from typing_extensions import TypedDict
from pydantic import BaseModel, Field, field_validator
import json
import ast

class JokeMaterials(BaseModel):
  materials: Dict[str, str] = Field(default_factory=dict,
                                    description="key is the keyword, and value is the associated material")
  
class KeysAssociations(BaseModel):
  """Please use this Model to store the keyword and the associations"""
  keys_associations: Dict[str, List[str]] = Field(
    description="Return a dictionary where the key is the keyword or a key phrase, and the value is a list of associations, excluding headers.",
    default_factory={}
    )
  
  @field_validator('keys_associations', mode="before")
  def check_associations(cls, value):
    try:
      if isinstance(value, str):
        value = ast.literal_eval(value)
      elif isinstance(value, dict) and any(isinstance(v, str) for v in value.values()):
        value = {k: ast.literal_eval(v) if isinstance(v, str) else v for k, v in value.items()}
    except Exception as e:
      raise ValueError("association is not a dict, nor a string of dict")
    
    return value
  
  class Config:
    json_schema_extra  = {
      "example": {
        "keys_associations": {
          "baby oil": ["'Oil slick' comments (comparing someone's skin to being too shiny or greasy)"
                       "'Slick' as a term for someone trying to be smooth or charming",
                       "Tanning beds", "Smooth", "sleek",
                       "Baby oil in cooking or baking (a humorous twist on using it for skin care)"]
        }
      },
      "example 2": {
        "keys_associations": {
          "phone": ["Steve Jobs (co-founder of Apple and iPhone developer)",
                    "Meeting rooms with conference phones",
                    "'Hang up on someone' (to end a conversation abruptly)",
                    "Social media obsession",
                    "reach out", "get in touch", "call back", 
                    "Using a phone in a place with no signal (e.g., wilderness or a bunker)"]
        }
      }
    }

def update_keysassociations(orig_associations: KeysAssociations, new_associations: KeysAssociations):
  orig_associations.keys_associations.update(new_associations.keys_associations)
  return orig_associations

class OverallState(TypedDict):
  keywords: list[str]
  keywords_associations: Annotated[KeysAssociations, update_keysassociations]
  joke_material: JokeMaterials
  joke: str
