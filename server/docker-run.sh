#!/bin/bash


CFD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
docker build -t vh .
# docker run -v $CFD/db_storage:/vh/db_storage -v $CFD/dict:/vh/dict  -p 8080:80  --entrypoint /bin/bash -it vh
docker stop vh 
docker rm vh 
docker run -it --name vh -v $CFD/db_storage:/vh/db_storage -v $CFD/dict:/vh/dict   -p 127.0.0.1:10000:8080  vh  