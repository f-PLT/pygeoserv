"""
Main pygeoserv module
"""
from typing import Dict
import pprint
import json

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
        self.headers = {"Content-type": "application/xml"}
        self._workspace_isolation_default = "True"

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

    def create_workspace(self, workspace_name, isolated=None) -> bool:
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
        request_url = f"{self.url}workspaces/"
        if not isolated:
            isolated = self._workspace_isolation_default
        payload = """
        <workspace>
            <name>{}</name>
            <isolated>{}</isolated>
        </workspace>
        """.format(
            workspace_name, isolated
        )

        request = requests.post(
            url=request_url,
            data=payload,
            auth=self.auth,
            headers=self.headers,
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
        request_url = f"{self.url}workspaces/{workspace_name}/datastores"
        payload = """
        <dataStore>
            <name>{}</name>
            <type>Directory of spatial files (shapefiles)</type>
            <enabled>true</enabled>
            <connectionParameters>
                <charset>UTF-8</charset>
                <url>file://{}</url>
                <fstype>shape</fstype>
                <filetype>shapefile</filetype>
            </connectionParameters>
        </dataStore>
        """.format(
            store_name, folder_path
        )

        request = requests.post(
            url=request_url, data=payload, auth=self.auth, headers=self.headers
        )
        request.raise_for_status()
        return True

    def get_datastore(self, store_name, workspace_name="default"):
        request_url = f"{self.url}workspaces/{workspace_name}/datastores/{store_name}"

        request = requests.get(url=request_url, auth=self.auth, headers=self.headers)
        request.raise_for_status()
        pprint.pprint(request.json())
        return True

    def get_workspace(self, workspace_name="default"):
        request_url = f"{self.url}workspaces/{workspace_name}"
        request = requests.get(url=request_url, auth=self.auth, headers=self.headers)
        request.raise_for_status()
        pprint.pprint(request.json())
        return True