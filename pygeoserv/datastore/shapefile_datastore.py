import requests

from pygeoserv.datastore.abstract_datastore import AbstractDatastore
from pygeoserv.workspace import Workspace
from pygeoserv.geoserver_requests.datastore import (
    create_shapefile_store_request,
    configure_datastore_request,
    publish_shapefile_layer_request,
    remove_shapefile_layer_request,
)


class ShapefileDatastore(AbstractDatastore):
    def __init__(self, workspace: Workspace, datastore_name: str, data_path: str):
        """
        Shapefile datastore object

        :param workspace: Workspace instance
        :param datastore_name: Datastore's name
        :param data_path: Path to the data on the server
        """
        super().__init__(
            workspace=workspace, datastore_name=datastore_name, data_path=data_path
        )

    #
    # Abstract class implementation
    #

    def create_datastore(self) -> requests.Response:
        """

        :return: Response object
        """
        response = self._create_shapefile_store()
        print(response.status_code)
        if response.status_code != 201:
            return response

        response = self._configure_datastore()
        if response.status_code != 200:
            return response

        return response

    def remove_store(self) -> requests.Response:
        """

        :return: Response object
        """
        request_url = f"{self.url}?recurse=true"
        response = requests.delete(url=request_url, auth=self.geoserver.auth)
        return response

    def publish_layer(self, filename) -> requests.Response:
        """

        :param filename: Filename of layer to publish
        :return: Response object
        """
        response = publish_shapefile_layer_request(
            url=self.geoserver.url,
            auth=self.geoserver.auth,
            workspace_name=self.workspace.name,
            datastore_name=self.name,
            filename=filename,
        )
        return response

    def remove_layer(self, filename) -> requests.Response:
        """

        :param filename: Filename of layer to publish
        :return: Response object
        """
        response = remove_shapefile_layer_request(
            url=self.geoserver.url,
            auth=self.geoserver.auth,
            workspace_name=self.workspace.name,
            datastore_name=self.name,
            filename=filename,
        )
        response.raise_for_status()
        return response

    #
    # ShapefileDatastore class functions
    #

    def _create_shapefile_store(self) -> requests.Response:
        """
        Initial creation of shapefile datastore. Trying to create and configure
        the this type of datastore often creates problems. It was found to be more
        reliable in two steps.

        :return:
        """

        response = create_shapefile_store_request(
            url=self.geoserver.url,
            auth=self.geoserver.auth,
            workspace_name=self.workspace.name,
            datastore_name=self.name,
        )
        response.raise_for_status()
        return response

    def _configure_datastore(self) -> requests.Response:
        """
        Configures the connection parameters of the datastore.
        This is done as a secondary step because Geoserver tends to create the wrong type of datastore
        (shapefile instead of directory of shapefiles) when setting them at creation.

        :returns: Response object
        """
        response = configure_datastore_request(
            url=self.geoserver.url,
            auth=self.geoserver.auth,
            workspace_name=self.workspace.name,
            datastore_name=self.name,
            data_path=self.data_path,
        )
        response.raise_for_status()
        return response
