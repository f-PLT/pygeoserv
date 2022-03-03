"""
Main pygeoserv module
"""
from email import header
import requests


class Geoserver:
    """Geoserver class"""

    def __init__(self, url: str, auth: tuple) -> None:
        """
        Create a connection to Geoserver server

        :param url: Base url of Geoserver instance
        :param auth: Credentials tuple ("username", "password")
        """
        self.server_url = url
        self.url = (
            f"{self.server_url}/rest"
            if not self.server_url.endswith("/")
            else f"{self.server_url}rest"
        )
        self.auth = auth
        self.headers = {"Content-type": "application/json"}
        self.status()

    def status(self) -> dict:
        """
        Checks the status of the Geoserver server

        :returns: Status response in Json format

        """
        connection_url = self.url + "/about/status.json"
        response = requests.get(connection_url, auth=self.auth)
        response.raise_for_status()
        return response.json()

    @property
    def workspaces(self) -> dict:
        """
        Checks for existing workspaces in the Geoserver server

        :returns: Information about workspaces in Json format
        """
        workspaces_api_url = f"{self.url}/workspaces/"
        response = requests.get(workspaces_api_url, auth=self.auth)
        response.raise_for_status()
        return response.json()
