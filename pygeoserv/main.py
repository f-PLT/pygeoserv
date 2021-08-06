"""Testing script"""
import pprint

from pygeoserv import Pygeoserv

BASE_URL = "http://192.168.0.20:8600/geoserver"
AUTH = ("admin", "myawesomegeoserver")


def main():
    """Main script method"""

    myconnection = Pygeoserv(url=BASE_URL, auth=AUTH)
    # myconnection.workspaces()
    # workspace_name = "bobbyMcgeedfgdfgdf"

    # myconnection.create_workspace(workspace_name)
    pprint.pprint(myconnection.workspaces)


if __name__ == "__main__":
    main()
