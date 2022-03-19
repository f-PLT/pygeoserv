"""
Module for complex Geoserver API payloads
"""


def shapefile_datastore_creation(store_name: str) -> dict:
    """

    :param store_name: Name of the store being created
    :return: Payload dictionary
    """
    payload = {
        "dataStore": {
            "name": store_name,
            "type": "Directory of spatial files (shapefiles)",
            "connectionParameters": {"entry": []},
        }
    }
    return payload


def shapefile_datastore_configuration(
    store_name: str, geoserver_datastore_path: str
) -> dict:
    """

    :param store_name: Name of the store being configured
    :param geoserver_datastore_path: Path (server-side) used by the store
    :return: Payload dictionary
    """
    payload = {
        "dataStore": {
            "name": store_name,
            "type": "Directory of spatial files (shapefiles)",
            "connectionParameters": {
                "entry": [
                    {"$": "UTF-8", "@key": "charset"},
                    {"$": "shapefile", "@key": "filetype"},
                    {"$": "true", "@key": "create spatial " "index"},
                    {"$": "true", "@key": "memory mapped " "buffer"},
                    {"$": "GMT", "@key": "timezone"},
                    {"$": "true", "@key": "enable spatial " "index"},
                    {"$": f"http://{store_name}", "@key": "namespace"},
                    {"$": "true", "@key": "cache and reuse " "memory maps"},
                    {"$": geoserver_datastore_path, "@key": "url"},
                    {"$": "shape", "@key": "fstype"},
                ]
            },
        }
    }
    return payload


def shapefile_publishing_configuration(filename: str) -> dict:
    """

    :param filename: Name of the file being published
    :return: Payload dictionary
    """
    payload = {
        "featureType": {
            "name": filename,
            "nativeCRS": """
                GEOGCS[
                    "WGS 84", 
                    DATUM[
                        "World Geodetic System 1984",
                        SPHEROID["WGS 84", 6378137.0, 298.257223563, AUTHORITY["EPSG","7030"]],
                        AUTHORITY["EPSG","6326"]
                    ],
                    PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]],
                    UNIT["degree", 0.017453292519943295],
                    AXIS["Geodetic longitude", EAST],
                    AXIS["Geodetic latitude", NORTH],
                    AUTHORITY["EPSG","4326"]
                ]
            """,
            "srs": "EPSG:4326",
            "projectionPolicy": "REPROJECT_TO_DECLARED",
            "maxFeatures": 5000,
            "numDecimals": 6,
        }
    }
    return payload
