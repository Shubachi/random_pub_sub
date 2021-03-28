# random_pub_sub
This project contains 3 python applications where:
* A publisher publishes random integers to Redis
* A subscriber calculates the median over a period of time
* A subscriber calculates the sum over a period of time

# Assumptions
* Integers published are defined as a number between negative and positive int_max (2137483647)

# Setup
# Build the docker images
Execute build.sh to build the docker images for each

# Start Redis
```
docker run --name test_redis -d -p 6379:6379 redis
```

# Start the publisher
```
docker run -d --network="host" test_publisher
```

# Start the subscribers
In a different terminal for each command (so you can watch the output of each), run:
```
docker run --network="host" test_subscriber_median
docker run --network="host" test_subscriber_sum
```