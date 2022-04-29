from robo_sdk.robo_ai.model.session import Session
from robo_sdk.robo_ai.model.config import Config
from robo_sdk.robo_ai.resources.assistants import AssistantsResource
from robo_sdk.robo_ai.resources.base_resource import BaseResource
from robo_sdk.robo_ai.resources.oauth import OauthResource


class RoboAi:
    """
    Class used to represent a RoboAi client.
    It allows ROBO-AI resources to be managed.

    Args:
        config (Config): a config object with the URL to the server, username and password.

    Attributes:
        __config (Config): Where config is stored.
        __current_session (Session): Where information regarding the session is stored.
        __base_resource (BaseResource): where __config and __current_session information is stored.
    """

    __config: Config = None
    __base_resource: BaseResource = None
    __current_session = Session()

    def __init__(self, config: Config):
        self.__config = config
        self.__base_resource = BaseResource(self.__config, self.__current_session)

    def set_config(self, config: Config):
        """
        Overwrite the object's __config attribute.

        Args:
            config (Config): a config object with the URL to the server, username and password.
        """
        self.__config = config

    def set_session_token(self, access_token: str):
        """
        Overwrite the object's __current_session attribute

        Args:
            access_token (str): a string containing the access token.
        """
        self.__current_session.access_token = access_token

    @property
    def oauth(self) -> OauthResource:
        """
        Return a resource that allows managing the authentication session.

        Returns:
            OauthResource: object containing authentication information.
        """
        return self.__base_resource.oauth

    @property
    def assistants(self) -> AssistantsResource:
        """
        return a resource that allows managing the bot information and bot runtimes.

        Returns:
            AssistantsResource: object containing assistants information.
        """
        return self.__base_resource.assistants
