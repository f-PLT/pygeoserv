"""Testing script"""
import pprint

from pygeoserv import Pygeoserv

BASE_URL = "http://192.168.0.20:8600/geoserver"
AUTH = ("admin", "myawesomegeoserver")


def main():
    """Main script method"""

    workspace_name = "my-isolated-workspace"
    myconnection = Pygeoserv(url=BASE_URL, auth=AUTH)
    myconnection.create_workspace(workspace_name)
    # myconnection.workspaces()

    pprint.pprint(myconnection.workspaces)
    store_name = "my-datastore"
    myconnection.create_shapefile_store(
        workspace_name=workspace_name,
        store_name=store_name,
        folder_path="/user_workspaces/",
    )
    myconnection.get_workspace(workspace_name=workspace_name)
    myconnection.get_datastore(store_name=store_name, workspace_name=workspace_name)


if __name__ == "__main__":
    main()
