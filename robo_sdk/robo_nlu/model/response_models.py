from typing import List, Dict, Optional, Union, Literal
from enum import Enum
from pydantic import BaseModel, Field 

class Status(str, Enum):
    NEW = "NEW"
    TO_TRAIN = "TO_TRAIN"
    READY = "READY"
    TRAINING = "TRAINING"
    FAILED = "FAILED"

class BaseResponse(BaseModel):
    timestamp: str


class CreateContent(BaseModel):
    model_uuid: str 
    job_status: Status 


class CreateResponse(BaseResponse):
    """
    Create response schema output by the /create endpoint
    """

    content: CreateContent

    class Config:
        """
        Example of the above schema.
        """

        schema_extra = {
                "example": {
                    "content": {
                        "model_id": "8715ced38b044279ab56e66ca04a0aac",
                        "job_status": "NEW",
                    },
                "timestamp": "Wed Dec 22 18:30:21 2021",
                }
            }


class TrainContent(BaseModel):

    job_status: Status 


class TrainResponse(BaseResponse):
    """
    Train response schema output by the train endpoint
    """

    content: TrainContent

    class Config:
        """
        Example of the above schema.
        """

        schema_extra = {
            "example": {
                "content": {
                    "job_status": "TO_TRAIN"
                    },
                "timestamp": "Wed Dec 22 18:30:21 2021",
                }
        }


class StatusContent(BaseModel):

    job_status: Status 


class StatusResponse(BaseResponse):
    """
    Status response schema output by the train endpoint
    """

    content: StatusContent

    class Config:
        """
        Example of the above schema.
        """

        schema_extra = {
            "example": {
                "content":{
                    "job_status": "TRAINING"
                },
                "timestamp": "Wed Dec 22 18:30:21 2020",
            }
        }

class ReportEntry(BaseModel):
    precision: float = Field(alias="precision")
    recall: float = Field(alias="recall")
    f1_score: float = Field(alias="f1-score")
    support: int = Field(alias="support")
    confused_with: Optional[Dict[str,int]]=Field(alias="f1-score")
    
    class Config:
        allow_population_by_field_name = True


class AverageEntry(BaseModel):
    precision: float = Field(alias="precision")
    recall: float = Field(alias="recall")
    f1_score: float = Field(alias="f1-score")
    support: int = Field(alias="support")
    
    class Config:
        allow_population_by_field_name = True

class AccuracyEntry(BaseModel):
    accuracy: float 


class ConfusionListEntry(BaseModel):
    intent: str
    confused_with: str
    count: int


class MetricsContent(BaseModel):
    report: Dict[str, Union[ReportEntry, float, AverageEntry]] # Union[Dict[str, ReportEntry], AccuracyEntry, Dict[Literal["micro avg", "macro avg", "weighted avg"], AverageEntry]]#
    confusion_list: List[ConfusionListEntry]
    confusion_matrix: Dict[str,Dict[str,int]]
    

class MetricsResponse(BaseResponse):
    content: MetricsContent

    class Config:
        """
        Example of the above schema.
        """

        schema_extra = {
            "example": {
                "content": {
                    "report": {
                        "Bye": {
                            "precision": 0.4,
                            "recall": 0.5,
                            "f1-score": 0.4444444444444445,
                            "support": 4
                        },
                        "Greeting": {
                            "precision": 0.5,
                            "recall": 0.4,
                            "f1-score": 0.4444444444444445,
                            "support": 5
                        },
                        "accuracy": 0.4444444444444444,
                        "macro avg": {
                            "precision": 0.45,
                            "recall": 0.45,
                            "f1-score": 0.4444444444444445,
                            "support": 9
                        },
                        "weighted avg": {
                            "precision": 0.4555555555555555,
                            "recall": 0.4444444444444444,
                            "f1-score": 0.4444444444444444,
                            "support": 9
                        }
                        },
                        "confusion_list": [
                        {
                            "intent": "Greeting",
                            "confused_with": "Bye",
                            "count": 3
                        },
                        {
                            "intent": "Bye",
                            "confused_with": "Greeting",
                            "count": 2
                        }
                        ],
                        "confusion_matrix": {
                        "Bye": {
                            "Bye": 2,
                            "Greeting": 2
                        },
                        "Greeting": {
                            "Bye": 3,
                            "Greeting": 2
                        }
                        }
                    },
                "timestamp": "03/11/2022, 14:35:32"
            }
        }

class IntentResponseBody(BaseModel):
    
    name: str
    confidence: float

class EntityResponseBody(BaseModel):
    
    entity: str
    start: int
    end: int
    value: str

class PredictContent(BaseModel):
        
    intents: List[IntentResponseBody]
    entities: List[EntityResponseBody] = None
    

class PredictResponse(BaseResponse):
    """
    Predict response schema output bt thr predict endpoint
    """

    content: PredictContent


class DeleteContent(BaseModel):
    model_uuid: str

class DeleteResponse(BaseResponse):
    content: DeleteContent