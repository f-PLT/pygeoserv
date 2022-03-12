import requests

from pygeoserv.utils import bool2string, HEADERS_JSON


def create_workspace_request(
    url: str, auth: tuple, name: str, is_isolated: bool = False
) -> requests.Response:
    """
    Post request wrapper to create a Geoserver workspace

    :param url: Base url of Geoserver instance
    :param auth: Authentification tuple (username, password)
    :param name: Name of the workspace to be created
    :param is_isolated: , defaults to False
    :return: Response object
    """
    request_url = f"{url}/rest/workspaces/"
    isolate = bool2string(is_isolated)
    payload = {"workspace": {"name": name, "isolated": isolate}}

    response = requests.post(
        url=request_url,
        json=payload,
        auth=auth,
        headers=HEADERS_JSON,
    )
    return response

def workspace_info_request(url: str, auth: tuple, name: str):
    """_summary_

    :param url: _description_
    :param auth: _description_
    :param name: _description_
    :return: _description_
    """
    request_url = f"{url}/rest/workspaces/{name}"
    response = requests.get(
        url=request_url,
        auth=auth,
        headers=HEADERS_JSON,
    )
    return response

def workspace_datastore_info_request(url: str, auth: tuple, name: str):
    """_summary_

    :param url: _description_
    :param auth: _description_
    :param name: _description_
    :return: _description_
    """
    request_url = f"{url}/rest/workspaces/{name}/datastores"
    response = requests.get(
        url=request_url,
        auth=auth,
        headers=HEADERS_JSON,
    )
    return response


def remove_workspace_request(url: str, auth: tuple, name: str)-> requests.Response:
    """_summary_

    :param url: _description_
    :param auth: _description_
    :param name: _description_
    :return: _description_
    """
    request_url = f"{url}/rest/workspaces/{name}?recurse=true"
    response = requests.delete(url=request_url, auth=auth, headers=HEADERS_JSON)
    return response
