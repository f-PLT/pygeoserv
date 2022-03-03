import requests

from pygeoserv.geoserver import Geoserver
from pygeoserv.utils import bool2string, is_response_ok


class Workspace:
    def __init__(self, geoserver: Geoserver, workspace_name: str, isolated: bool = False) -> None:
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
        self.isolated = bool2string(isolated)
        if not self._does_workspace_exist():
            self.create_workspace()

    def _does_workspace_exist(self):
        """
        Checks if the workspace exists on the Geoserver server

        :returns: Returns true if workspace exists
        """

        response = requests.get(
            url=self.url,
            auth=self.geoserver.auth,
            headers=self.geoserver.headers,
        )
        return is_response_ok(response)

    def info(self) -> dict:
        """
        Fetch information about the workspace

        :returns: Returns workspace information in Json format
        """

        response = requests.get(
            url=self.url,
            auth=self.geoserver.auth,
            headers=self.geoserver.headers,
        )
        response.raise_for_status()
        return response.json()

    def create_workspace(self) -> requests.Response:
        """
        Create a workspace on Geoserver server

        :return: Response Object
        """
        request_url = f"{self.geoserver.url}/workspaces/"
        isolate = self.isolated
        payload = {"workspace": {"name": self.name, "isolated": isolate}}

        response = requests.post(
            url=request_url,
            json=payload,
            auth=self.geoserver.auth,
            headers=self.geoserver.headers,
        )
        response.raise_for_status()
        return response

    def remove_workspace(self) -> requests.Response:
        """
        Remove the workspace from the Geoserver server

        :return: Response object
        """
        request_url = f"{self.url}?recurse=true"
        response = requests.delete(
            url=request_url, auth=self.geoserver.auth, headers=self.geoserver.headers
        )
        response.raise_for_status()
        return response
