# Docker Container Images Refresher

Script to pull periodically your favourite images to prevent them to be deleted from DockerHub

# Background
Docker has changed their [container image retention](https://www.docker.com/pricing/retentionfaq) policy in the Free plans starting November 1, 2020.
Inactive images will be deleted after 6 months. An inactive image is a container image that has not been either pushed or pulled from the image repository in 6 or more months.
This script pulls your images periodically, so they don't become inactive.

## Usage
python docker-refresh.py

Edit settings.ini file with an interval period to refresh and your image list. Example:
```
refresh_interval_days=90 
images_to_refresh=myrepo/myimage:latest,myrepo/otherimage:1.0
```

Run this script at system startup... and keep your images alive in Docker hub :)

## Requirements
- Pyhton >= 3.7
- [Docker SDK for Python](https://pypi.org/project/docker/) : pip install docker
- A regular Docker installed in your system