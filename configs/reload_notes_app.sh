#!/usr/bin/env bash

docker pull kishmakov/notes_app:latest
docker stop notes_cont
docker rm notes_cont
docker run -d -p 5002:5003 --name notes_cont kishmakov/notes_app:latest
