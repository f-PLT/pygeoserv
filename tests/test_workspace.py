from pygeoserv.geoserver import Geoserver
from pygeoserv.geoserver_requests.workspace import remove_workspace_request
from pygeoserv.workspace import Workspace
from tests.conftest import AUTH, GEOSERVER_URL


class TestWorkspace:
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

    def test_workspace_creation(self, geoserver: Geoserver):
        workspace = Workspace(geoserver, self.workspace_dict["create_workspace"])
        workspace.remove_workspace()

    def test_workspace_info(self, geoserver: Geoserver):
        workspace = Workspace(geoserver, self.workspace_dict["workspace_info"])
        workspace.info()

    def test_workspace_datastores_info(self, geoserver: Geoserver):
        workspace = Workspace(
            geoserver, self.workspace_dict["workspace_datastores_info"]
        )
        workspace.datastores_info()

    def test_workspace_creation_and_removal(self, geoserver: Geoserver):
        workspace = Workspace(geoserver, self.workspace_dict["remove_workspace"])
        workspace.remove_workspace()
