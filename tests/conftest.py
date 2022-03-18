import pytest

from pygeoserv.geoserver import Geoserver

GEOSERVER_URL = "http://0.0.0.0:9876/geoserver"
AUTH = ("admin", "myawesomegeoserver")
DATA_BASE_PATH = "/data"
SHAPEFILE_DATA_PATH = f"{DATA_BASE_PATH}/shapefile"
SHAPEFILE_TEST_DATA = "test_data"


@pytest.fixture(name="geoserver")
def gs():
    yield Geoserver(GEOSERVER_URL, AUTH)
