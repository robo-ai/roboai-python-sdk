from pydantic import BaseModel
from typing import List, Optional, Pattern, Union

# Train endpoint schema

class IntentEntry(BaseModel):
    intent: str
    examples: List[str]

class LookupEntry(BaseModel):
    lookup: str
    examples: List[str]

class RegexEntry(BaseModel):
    regex: str
    examples: List[Pattern]

class TrainBody(BaseModel):
    """
    TrainBody schema sent in the train POST request.
    """
    nlu: List[Union[IntentEntry, Optional[LookupEntry], Optional[RegexEntry]]]
