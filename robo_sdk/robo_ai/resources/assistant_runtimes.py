import os
from typing import Callable

from robo_sdk.robo_ai.model.assistant_runtime.assistant_runtime_logs_response import AssistantRuntimeLogsResponse
from robo_sdk.robo_ai.model.assistant_runtime.assistant_runtime_response import AssistantRuntimeResponse
from robo_sdk.robo_ai.resources.client_resource import ClientResource, RequestMethod


class AssistantRuntimesResource(ClientResource):
    """
    This class implements operations to manage bot runtimes.
    """

    def create(
        self,
        assistant_uuid: str,
        package_file_path: str,
        base_runtime: str,
        progress_callback: Callable[[int], None] = None,
    ):
        """
        Create a new bot runtime given a file package.

        Args:
            assistant_uuid (str): Unique identifier of the assistant into where the bot will be set.
            package_file_path (str): Filesystem path to the bot runtime package.
            base_runtime (str): Reference to the framework base and version where the bot was built in order
                to establish the correct environment in the server.
            progress_callback (Callable[[int], None], optional): Callable object to enable a progress indicator
                in the command line. Defaults to None.

        Returns:
            AssistantRuntimeResponse: see [robo_ai.model.assistant_runtime.assistant_runtime_response]
        """

        return self.__deploy(RequestMethod.POST, assistant_uuid, package_file_path, base_runtime, progress_callback)

    def update(
        self,
        assistant_uuid: str,
        package_file_path: str,
        base_runtime: str,
        progress_callback: Callable[[int], None] = None,
    ):
        """
        Update an existing bot runtime using a new file package.

        Args:
            assistant_uuid (str): Unique identifier of the assistent runtime into where the bot lives.
            package_file_path (str): Filesystem path to the bot runtime file package.
            base_runtime (str): Reference to the framework base and version where the bot was built,
                in order to establish the correct environment in the server.
            progress_callback (Callable[[int], None], optional): Callable object to enable a progress indicator
                in the command line. Defaults to None.

        Returns:
            AssistantRuntimeResponse: see [robo_ai.model.assistant_runtime.assistant_runtime_response]
        """
        return self.__deploy(RequestMethod.PUT, assistant_uuid, package_file_path, base_runtime, progress_callback)

    def stop(self, assistant_uuid: str):
        """
        Stop a bot runtime that is running.
        Args:
            assistant_uuid (str): Unique identifier of the assistant runtime where the bot lives.

        Returns:
            AssistantRuntimeResponse: see [robo_ai.model.assistant_runtime.assistant_runtime_response]
        """
        url = self.__get_runtime_url(assistant_uuid) + "/stop"
        response = self.execute_request(RequestMethod.POST, url, response_class=AssistantRuntimeResponse)
        return response

    def start(self, assistant_uuid: str):
        """
        Start a bot runtime that is stopped.

        Args:
            assistant_uuid (str): Unique identifier of the assistant runtime where the bot lives.

        Returns:
            AssistantRuntimeResponse: see [robo_ai.model.assistant_runtime.assistant_runtime_response]
        """
        url = self.__get_runtime_url(assistant_uuid) + "/start"
        response = self.execute_request(RequestMethod.POST, url, response_class=AssistantRuntimeResponse)
        return response

    def remove(self, assistant_uuid: str):
        """
        Remove a bot runtime.

        Args:
            assistant_uuid (str): Unique identifier of the assistant runtime where the bot lives.
        """
        url = self.__get_runtime_url(assistant_uuid)
        self.execute_request(RequestMethod.DELETE, url)

    def get(self, assistant_uuid: str) -> AssistantRuntimeResponse:
        """
        Fetch information from a given bot runtime.

        Args:
            assistant_uuid (str): Unique identifier of the assistant runtime where the bot lives.

        Returns:
            AssistantRuntimeResponse: see [robo_ai.model.assistant_runtime.assistant_runtime_response]
        """
        url = self.__get_runtime_url(assistant_uuid)
        response = self.execute_request(RequestMethod.GET, url, response_class=AssistantRuntimeResponse)
        return response

    def get_logs(self, assistant_uuid: str) -> AssistantRuntimeLogsResponse:
        """
        Fetch the most recent logs from a given runtime.

        Args:
            assistant_uuid (str): Unique identifier of the assistant runtime where the bot lives.

        Returns:
            AssistantRuntimeLogsResponse: see
                [robo_ai.model.assistant_runtime.assistant_runtime_logs.AssistantRuntimeLogsResponse()]
        """
        url = self.__get_runtime_url(assistant_uuid) + "/logs"
        response = self.execute_request(RequestMethod.GET, url, response_class=AssistantRuntimeLogsResponse)
        return response

    def __deploy(
        self,
        method: RequestMethod,
        assistant_uuid: str,
        package_file_path: str,
        base_runtime: str,
        progress_callback: Callable[[int], None] = None,
    ):
        """
        Deploy a given bot.

        Args:
            method (RequestMethod): Method of the request to be executed.
            assistant_uuid (str): Unique identifier of the assistant runtime where the bot lives.
            package_file_path (str): Filesystem path to the bot runtime file package.
            base_runtime (str): Reference to the framework base and version where the bot was built,
                in order to establish the correct environment in the server.
            progress_callback (Callable[[int], None], optional): Callable object to enable a progress indicator
                in the command line. Defaults to None.

        Returns:
            AssistantRuntimeResponse: see [robo_ai.model.assistant_runtime.assistant_runtime_response]
        """
        url = self.__get_runtime_url(assistant_uuid)
        with open(package_file_path, "rb") as package_file:
            data = {
                "runtimeBase": base_runtime,
                "file": (os.path.basename(package_file_path), package_file, "application/zip"),
            }

            def progress_callback_wrapper(monitor):
                progress_callback(monitor.bytes_read)

            callback = None
            if progress_callback:
                callback = progress_callback_wrapper

            response = self.execute_request(
                method, url, data=data, response_class=AssistantRuntimeResponse, progress_callback=callback
            )
            return response

    @staticmethod
    def __get_runtime_url(assistant_uuid: str):
        return "/api/assistants/{0}/runtime".format(assistant_uuid)
