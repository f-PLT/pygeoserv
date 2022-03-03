import requests

SHAPEFILE_DS = "shapefile"

def bool2string(isolated: bool) -> str:
    """
    Transforms a bool value to a string equivalent.

    :param isolated: Bool value
    :return: Bool in string format
    """
    return "True" if isolated else "False"


def is_response_ok(response: requests.Response, status_code_expected: int=200) -> bool:
    """
    Checks if response was successful

    :param response: Response object of an executed request
    :param status_code_expected: Expected response status code for successful request.

    :returns: True if response is ok
    """
    if response.status_code == 404:
        return False
    if response.status_code != status_code_expected:
        response.raise_for_status()
    return True
