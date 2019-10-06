#!/bin/bash
CFD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
VERSION=$1
docker pull wucong/vh:$VERSION
docker stop vh
docker rm vh
docker run -it --name vh -v $CFD/db_orage:/vh/db_storage -v $CFD/dict:/vh/dict   -p 80:8080 wucong/vh:$VERSION