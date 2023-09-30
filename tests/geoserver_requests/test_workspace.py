from pygeoserv.geoserver_requests.workspace import (
    create_workspace_request,
    remove_workspace_request,
    workspace_datastore_info_request,
    workspace_info_request,
)
from tests.conftest import AUTH, GEOSERVER_URL


class TestWorkspaceRequests:
    workspace_dict = {
        "create_workspace": "test-create-workspace",
        "workspace_info": "test-workspace-info",
        "workspace_datastores_info": "test-workspace-datastores-info",
        "remove_workspace": "test-remove-workspace",
    }

    def teardown_class(self):
        for _, ws in self.workspace_dict.items():
            try:
                remove_workspace_request(GEOSERVER_URL, AUTH, ws)
            except Exception:
                pass

    def test_create_workspace(self):
        response = create_workspace_request(
            GEOSERVER_URL, AUTH, self.workspace_dict["create_workspace"]
        )
        assert response.status_code == 201

    def test_workspace_info(self):
        response = workspace_info_request(
            GEOSERVER_URL, AUTH, self.workspace_dict["create_workspace"]
        )
        assert response.status_code == 200

    def test_workspace_datastore_info(self):
        response = workspace_datastore_info_request(
            GEOSERVER_URL, AUTH, self.workspace_dict["create_workspace"]
        )
        assert response.status_code == 200

    def test_remove_workspace(self):
        response = remove_workspace_request(
            GEOSERVER_URL, AUTH, self.workspace_dict["create_workspace"]
        )
        assert response.status_code == 200
