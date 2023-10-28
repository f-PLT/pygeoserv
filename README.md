# pygeoserv

This was a small experimental project for a module built around Geoserver's API for a more 
automated publishing of shapefiles and other data types.

This module was meant to be used on the machine or host running a Geoserver instance, 
as it requires access to the file system for layer creation.

However, since [geoserver-rest](https://github.com/gicait/geoserver-rest) and [GeoNode's own geoserver-restconfig](https://github.com/GeoNode/geoserver-restconfig) have both seen recent development, there is little value in continuing this little test project.

## Requirements

Outside of the package requirements, to use or test Pygeoserv, you need to install
Docker and Docker Compose on the system running it.
