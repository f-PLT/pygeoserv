from abc import ABC, abstractmethod

import requests


from pygeoserv.workspace import Workspace
from pygeoserv.utils import is_response_ok

SHAPEFILE = "shapefile"


class AbstractDatastore(ABC):
    def __init__(self, workspace: Workspace, datastore_name: str, data_path: str):
        """

        :param workspace: Workspace instance
        :param datastore_name: Datastore's name
        :param data_path: Path to the data on the server
        """

        self.workspace = workspace
        self.geoserver = workspace.geoserver
        self.name = datastore_name
        self.url = f"{self.workspace.url}/datastores/{self.name}"
        self.data_path = data_path

    def _does_datastore_exist(self):
        """
        Checks if datastore exists

        :return: True is datastore exists
        """
        response = requests.get(
            url=self.url, auth=self.geoserver.auth, headers=self.geoserver.headers
        )
        return is_response_ok(response)

    @abstractmethod
    def create_datastore(self):
        pass

    @abstractmethod
    def remove_store(self):
        pass

    @abstractmethod
    def publish_layer(self, filename):
        pass

    @abstractmethod
    def remove_layer(self, filename):
        pass
