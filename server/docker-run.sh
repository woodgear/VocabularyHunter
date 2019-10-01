
CFD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
echo $CFD
# docker run -v $CFD/db_storage:/vh/db_storage -v $CFD/dict:/vh/dict  -p 5000:80  --entrypoint /bin/bash -it vh
docker start -v $CFD/db_storage:/vh/db_storage -v $CFD/dict:/vh/dict  -p 5000:80  