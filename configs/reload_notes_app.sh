#!/usr/bin/env bash

if [ -z "$1" ]; then
  docker pull kishmakov/notes_app:latest
elif [ "$1" == "local" ]; then
  docker build -t kishmakov/notes_app:latest ../notes_app/
fi

docker stop notes_cont
docker rm notes_cont
docker run -d -p 5002:5003 --name notes_cont kishmakov/notes_app:latest
