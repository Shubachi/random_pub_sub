#!/bin/sh

docker build -t test_publisher ./publisher
docker build -t test_subscriber_median ./subscriber_median
docker build -t test_subscriber_sum ./subscriber_sum
