#!/usr/bin/env bash

if [ -z "$1" ]; then
  docker pull kishmakov/welcome_app:latest
elif [ "$1" == "local" ]; then
  docker build -t kishmakov/welcome_app:latest ../welcome_app/
fi

docker stop welcome_cont
docker rm welcome_cont
docker run -d -p 5000:5001 --name welcome_cont kishmakov/welcome_app:latest
