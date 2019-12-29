version=$(date +"%y-%m-%d-%H-%M-%S")_dev_0.1
echo $version
docker build -t wucong/vh-server:$version .