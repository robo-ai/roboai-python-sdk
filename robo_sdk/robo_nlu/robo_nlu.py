
from robo_sdk.robo_nlu.resources.nlu_resources import NLUResources
from robo_sdk.robo_nlu.model.config import Config


class RoboNLU:
    """
    Entry point class for NLU SDK. Allows to configure the NLU Service client on intialization.
    """
    __config=None

    def __init__(self, 
                 base_endpoint:str = "http://127.0.0.1:8000", # could be removed later
                 username:str = "user", 
                 password:str = "bestpassword"):
        self.__config=Config(base_endpoint = base_endpoint, 
                             http_auth={"username": username,
                                        "password": password})
              
    def model(self, model_uuid: str = None):
        """
        Instantiates a local model instance. If no uuid is passed as argument, the instance is void and ready to 
        create a nem model instance within configured the NLU Service API.
                   
        arguments: - model_uuid: str, existing model_uuid string. To be used when access to existing model is required.

        returns:   - a NLUResources() instantiated object.
        """
        if model_uuid:
            return NLUResources(config = self.__config, model_uuid=model_uuid)
        else:
            return NLUResources(config = self.__config)
