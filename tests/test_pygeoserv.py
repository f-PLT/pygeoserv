from pygeoserv.geoserver import Geoserver


class TestGeoserver:
    def test_status(self, geoserver: Geoserver):
        geoserver.status()

    def test_workspaces(self, geoserver: Geoserver):
        geoserver.workspaces
