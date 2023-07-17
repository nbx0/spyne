
---
output:
  html_document:
      keep_md: yes
---

<!-- README.md is generated from README.Rmd. Please edit that file -->



### Requirements

- Docker version >= 18
- Git version >= 2.21.0

### Steps to run spyne container

#### (1) Clone this respitory

```
git clone https://github.com/cdcgov/spyne/tree/container_init
``` 

#### (2) CD to `spyne` folder 

#### (3) Check out `container_init` branch

```
git checkout container_init 
```

#### (4) Pull down irma and dais-ribosome images

- From a docker registry

&emsp; **IRMA**: `docker pull public.ecr.aws/n3z8t4o2/irma:1.0.2p3` <br>
&emsp; **Dias-Ribosome**: `docker pull public.ecr.aws/n3z8t4o2/dais-ribosome:1.2.1`

#### (5) Run **irma** and **dais-ribosome** containers

&emsp; **IRMA**: `docker run -v /path/to/data:/data --name irma:1.0.2p3 -t -d public.ecr.aws/n3z8t4o2/irma:1.0.2p3` <br>
&emsp; **Dais-Ribosome**: `docker run -v /path/to/data:/data --name dais-ribosome:1.2.1 -t -d public.ecr.aws/n3z8t4o2/dais-ribosome:1.2.1`

**NOTE:** <br>
- Change __/path/to/data__ to your local directory where it contains all data files needed to feed into the `IRMA` and `Dais-ribosome` workflow. This directory is mounted to `/data` directory inside the container. <br>

#### (6) Build **spyne** image and run its container

__NOTE:__ In the `SC2-seq-spike` directory, there is a `Dockerfile` that contains a list of instructions and steps of how to build and run the `spyne` workflow.

**A. Build the development version**

- Using a build-arg

```
docker build -t spyne-dev:v1.0.0 --build-arg BUILD_STAGE=dev .
```

- Using a specific dockerfile for development stage (e.g. `Dockerfile.dev`)

```
docker build -t spyne-dev:v1.0.0 -f Dockerfile.dev .
```

**-t**: add a tag to an image such as the version of the application, e.g. *spyne-dev:v1.0.0* or *spyne-dev:latest* <br>
**`--`file, -f**: name of the Dockerfile <br>
**`--`build-arg**: set the build time variable for docker image. In this case, we want to build the **development** stage by setting build variable `BUILD_STAGE=dev`. <br>

_The image took approximately < 10 mins to build_

After the build is completed, you can check if the image is built successfully

```
docker images

REPOSITORY             TAG        IMAGE ID        CREATED        SIZE
spyne-dev      v1.0.0     2c22887402d3    2 hours ago    1.58GB
```

To run the `spyne-dev` container

```    
docker run -v /path/to/data:/data -v /path/to/spyne:/spyne -v /var/run/docker.sock:/var/run/docker.sock --name spyne-dev-1.0.0 -t -d spyne-dev:v1.0.0 
```

**NOTE:** <br>
- Change __/path/to/data__ to your local directory where it contains all data files needed to feed into the `spyne` workflow. This directory is mounted to `/data` directory inside the container. <br>
- Change __/path/to/spyne__ to your local `spyne` directory. This directory must contain all of the code base needed to build the `spyne` workflow. <br>
- **/var/run/docker.sock:/var/run/docker.sock** is used to connect the host's docker.socket to container's docker.socket where you can run a container inside of another container. <br>

**-t**: allocate a pseudo-tty <br>
**-d**: run the container in detached mode <br>
**-v**: mount code base and data files from host directory to container directory **[host_div]:[container_dir]**. By exposing the host directory to docker container, docker will be able to access data files within that mounted directory and use it to fire up the `spyne` workflow.  <br>
**`--`name**: give an identity to the container <br>

For more information about the Docker syntax, see [Docker run reference](https://docs.docker.com/engine/reference/run/)

To check if the container is built successfully

```
docker container ps


CONTAINER ID   IMAGE                        COMMAND        CREATED         STATUS        PORTS      NAMES
b37b6b19c4e8   spyne-dev:v1.0.0     "bash"         5 hours ago     Up 5 hours               spyne-dev-1.0.0
```

**B. Build the production version**

- By default

```
docker build -t spyne-prod:v1.0.0 .
```

- Using a specific dockerfile for production stage (e.g. `Dockerfile.prod`)

```
docker build -t spyne-prod:v1.0.0 -f Dockerfile.prod .
```

**-t**: add a tag to an image such as the version of the application, e.g. *spyne-prod:v1.0.0* or *spyne-prod:latest* <br>
**`--`file, -f**: name of the Dockerfile

_The image took approximately < 10 mins to build_

After the build is completed, you can check if the image is built successfully

```
docker images

REPOSITORY             TAG        IMAGE ID        CREATED        SIZE
spyne-prod     v1.0.0     c436f88dcd2f    2 hours ago    1.58GB
```

To run the `spyne-prod` container

```    
docker run -v /path/to/data:/data -v /var/run/docker.sock:/var/run/docker.sock --name spyne-prod-1.0.0 -t -d spyne-prod:v1.0.0 
```

**NOTE:** <br>
- Change __/path/to/data__ to your local directory where it contains all data files needed to feed into the `spyne` workflow. This directory is mounted to `/data` directory inside the container. <br>
- **/var/run/docker.sock:/var/run/docker.sock** is used to connect the host's docker.socket to container's docker.socket where you can run a container inside of another container. <br>

**-t**: allocate a pseudo-tty <br>
**-d**: run the container in detached mode <br>
**-v**: mount code base and data files from host directory to container directory **[host_div]:[container_dir]**. By exposing the host directory to docker container, docker will be able to access data files within that mounted directory and use it to fire up the `spyne` workflow.  <br>
**`--`name**: give an identity to the container <br>

For more information about the Docker syntax, see [Docker run reference]()

To check if the container is built successfully

```
docker container ps


CONTAINER ID   IMAGE                        COMMAND     CREATED        STATUS        PORTS      NAMES
475741fd9bc7   spyne-prod:v1.0.0    "bash"      5 hours ago    Up 5 hours               spyne-prod-1.0.0
```

#### (7) To execute snakemake pipeline inside **spyne-prod-1.0.0** container

```
docker exec -w /data spyne-prod-1.0.0 bash snake-kickoff <path/to/samplesheet.csv> <runpath> <experiment_type>
```

#### (8) To execute irma pipeline inside **irma-1.0.2p3** container

- FOR PAIRED-END

```
docker exec -w /data irma-1.0.2p3 IRMA <MODULE|MODULE-CONFIG> <R1.fastq.gz|R1.fastq> <R2.fastq.gz|R2.fastq> [path/to/]<sample_name>
```

- For SINGLE-END

```
docker exec -w /data irma-1.0.2p3 IRMA <MODULE|MODULE-CONFIG> <fastq|fastq.gz> [path/to/]<sample_name>
```

<br>

Any questions or issues? Please report them on our [github issues](https://github.com/cdcgov/spyne/issues)

<br>


