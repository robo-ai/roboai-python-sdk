from robo_ai.model.assistant.assistant_list_response import AssistantListResponse
from robo_ai.model.assistant.assistant_response import AssistantResponse
from robo_ai.resources.assistant_runtimes import AssistantRuntimesResource
from robo_ai.resources.client_resource import ClientResource, RequestMethod


class AssistantsResource(ClientResource):
    """
    This class implements operations to manage and retrieve bots.
    """

    def _register_resources(self):
        self._add_resource('runtimes', AssistantRuntimesResource)

    def get_list(self, page=1) -> AssistantListResponse:
        """
        Return a paged list of all bots available.

        Args:
            page (int, optional): Indicates the page being requested. Defaults to 1.

        Returns:
            AssistantListResponse: see [robo_ai.model.assistant.assistant_list_response.AssistantListResponse]
        """
        params = {'page': page}
        url = '/api/assistants'
        return self.execute_request(RequestMethod.GET, url, params=params, response_class=AssistantListResponse)

    def get_assistant(self, uuid: str) -> AssistantResponse:
        """
        Return an assistant according to a given uuid.

        Args:
            uuid (str): Unique identifier of the assistant.

        Returns:
            AssistantResponse: see [robo_ai.model.assistant.assistant_response.AssistantResponse]
        """
        url = '/api/assistants/uuid/' + uuid
        return self.execute_request(RequestMethod.GET, url, response_class=AssistantResponse)

    @property
    def runtimes(self) -> AssistantRuntimesResource:
        """
        Return the assistant's runtimes.

        Returns:
            AssistantRuntimesResource: see [robo_ai.resources.assistant_runtimes.AssistantRuntimesResource]
                which allows all handling of the remote runtime by the client.
        """
        return self._get_resource('runtimes')
