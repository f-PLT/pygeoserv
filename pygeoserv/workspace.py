from requests import Response

from pygeoserv.geoserver import Geoserver
from pygeoserv.geoserver_requests.workspace import (
    create_workspace_request,
    remove_workspace_request,
    workspace_datastore_info_request,
    workspace_info_request,
)
from pygeoserv.utils import is_response_ok


class Workspace:
    """
    Class that represents a Geoserver workspace
    """

    def __init__(
        self,
        geoserver: Geoserver,
        workspace_name: str,
        is_isolated: bool = False,
    ) -> None:
        """
        A Geoserver Workspace.

        If the workspace does not exist, it will be created automatically.

        :param geoserver: Geoserver instance
        :param workspace_name: Name of the workspace
        :param isolated: Is the workspace isolated (only important if creating
               a workspace that doesn't already exist on the server)
        """

        self.geoserver = geoserver
        self.name = workspace_name
        self.url = f"{geoserver.url}/workspaces/{self.name}"
        self.is_isolated = is_isolated
        if not self.does_workspace_exist():
            self.create_workspace()

    def does_workspace_exist(self):
        """
        Checks if the workspace exists on the Geoserver server

        :returns: Returns true if workspace exists
        """

        response = workspace_info_request(
            url=self.geoserver.url, auth=self.geoserver.auth, name=self.name
        )
        return is_response_ok(response)

    def info(self) -> dict:
        """
        Fetch information about the workspace

        :returns: Returns workspace information in Json format
        """

        response = workspace_info_request(
            url=self.geoserver.url, auth=self.geoserver.auth, name=self.name
        )
        response.raise_for_status()
        return response.json()

    def datastores_info(self):
        """
        Fetch information about the workspace

        :returns: Returns workspace information in Json format
        """

        response = workspace_datastore_info_request(
            url=self.geoserver.url, auth=self.geoserver.auth, name=self.name
        )
        response.raise_for_status()
        return response.json()

    def create_workspace(self) -> Response:
        """
        Create a workspace on Geoserver server

        :return: Response Object
        """
        response = create_workspace_request(
            url=self.geoserver.url,
            auth=self.geoserver.auth,
            name=self.name,
            is_isolated=self.is_isolated,
        )
        response.raise_for_status()
        return response

    def remove_workspace(self) -> Response:
        """
        Remove the workspace from the Geoserver server

        :return: Response object
        """
        response = remove_workspace_request(
            url=self.geoserver.url,
            auth=self.geoserver.auth,
            name=self.name,
        )
        response.raise_for_status()
        return response


def create_workspace(
    geoserver: Geoserver, workspace_name: str, is_isolated: bool = False
) -> Workspace:
    """
    Creates a workspace object. If the workspace does not exist on the
    server, it will be created

    :param geoserver: Geoserver instance
    :param workspace_name: Name of the workspace
    :param isolated: Is the workspace isolated (only important if creating
            a workspace that doesn't already exist on the server)
    """
    workspace = Workspace(
        geoserver=geoserver, workspace_name=workspace_name, is_isolated=is_isolated
    )
    if not workspace.does_workspace_exist():
        workspace.create_workspace()
    return workspace
