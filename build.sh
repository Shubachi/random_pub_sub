#!/bin/sh

docker build -t test_publisher ./publisher
docker build -t test_subscriber ./subscriber
