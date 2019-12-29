#!/bin/bash

name=$1
CFD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
docker stop vh 
docker rm vh 
docker run -d --name vh  -v $CFD/vol:/vh/vol:rw  -p 10000:10000  $name
docker logs -f vh