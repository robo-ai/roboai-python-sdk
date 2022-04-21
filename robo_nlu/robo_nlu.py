
from robo_nlu.resources.nlu_resources import NLUResources
from robo_nlu.model.config import Config


class RoboNLU:
    """
    Entry point class for NLU SDK. Allow to configure  
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
        bla bla bla
        """
        if model_uuid:
            return NLUResources(config = self.__config, model_uuid=model_uuid)
        else:
            return NLUResources(config = self.__config)
