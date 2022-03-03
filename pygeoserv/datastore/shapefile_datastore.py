import requests

from pygeoserv.datastore.abstract_datastore import AbstractDatastore
from pygeoserv.datastore.payload import shapefile
from pygeoserv.workspace import Workspace


class ShapefileDatastore(AbstractDatastore):
    def __init__(self, workspace: Workspace, datastore_name: str, data_path: str):
        """
        Shapefile datastore object

        :param workspace: Workspace instance
        :param datastore_name: Datastore's name
        :param data_path: Path to the data on the server
        """
        super().__init__(workspace=workspace, datastore_name=datastore_name, data_path=data_path)
        if not self._does_datastore_exist():
            self.create_datastore()

    #
    # Abstract class implementation
    #

    def create_datastore(self) -> requests.Response:
        """

        :return: Response object
        """
        response = self._create_shapefile_store()
        if response.status_code != 200:
            return response

        response = self._configure_datastore()
        if response.status_code != 201:
            return response

        return response

    def remove_store(self) -> requests.Response:
        """

        :return: Response object
        """
        request_url = f"{self.url}?recurse=true"
        response = requests.delete(
            url=request_url, auth=self.geoserver.auth, headers=self.geoserver.headers
        )
        return response

    def publish_layer(self, filename) -> requests.Response:
        """

        :param filename: Filename of layer to publish
        :return: Response object
        """
        request_url = f"{self.url}/featuretypes"
        payload = shapefile.shapefile_publishing_configuration(filename)
        response = requests.post(
            url=request_url,
            json=payload,
            auth=self.geoserver.auth,
            headers=self.geoserver.headers,
        )
        return response

    def remove_layer(self, filename) -> requests.Response:
        """

        :param filename: Filename of layer to publish
        :return: Response object
        """
        request_url = f"{self.url}/featuretypes/{filename}?recurse=true"
        response = requests.delete(
            url=request_url, auth=self.geoserver.auth, headers=self.geoserver.headers
        )
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

        request_url = f"{self.geoserver.url}/workspaces/{self.workspace.name}/datastores"
        payload = shapefile.shapefile_datastore_creation(self.name)

        response = requests.post(
            url=request_url,
            json=payload,
            auth=self.geoserver.auth,
            headers=self.geoserver.headers
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
        geoserver_datastore_path = f"file://{self.data_path}"
        request_url = f"{self.geoserver.url}/workspaces/{self.workspace.name}/datastores/{self.name}"
        payload = shapefile.shapefile_datastore_configuration(
            self.name, geoserver_datastore_path
        )
        response = requests.put(
            url=request_url,
            json=payload,
            auth=self.geoserver.auth,
            headers=self.geoserver.headers,
        )
        response.raise_for_status()
        return response
