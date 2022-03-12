import requests

from pygeoserv.utils import HEADERS_JSON
from pygeoserv.datastore.payload import shapefile


#
# Shapefile requests
#


def create_shapefile_store_request(
    url: str, auth: tuple, workspace_name: str, datastore_name: str
) -> requests.Response:
    """
    Initial creation of shapefile datastore. Trying to create and configure
    the this type of datastore often creates problems. It was found to be more
    reliable in two steps.

    :return:
    """

    request_url = f"{url}/rest/workspaces/{workspace_name}/datastores"
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
    This is done as a secondary step because Geoserver tends to create the wrong type of datastore
    (shapefile instead of directory of shapefiles) when setting them at creation.

    :returns: Response object
    """
    geoserver_datastore_path = f"file://{data_path}"
    request_url = f"{url}/rest/workspaces/{workspace_name}/datastores/{datastore_name}"
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

    :param filename: Filename of layer to publish
    :return: Response object
    """
    request_url = f"{url}/rest/workspaces/{workspace_name}/datastores/{datastore_name}/featuretypes"
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

    :param filename: Filename of layer to publish
    :return: Response object
    """
    request_url = f"{url}/rest/workspaces/{workspace_name}/datastores/{datastore_name}/featuretypes/{filename}?recurse=true"
    response = requests.delete(url=request_url, auth=auth, headers=HEADERS_JSON)
    return response
