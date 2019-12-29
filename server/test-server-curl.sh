curl --compressed -X POST \
  http://34.69.254.157/api/vh/explain \
  -H 'Accept: */*' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Cache-Control: no-cache' \
  -H 'Connection: keep-alive' \
  -H 'Content-Length: 24' \
  -H 'Content-Type: application/json' \
  -H 'Host: 127.0.0.1:10000' \
  -H 'Postman-Token: ff6a19f2-889e-4da2-8ac6-a194d3654f11,0e84b77d-c9a0-4abb-a4dd-d36ae87a6616' \
  -H 'User-Agent: PostmanRuntime/7.20.1' \
  -H 'cache-control: no-cache' \
  -H 'id: mock_id' \
  -d '{
   "words": ["tree"]
}' --output -