from enum import Enum
from typing import Optional, BinaryIO, Type, Union, Callable
from requests_toolbelt.multipart.encoder import MultipartEncoder, MultipartEncoderMonitor

import cattr
import requests

from robo_sdk.robo_ai.exception.api_error import ApiError
from robo_sdk.robo_ai.exception.invalid_credentials_error import InvalidCredentialsError
from robo_sdk.robo_ai.exception.not_authorized_error import NotAuthorizedError
from robo_sdk.robo_ai.exception.not_found_error import NotFoundError
from robo_sdk.robo_ai.model.base_response import BaseResponse
from robo_sdk.robo_ai.model.config import Config
from robo_sdk.robo_ai.model.session import Session


class RequestMethod(Enum):
    POST = 'post'
    GET = 'get'
    PUT = 'put'
    DELETE = 'delete'


class ClientResource:
    """
    A client for communicating with the ROBO.AI server.

    Args:
        config (Config): a config object with the URL to the server, username and password.
        session (Session): a session object containing the access token.

    Attributes:
        __config (Config): Where config is stored.
        __session (Session): Where session is stored.
        resources (dict): a dictionary containing the object's resources.
    """

    __config: Config = None
    __session: Session = None
    __resources: dict = {}

    def __init__(self, config: Config, session: Session):
        self.__config = config
        self.__session = session
        self._register_resources()

    def get_config(self) -> Config:
        """
        Return the config attribute.

        Returns:
            Config: a config object with the URL to the server,
                username and password.
        """
        return self.__config

    def get_auth_headers(self) -> dict:
        """
        Return the authorization request header containing the bearer token.

        Returns:
            dict: a dictionary with the authorization request header
                containing the bearer token.
        """
        token = self.get_access_token()
        return {
            'Authorization': 'bearer %s' % token,
        } if token else {}

    def get_access_token(self) -> Optional[str]:
        """
        Return the access token.

        Returns:
            Optional[str]: the access token if the session exists. Otherwise,
                it returns None.
        """
        if self.__session:
            return self.__session.access_token
        return None

    def execute_request(self, method: RequestMethod, url: str, response_class: Type[BaseResponse] = None,
                        json_data: dict = None, data: Union[dict, BinaryIO] = None, files: dict = None,
                        params: dict = None, headers: dict = {}, auth_headers=True,
                        progress_callback: Callable[[MultipartEncoderMonitor], None] = None):
        """
        Execute request.

        Args:
            method (RequestMethod): type of request to be made.
            url (str): URL of the request.
            response_class (Type[BaseResponse], optional): type of response to be used in the request. Defaults to None.
            json_data (dict, optional): dictionary containing the request payload. Defaults to None.
            data (Union[dict, BinaryIO], optional): data to be sent in the request. Defaults to None.
            files (dict, optional): dictionary containing files data. Defaults to None.
            params (dict, optional): dictionary containing parameters data. Defaults to None.
            headers (dict, optional): dictionary containing headers data. Defaults to {}.
            auth_headers (bool, optional): bool indicating whether authentication headers are present or not.
                Defaults to True.
            progress_callback (Callable[[MultipartEncoderMonitor], None], optional): Callable object to
                enable a progress indicator. Defaults to None.

        Raises:
            InvalidCredentialsError: if the credentials are wrong.
            NotAuthorizedError: if the access to the resource is forbidden.
            NotFoundError: if the resource is not found.
            ApiError: if the server returns an error.

        Returns:
            if a response_class is passed and the request is successful,
                it returns an assistant, otherwise the contents of the response are returned.
                If the request is not successful, an Exception is raised.
        """

        config = self.get_config()
        full_url = config.base_endpoint + url

        if auth_headers:
            auth_headers = self.get_auth_headers()
            headers = {
                **headers,
                **auth_headers
            }

        data_fields = None
        if data:
            data_fields = MultipartEncoder(fields=data)
            headers['Content-Type'] = data_fields.content_type
            if progress_callback:
                data_fields = MultipartEncoderMonitor(data_fields, progress_callback)

        response = requests.request(method.value, full_url, headers=headers, params=params, data=data_fields,
                                    json=json_data, files=files)

        # all 2xx codes are considered success
        is_success = response.status_code // 100 == 2

        if is_success:
            if response_class:
                assistant = cattr.structure(response.json(), response_class)
                return assistant
            else:
                return response.content
        elif response.status_code == 401:
            raise InvalidCredentialsError()
        elif response.status_code == 403:
            raise NotAuthorizedError()
        elif response.status_code == 404:
            raise NotFoundError()
        else:
            raise ApiError()

    def _add_resource(self, name: str, resource_type: Type['ClientResource']):
        self.__resources[name] = resource_type(self.__config, self.__session)

    def _get_resource(self, name: str):
        return self.__resources[name]

    def _register_resources(self):
        pass
