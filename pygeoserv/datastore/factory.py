from pygeoserv.datastore import shapefile_datastore
from pygeoserv.datastore.abstract_datastore import AbstractDatastore, SHAPEFILE
from pygeoserv.workspace import Workspace

DATASTORES = {SHAPEFILE: shapefile_datastore.ShapefileDatastore}


def datastore_factory(
    store_type: str, workspace: Workspace, datastore_name: str, data_path: str
) -> AbstractDatastore:
    """
    Datastore factory utility function

    :param store_type: Store type
    :param workspace: Workspace instance
    :param datastore_name: Datastore name
    :param data_path: Path to data on the server
    
    :returns: Datastore instance
    """

    datastore_instance = DATASTORES[store_type](workspace, datastore_name, data_path)

    return datastore_instance
