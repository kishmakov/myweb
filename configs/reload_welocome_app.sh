#!/usr/bin/env bash

docker pull kishmakov/welcome_app:latest
docker stop welcome_cont
docker rm welcome_cont
docker run -d -p 5000:5001 --name welcome_cont kishmakov/welcome_app:latest
