REF=$1
TAG=$(echo ${REF} | sed -e 's/refs\/tags\/vh-server-//')
echo $TAG
kubectl set image deployment vh-server  vh-server=wucong/vh-server:$TAG -nvh