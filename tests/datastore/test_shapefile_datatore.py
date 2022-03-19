from pygeoserv.datastore.factory import datastore_factory
from pygeoserv.datastore.shapefile_datastore import ShapefileDatastore
from pygeoserv.geoserver import Geoserver
from pygeoserv.geoserver_requests.workspace import remove_workspace_request
from pygeoserv.utils import SHAPEFILE_DS
from pygeoserv.workspace import create_workspace
from tests.conftest import AUTH, GEOSERVER_URL, SHAPEFILE_DATA_PATH, SHAPEFILE_LAYER


class TestShapefileDatastore:
    workspace_dict = {
        "create_datastore": "test-create-sh-datastore",
        "remove_datastore": "test-remove-sh-datastore",
        "publish_shapefile": "test-publish-shapefile-datastore",
        "remove_shapefile": "test-remove-shapefile-datastore",
        "factory_datastore": "test_shapefile_factory_datastore",
    }

    datastore_name = "test_shapefile_datastore"
    data_path = "/data"

    def teardown_class(self):
        for _, workspace in self.workspace_dict.items():
            try:
                remove_workspace_request(GEOSERVER_URL, AUTH, workspace)
            except Exception:
                pass

    def test_create_datastore(self, geoserver: Geoserver):
        workspace = create_workspace(geoserver, self.workspace_dict["create_datastore"])
        datastore = ShapefileDatastore(
            workspace, self.datastore_name, SHAPEFILE_DATA_PATH
        )
        response = datastore.create_datastore()
        assert response.status_code == 200

    def test_remove_datastore(self, geoserver: Geoserver):
        workspace = create_workspace(geoserver, self.workspace_dict["remove_datastore"])
        datastore = ShapefileDatastore(
            workspace, self.datastore_name, SHAPEFILE_DATA_PATH
        )
        datastore.create_datastore()
        response = datastore.remove_store()
        assert response.status_code == 200

    def test_publish_shapefile(self, geoserver: Geoserver):
        workspace = create_workspace(
            geoserver, self.workspace_dict["publish_shapefile"]
        )
        datastore = ShapefileDatastore(
            workspace, self.datastore_name, SHAPEFILE_DATA_PATH
        )
        datastore.create_datastore()
        response = datastore.publish_layer(SHAPEFILE_LAYER)
        assert response.status_code == 201

    def test_remove_shapefile(self, geoserver: Geoserver):
        workspace = create_workspace(geoserver, self.workspace_dict["remove_shapefile"])
        datastore = ShapefileDatastore(
            workspace, self.datastore_name, SHAPEFILE_DATA_PATH
        )
        datastore.create_datastore()
        datastore.publish_layer(SHAPEFILE_LAYER)
        response = datastore.remove_layer(SHAPEFILE_LAYER)
        assert response.status_code == 200

    def test_factory_shapefile_datastore(self, geoserver: Geoserver):
        workspace = create_workspace(
            geoserver, self.workspace_dict["factory_datastore"]
        )
        datastore = datastore_factory(
            SHAPEFILE_DS, workspace, self.datastore_name, SHAPEFILE_DATA_PATH
        )
        assert isinstance(datastore, ShapefileDatastore)
