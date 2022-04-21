from enum import Enum
from typing import Optional, BinaryIO, Type, Union, Callable
from pydantic import BaseModel

import requests
from requests.auth import HTTPBasicAuth
from robo_nlu.model.config import Config

from robo_nlu.exception.not_found_error import NotFoundError
from robo_nlu.exception.not_authorized_error import NotAuthorizedError 
from robo_nlu.exception.not_acceptable_error import NotAcceptableError
from robo_nlu.exception.unprocessable_entity_error import UnprocessableEntityError

class RequestMethod(Enum):
    POST = 'post'
    GET = 'get'
    PUT = 'put'
    DELETE = 'delete'

class NLUClient:
    """
    NLU Client class: Superclass to NLU resources class (and other possible classes) which 
                      defines the base for requests to the NLU Service API

                      Needs to be initialized with a config instance, holding the authentication parameters.
    """

    __config: Config = None 

    def __init__(self, config: Config):
        self.__config=config

    def _get_config(self):
        return self.__config
    
    def _execute_request(self, method: RequestMethod, url: str, params: dict=None, json_data: dict = None, response_model:Type[BaseModel]=None):
        config = self._get_config()
        full_url = config.base_endpoint + url 

        response  = requests.request(method=method.value, url=full_url, params=params,json=json_data, auth=HTTPBasicAuth(config.http_auth_username,config.http_auth_password))

        is_success =  response.status_code // 100 ==2 
        if is_success:
            return response
        
        elif response.status_code==401:
            raise NotAuthorizedError(response.json()["detail"])

        elif response.status_code==404:
            raise NotFoundError(response.json()["detail"])
        
        elif response.status_code==406:
            raise NotAcceptableError(response.json()["detail"])

        elif response.status_code==422:
            raise UnprocessableEntityError(response.json()["detail"])
        
        else:
            raise Exception 