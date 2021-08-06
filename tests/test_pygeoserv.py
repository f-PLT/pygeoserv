"""[summary]"""
from pygeoserv import Pygeoserv

AUTH = ("admin", "myawesomegeoserver")


def test_bogus():
    my_geoserver = Pygeoserv("http://192.168.0.20:8600/geoserver", AUTH)
    response = my_geoserver.workspaces
    url = response["workspaces"]["workspace"][0]["href"]
    assert url == "http://192.168.0.20:8600/geoserver/rest/workspaces/sentiers.json"

