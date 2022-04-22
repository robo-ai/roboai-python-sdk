from robo_sdk.robo_nlu.model.response_models import TrainResponse
from robo_sdk.robo_nlu.resources.nlu_client import NLUClient, RequestMethod
from robo_sdk.robo_nlu.model.response_models import CreateResponse, TrainResponse, StatusResponse, MetricsResponse, PredictResponse, DeleteResponse, DeleteContent
from robo_sdk.robo_nlu.utils.utils import load_yaml_to_json

from typing import Union
from datetime import datetime

class NLUResources(NLUClient):
    """
    NLUResources class: Abstraction class to API interaction. Provides a method for each API endpoint. 
                        More detail within each method description.

                        Each object need to be initialized with a config object instance (see NLUClient superclass).
                        Optionally the object can be initialized with a model_uuid. This presuposes that a model instance
                        exists within the API service and therefor a model creation is not allowed.

                        Note: all methods that request a API endpoint return the API response on an enriched object based on 
                              pydantic models, for ease of response parsing. This allows for a number of utility methods to 
                              be accessible within each returned object. For more information on the available methods, please
                              refer to https://pydantic-docs.helpmanual.io/usage/models/.
    """

    def __init__(self, config, model_uuid: str=None):
        """
            Initialization method for NLUResources class.
            
            arguments: - config: Config() instance, holding basic auth parameters. See Config class.
                       - model_uuid: str, existing model_uuid string. To be used when access to existing model is required.

            returns:   - a NLUResources() instantiated object.
        """

        super().__init__(config)
        self.__model_uuid = model_uuid


    def create(self, language: str):
        """
        Method to create a model object within the NLU API service.
        Note that if the object's model_uuid attribute is not None, this method is not effective, and returns None.

        arguments: - language: str, a 2 char code for the language that characterizes the model.

        returns:   - CreateResponse() object (based upon a pydantic BaseModel).
                or
                   - None,  if object's model_uuid is not None.
        """
        
        if self.__model_uuid:
             print("Cannot create a new model given that a model uuid was provided")
        else:
            create_url= f"/create/{language}"
            response= self._execute_request(method=RequestMethod.POST, url=create_url)     
            self.__model_uuid= response.json()["content"]["model_uuid"]     
            return CreateResponse(**response.json())
           
     
    def train(self, json_data: Union[dict,str], model_eval: bool=False , max_allowed_error_number: int=3, min_word_length: int=3):
        """
        Method to train a model object within the NLU API service. The data used to train the model can be a memory loaded dict object with 
        the same format as expected by the API:
        
        data example: 
            {
                "nlu": [
                    {"intent": "Greeting", "examples": ["Hi","Hello","Howdy","Bonjour","Ça va bien?"]},
                    {"intent": "Bye", "examples": ["Good bye","Bye bye", "Au revoir","C U"]},
                    {"lookup": "Language", "examples":["PT","ENG"]},
                    {"regex": "door_number", "examples":["(\W|^)po[#\-]{0,1}\s{0,1}\d{2}[\s-]{0,1}\d{4}(\W|$)"]}

                    ]
            }

        or, if a string path reference is passed to a RASA v3 yaml file, the data is loaded into memory from the file. 

        arguments: - json_data: dict, holding the training data in the required format, see example above.
                                or
                                str, a string reference path to a yaml Rasa v3 file, holding the training data.

                   - model_eval: bool (optional), a Boolean flag to preform the model evaluation tasks before training the data.
                                 Optional as defaults to False.

                   - max_allowed_error_number: int (optional), an integer number that controls the number of allowed errors in the lookup 
                                               entity extraction, allowing for fuzzy matching of strings.

                   - min_word_length: int (optional), an integer number that controls the minimum word length above witch fuzz matching is
                                      allowed.
        
        note: For a more comprehensive understanding of NER fuzzy matching, please refer to the NLU API swagger documentation

        returns:   - TrainResponse() object (based upon a pydantic BaseModel).
        """
        if type(json_data) == str:
            json_data = load_yaml_to_json(json_data)        
        train_url= f"/train/{self.__model_uuid}"
        params={"model_eval": model_eval,"max_allowed_error_number":max_allowed_error_number,"min_word_length":min_word_length}
        response = self._execute_request(method=RequestMethod.POST,url=train_url,params=params,json_data=json_data)
        return TrainResponse(**response.json())

    def status(self):
        """
        Method to retrieve the status of model object within the NLU API service. 
        
        arguments: None

        returns:   - StatusResponse() object (based upon a pydantic BaseModel).
        """

        status_url = f"/status/{self.__model_uuid}"
        response =  self._execute_request(method=RequestMethod.GET, url=status_url)
        return StatusResponse(**response.json())
    
    def metrics(self):
        """
        Method to retrieve the status of model object within the NLU API service. 
        
        arguments: No arguments are required.

        returns:   - MetricsResponse() object (based upon a pydantic BaseModel).
        """
        metrics_url = f"/metrics/{self.__model_uuid}"
        response =  self.execute_request(method=RequestMethod.GET, url=metrics_url)
        return MetricsResponse(**response.json())

    def predict(self, json_data:dict):
        """
        Method to, given a text, retrieve the prediction of model object within the NLU API service.
        
        arguments: - json_data: dict, a dictionary holding a text string as value identified by the "text" key. 
                     data example {"text":"Hello and goodbye"}

        returns:   - PredictResponse() object (based upon a pydantic BaseModel).
        """
        predict_url = f"/predict/{self.__model_uuid}"
        response =  self._execute_request(method=RequestMethod.POST, url=predict_url, json_data=json_data)
        return PredictResponse(**response.json())

    def delete(self):
        """
        Method to delete an existing model object within the NLU API service.
        
        arguments: No arguments are required.

        returns:   - DeleteResponse() object (based upon a pydantic BaseModel).
        """
        delete_url = f"/delete/{self.__model_uuid}"
        response = self._execute_request(method=RequestMethod.DELETE, url=delete_url)
        return DeleteResponse(content = DeleteContent(
           model_uuid = self.__model_uuid
       ), 
       timestamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
       )


    @property
    def get_model(self):
        """
        Property to get the NLU model UUID.
        
        arguments: No arguments are required.

        returns: model_uuid: str, the string holding the NLU model UUID.
        """
        return self.__model_uuid
    

        