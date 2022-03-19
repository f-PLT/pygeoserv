import requests

from pygeoserv.utils import HEADERS_JSON, bool2string


def _base_workspace_path(url: str, workspace_name: str = ""):
    if workspace_name:
        return f"{url}/rest/workspaces/{workspace_name}"
    return f"{url}/rest/workspaces"


def create_workspace_request(
    url: str, auth: tuple, name: str, is_isolated: bool = False
) -> requests.Response:
    """
    Request wrapper to create a Geoserver workspace

    :param url: Base url of Geoserver instance
    :param auth: Authentification tuple (username, password)
    :param name: Name of the workspace to be created
    :param is_isolated: , defaults to False
    :return: Response object
    """
    request_url = _base_workspace_path(url)
    isolate = bool2string(is_isolated)
    payload = {"workspace": {"name": name, "isolated": isolate}}

    response = requests.post(
        url=request_url,
        json=payload,
        auth=auth,
        headers=HEADERS_JSON,
    )
    return response


def workspace_info_request(url: str, auth: tuple, name: str) -> requests.Response:
    """
    Request wrapper to get a workspace's information

    :param url: Base url of Geoserver instance
    :param auth: Authentification tuple (username, password)
    :param name: Name of the workspace to be created
    :return: Response object
    """

    request_url = _base_workspace_path(url, name)
    response = requests.get(
        url=request_url,
        auth=auth,
        headers=HEADERS_JSON,
    )
    return response


def workspace_datastore_info_request(url: str, auth: tuple, name: str):
    """
    Request wrapper to get a workspace datatores' information

    :param url: Base url of Geoserver instance
    :param auth: Authentification tuple (username, password)
    :param name: Name of the workspace to be created
    :return: Response object
    """
    base_url = _base_workspace_path(url, name)
    request_url = f"{base_url}/datastores"
    response = requests.get(
        url=request_url,
        auth=auth,
        headers=HEADERS_JSON,
    )
    return response


def remove_workspace_request(url: str, auth: tuple, name: str) -> requests.Response:
    """
    Request wrapper to remove a Geoserver workspace

    :param url: Base url of Geoserver instance
    :param auth: Authentification tuple (username, password)
    :param name: Name of the workspace to be created
    :return: Response object
    """
    base_url = _base_workspace_path(url, name)
    request_url = f"{base_url}?recurse=true"
    response = requests.delete(url=request_url, auth=auth, headers=HEADERS_JSON)
    return response
