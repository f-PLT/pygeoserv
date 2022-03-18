from pygeoserv.geoserver_requests.datastore import (
    configure_shapefile_store_request,
    create_shapefile_store_request,
    publish_shapefile_layer_request,
    remove_shapefile_layer_request,
)
from pygeoserv.geoserver_requests.workspace import (
    create_workspace_request,
    remove_workspace_request,
)
from tests.conftest import AUTH, GEOSERVER_URL, SHAPEFILE_DATA_PATH, SHAPEFILE_TEST_DATA


class TestDatastoreRequests:

    workspace_dict = {
        "create_shapefile_store": "test-create-shapefile",
        "configure_shapefile_store": "test-configure-shapefile",
        "publish_shapefile_layer": "test-publish-shapefile",
        "remove_shapefile_layer": "test-remove-shapefile",
    }

    datastore_name = "shapefile_datastore"
    data_path = "/data"

    def teardown_class(self):
        for _, ws in self.workspace_dict.items():
            try:
                remove_workspace_request(GEOSERVER_URL, AUTH, ws)
            except Exception:
                pass

    def test_create_shapefile_store(self):
        create_workspace_request(
            GEOSERVER_URL, AUTH, self.workspace_dict["create_shapefile_store"]
        )
        response = create_shapefile_store_request(
            GEOSERVER_URL,
            AUTH,
            self.workspace_dict["create_shapefile_store"],
            self.datastore_name,
        )
        assert response.status_code == 201

    def test_configure_shapefile_store(self):
        create_workspace_request(
            GEOSERVER_URL, AUTH, self.workspace_dict["configure_shapefile_store"]
        )
        create_shapefile_store_request(
            GEOSERVER_URL,
            AUTH,
            self.workspace_dict["configure_shapefile_store"],
            self.datastore_name,
        )
        response = configure_shapefile_store_request(
            GEOSERVER_URL,
            AUTH,
            self.workspace_dict["configure_shapefile_store"],
            self.datastore_name,
            self.data_path,
        )
        assert response.status_code == 200

    def test_publish_shapefile_layer(self):
        create_workspace_request(
            GEOSERVER_URL, AUTH, self.workspace_dict["publish_shapefile_layer"]
        )
        create_shapefile_store_request(
            GEOSERVER_URL,
            AUTH,
            self.workspace_dict["publish_shapefile_layer"],
            self.datastore_name,
        )
        configure_shapefile_store_request(
            GEOSERVER_URL,
            AUTH,
            self.workspace_dict["publish_shapefile_layer"],
            self.datastore_name,
            SHAPEFILE_DATA_PATH,
        )
        response = publish_shapefile_layer_request(
            GEOSERVER_URL,
            AUTH,
            self.workspace_dict["publish_shapefile_layer"],
            self.datastore_name,
            SHAPEFILE_TEST_DATA,
        )
        assert response.status_code == 201

    def test_remove_shapefile_layer(self):
        create_workspace_request(
            GEOSERVER_URL, AUTH, self.workspace_dict["publish_shapefile_layer"]
        )
        create_shapefile_store_request(
            GEOSERVER_URL,
            AUTH,
            self.workspace_dict["publish_shapefile_layer"],
            self.datastore_name,
        )
        configure_shapefile_store_request(
            GEOSERVER_URL,
            AUTH,
            self.workspace_dict["publish_shapefile_layer"],
            self.datastore_name,
            SHAPEFILE_DATA_PATH,
        )
        response = remove_shapefile_layer_request(
            GEOSERVER_URL,
            AUTH,
            self.workspace_dict["publish_shapefile_layer"],
            self.datastore_name,
            SHAPEFILE_TEST_DATA,
        )
        assert response.status_code == 200
