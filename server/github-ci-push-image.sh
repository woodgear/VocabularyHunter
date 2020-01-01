REF=$1
TAG=$(echo ${REF} | sed -e 's/refs\/tags\/vh-server-//')
echo $TAG
docker build -t wucong/vh-server:$TAG .
docker push wucong/vh-server:$TAG
