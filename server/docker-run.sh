#!/bin/bash


CFD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
docker build -t vh .
docker stop vh 
docker rm vh 
docker run -d --name vh -v $CFD/db_storage:/vh/db_storage:rw -v $CFD/dict:/vh/dict:rw   -p 127.0.0.1:10000:8080  wucong/vh:0.0.3  