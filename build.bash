#!/bin/bash

docker build --platform linux/amd64 --pull --rm -f ./Dockerfile -t registry.cn-shanghai.aliyuncs.com/ais/hivision-id-photos:latest .

docker image push registry.cn-shanghai.aliyuncs.com/ais/hivision-id-photos:latest
