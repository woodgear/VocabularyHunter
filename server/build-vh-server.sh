version=$1
echo $version
docker build -t wucong/vh-server:$version .