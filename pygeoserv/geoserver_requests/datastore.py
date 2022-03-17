import requests

from pygeoserv.datastore.payload import shapefile
from pygeoserv.utils import HEADERS_JSON

#
# Shapefile requests
#


def _base_datastore_path(url: str, workspace_name: str, datastore_name: str = ""):
    if datastore_name:
        return f"{url}/rest/workspaces/{workspace_name}/datastores/{datastore_name}"
    return f"{url}/rest/workspaces/{workspace_name}/datastores"


def create_shapefile_store_request(
    url: str, auth: tuple, workspace_name: str, datastore_name: str
) -> requests.Response:
    """
    Initial creation of shapefile datastore. Trying to create and configure
    the this type of datastore often creates problems. It was found to be more
    reliable in two steps.

    :param url: Base url of Geoserver instance
    :param auth: Authentification tuple (username, password)
    :param workspace_name: Name of the workspace to be created

    :return:
    """

    request_url = _base_datastore_path(url, workspace_name)
    payload = shapefile.shapefile_datastore_creation(datastore_name)

    response = requests.post(
        url=request_url, json=payload, auth=auth, headers=HEADERS_JSON
    )
    return response


def configure_datastore_request(
    url: str, auth: tuple, workspace_name: str, datastore_name: str, data_path: str
) -> requests.Response:
    """
    Configures the connection parameters of the datastore.
    This is done as a secondary step because Geoserver tends to create
    the wrong type of datastore (shapefile instead of directory of shapefiles)
    when setting them at creation.

    :param url: Base url of Geoserver instance
    :param auth: Authentification tuple (username, password)
    :param workspace_name: Name of the workspace containing the datastore
    :param data_path: Path to the folder containing the shapefiles on the server

    :returns: Response object
    """
    geoserver_datastore_path = f"file://{data_path}"
    base_url = _base_datastore_path(url, workspace_name, datastore_name)
    request_url = f"{base_url}"
    payload = shapefile.shapefile_datastore_configuration(
        datastore_name, geoserver_datastore_path
    )
    response = requests.put(
        url=request_url,
        json=payload,
        auth=auth,
        headers=HEADERS_JSON,
    )
    return response


def publish_shapefile_layer_request(
    url: str, auth: tuple, workspace_name: str, datastore_name: str, filename: str
) -> requests.Response:
    """
    Request to publish a shapefile layer from a datastore

    :param url: Base url of Geoserver instance
    :param auth: Authentification tuple (username, password)
    :param workspace_name: Name of the workspace containing the datastore
    :param datastore_name: Name of datastore containing the layer
    :param filename: Filename of layer to publish
    :return: Response object
    """
    base_url = _base_datastore_path(url, workspace_name, datastore_name)
    request_url = f"{base_url}/featuretypes"
    payload = shapefile.shapefile_publishing_configuration(filename)
    response = requests.post(
        url=request_url,
        json=payload,
        auth=auth,
        headers=HEADERS_JSON,
    )
    return response


def remove_shapefile_layer_request(
    url: str, auth: tuple, workspace_name: str, datastore_name: str, filename: str
) -> requests.Response:
    """
    Request to remove a shapefile layer from a datatore

    :param url: Base url of Geoserver instance
    :param auth: Authentification tuple (username, password)
    :param workspace_name: Name of the workspace containing the datastore
    :param datastore_name: Name of datastore containing the layer
    :param filename: Filename of layer to publish
    :return: Response object
    """
    base_url = _base_datastore_path(url, workspace_name, datastore_name)
    request_url = f"{base_url}/featuretypes/{filename}?recurse=true"
    response = requests.delete(url=request_url, auth=auth, headers=HEADERS_JSON)
    return response
