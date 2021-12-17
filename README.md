# Minimal Ubuntu application images
Proof of concept creating builder and runner containers Ubuntu 20.04 as base.

This minimal Ubuntu runtime build takes inspiration from [Distroless](https://github.com/GoogleContainerTools/distroless).
It uses Ubuntu as base and Dockerfile to build containers. A minimal runtime
container is created by copying a minimal subset of packages that are
necessary for an application to run. This is done by using a multistage docker
build where the first stage creates a new root directory that is copied into
a scratch container.

The apt package system is used to resolve dependencies of a minimal set of
packages necessary to run the application. When all the necessary packages
have been found we list the contents of those packages and copy them over
to the new root directory.

Top-level packages and why we install them.
* base-files (basic filesystem structure)
* ca-certificates (bundles CA certificates necessary for verifying TLS connections)
* dumb-init (used as entrypoint to make sure the responsibilites of pid 1 are taken care of)
* netbase (information about network protocols)
* nodejs (application runtime)
* tzdata (timezone information)


## How is this different than using Alpine?
Differences from from building on Alpine:
* Uses glibc instead of musl
* No shell or package manager included in runtime application image, Apline includes busybox.
* Use same base distro and package versions for both building and running the application.


## How is it different than using Distroless?
Differences from building on Distroless:
* Uses Dockerfiles instead of Bazel.
* Uses Ubuntu instead of Debian.
* Contains manifest of all installed packages, it can be scanned by AWS ECR.


## Why Ubuntu as base?
* Is used widely in cloud deployments.
* Long Term Support images have 2 years of support and 5 years of security updates.
* Available on AWS ECR, built and published by Canonical.
* Canonical ship updates regularly and is generally quick with security fixes.


## Images sizes
The NodeJS binary itself is ~80 MiB.
* Alpine: 110 MiB
* Distroless: 116 MiB
* Ubuntu: 118 MiB
