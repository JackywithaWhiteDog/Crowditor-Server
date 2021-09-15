#!bin/sh

if [ $# -ne 2 ] && [ "$1" == "-p" ]; then
    docker-compose --env-file prod.env config
else
    docker-compose config
fi
