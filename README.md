# JEP Visualiser

A little experiment to visualise the JDK releases and their constituent JEPs.

> Live demo available at https://jep-visualiser.herokuapp.com/

## Run it yourself?

Sure, you can just use the local run script:

```shell script
./scripts/run-locally.sh
```

Or, you can build and run a Docker container:

```shell script
docker build --tag jep-visualiser .
docker run -it -p 8000:8000 --name jep-visualiser jep-visualiser
```

You'll see a _TON_ of output the first time you run that Docker container. The data collection/transformation only runs on the first container start so subsequent starts will be much quicker.

If you want to trigger the data to be recollected _without_ re-running the contain you can just delete the file marker used to establish if the container has run before.

```shell script
docker exec -it jep-visualiser /bin/sh
rm CONTAINER_STARTED
```

## More details?

The local run script does a couple of things for you:

1. Creates a python virtual environment (with `virtualenv`)
2. Installs python dependencies (with `pip`)
3. Runs `scrapy` spiders to collect jdk and jep data
4. Transforms the jdk and jep data into a format `TimelineJS` can understand
5. Runs a simple HTTP server to serve `TimelineJS` visualisations
