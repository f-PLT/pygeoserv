"""
Main pygeoserv module
"""
import json
import pprint
from typing import Dict

import requests
from utils import bool2string


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
        self.headers = {"Content-Type": "application/json"}
        self.connected_workspaces = []

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
        response = requests.get(workspaces_api_url, auth=self.auth)
        return response.json()


def create_workspace(url, auth, workspace_name, isolated=False) -> bool:
    """
    [summary]

    Parameters
    ----------
    workspace_name : str
        [description]

    isolated : str
        [description]

    Returns
    -------
    [type]
        [description]
    """
    request_url = f"{url}/workspaces/"
    payload = {"workspace": {"name": workspace_name, "isolated": "false"}}

    headers = {"Content-type": "application/json"}

    response = requests.post(
        url=request_url,
        json=payload,
        auth=auth,
        headers=headers,
    )
    response.raise_for_status()
    return True

    def remove_workspace(self, workspace_name):
        """
        Request to remove workspace and all associated datastores and layers.
        @param workspace_name: Name of workspace to remove
        @return: Response object
        """
        request_url = f"{self.url}/workspaces/{workspace_name}?recurse=true"
        response = requests.delete(
            url=request_url, auth=self.auth, headers=self.headers
        )

        return response


def create_shapefile_store(self, workspace_name, store_name, folder_path):
    response = self._create_shapefile_store(workspace_name, store_name)
    if response.status_code != 200:
        return response

    response = self._configure_datastore(workspace_name, store_name, folder_path)
    if response.status_code != 201:
        return response


def _create_shapefile_store(self, workspace_name, store_name):
    """
    Create a shapefile directory store.

    Parameters
    ----------
    workspace_name : str
        [description]
    store_name : str
        [description]
    """
    request_url = f"{self.url}workspaces/{workspace_name}/datastores"
    payload = payloads.shapefile_datastore_creation(store_name)

    response = requests.post(
        url=request_url, json=payload, auth=self.auth, headers=self.headers
    )
    response.raise_for_status()
    return response


def _configure_datastore(self, workspace_name, store_name, datastore_path):
    """
    Configures the connection parameters of the datastore.
    This is done as a secondary step because Geoserver tends to create the wrong type of datastore
    (shapefile instead of directory of shapefiles) when setting them at creation.
    @param workspace_name: Name of the workspace in which the datastore is created
    @param datastore_name: Name of the datastore that will be created
    @return: Response object
    """
    geoserver_datastore_path = f"file://{datastore_path}"
    request_url = f"{self.url}/workspaces/{workspace_name}/datastores/{store_name}"
    payload = payloads.shapefile_datastore_configuration(
        store_name, geoserver_datastore_path
    )
    response = requests.put(
        url=request_url, json=payload, auth=self.auth, headers=self.headers
    )
    return response


def publish_shapefile(self, workspace_name, datastore_name, filename):
    # type:(Geoserver, str, str, str) -> requests.Response
    """
    Request to publish a shapefile in Geoserver. Does so by creating a `Feature type` in Geoserver.
    @param workspace_name: Workspace where file will be published
    @param datastore_name: Datastore where file will be published
    @param filename: Name of the shapefile (with no extentions)
    @return: Response object
    """
    request_url = "{}/workspaces/{}/datastores/{}/featuretypes".format(
        self.api_url, workspace_name, datastore_name
    )

    # This is just a basic example. There are lots of other attributes that can be configured
    # https://docs.geoserver.org/latest/en/api/#1.0.0/featuretypes.yaml
    payload = payloads.shapefile_publishing_configuration(filename)
    response = requests.post(
        url=request_url, json=payload, auth=self.auth, headers=self.headers
    )
    return response


def remove_shapefile(self, workspace_name, datastore_name, filename):
    # type:(Geoserver, str, str, str) -> requests.Response
    """
    Request to remove specified Geoserver `Feature type` and corresponding layer.
    @param workspace_name: Workspace where file is published
    @param datastore_name: Datastore where file is published
    @param filename: Name of the shapefile (with no extentions)
    @return: Response object
    """
    request_url = "{}/workspaces/{}/datastores/{}/featuretypes/{}?recurse=true".format(
        self.api_url, workspace_name, datastore_name, filename
    )
    response = requests.delete(url=request_url, auth=self.auth, headers=self.headers)
    return response


def get_datastore(self, store_name, workspace_name="default"):
    request_url = f"{self.url}workspaces/{workspace_name}/datastores/{store_name}"

    response = requests.get(url=request_url, auth=self.auth, headers=self.headers)
    response.raise_for_status()
    pprint.pprint(response.json())
    return True


def get_workspace(self, workspace_name="default"):
    request_url = f"{self.url}workspaces/{workspace_name}"
    response = requests.get(url=request_url, auth=self.auth, headers=self.headers)
    response.raise_for_status()
    pprint.pprint(response.json())
    return True


def main():
    BASE_URL = "http://192.168.0.20:8600/geoserver/rest"

    AUTH = ("admin", "myawesomegeoserver")

    workspace = create_workspace(BASE_URL, AUTH, "my-isolated-workspace2")

    # data_path = "/user_workspaces/"
    # shapefile_store = datastore_factory(
    #     "shapefile", workspace, "my_shapefile_datastore", data_path
    # )


if __name__ == "__main__":
    main()
