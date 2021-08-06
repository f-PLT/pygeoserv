"""
Main pygeoserv module
"""
from typing import Dict

import requests


class Pygeoserv:
    """Pygeoserv class"""

    def __init__(self, url: str, auth: tuple):
        """
        Create a connection to Geoserver instance

        Parameters
        ----------
        url : str
            Base url of Geoserver instance
        auth : tuple
            Credentials tuple ("username", "password")
        """
        self.url = f"{url}/rest/" if not url.endswith("/") else f"{url}rest/"
        self.auth = auth
        self.headers = {"content-type": "application/xml"}

    @property
    def workspaces(self) -> Dict:
        """
        [summary]

        Returns
        -------
        [type]
            [description]
        """
        workspaces_api_url = f"{self.url}workspaces/"
        request = requests.get(workspaces_api_url, auth=self.auth)
        return request.json()

    def create_workspace(self, workspace_name) -> bool:
        """
        [summary]

        Parameters
        ----------
        workspace_name : str
            [description]

        Returns
        -------
        [type]
            [description]
        """
        workspaces_api_url = f"{self.url}workspaces/"
        payload = f"<workspace><name>{workspace_name}</name></workspace>"

        request = requests.post(
            workspaces_api_url, data=payload, auth=self.auth, headers=self.headers
        )
        request.raise_for_status()
        return True

    def create_shapefile_store(self, workspace_name, store_name, folder_path) -> bool:
        """
        Create a shapefile directory store.

        Parameters
        ----------
        workspace_name : str
            [description]
        store_name : str
            [description]
        folder_path : str
            [description]
        """
        shapefile_api_url = f"{self.url}{workspace_name}"
        payload = [store_name, folder_path]
        return True
