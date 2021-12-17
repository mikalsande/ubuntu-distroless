FROM ubuntu:20.04 as builder

# This is the builder image, we do not care very much about image layers and space optimization.
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y curl gpg lsb-release

# NodeJS version.
ENV VERSION=node_16.x

# Add NodeJS repo.
ENV KEYRING=/usr/share/keyrings/nodesource.gpg
RUN curl -fsSL https://deb.nodesource.com/gpgkey/nodesource.gpg.key | gpg --dearmor | tee "$KEYRING" >/dev/null
RUN gpg --no-default-keyring --keyring "$KEYRING" --list-keys
RUN echo "deb [signed-by=$KEYRING] https://deb.nodesource.com/$VERSION $(lsb_release -s -c) main" | tee /etc/apt/sources.list.d/nodesource.list
RUN echo "deb-src [signed-by=$KEYRING] https://deb.nodesource.com/$VERSION $(lsb_release -s -c) main" | tee -a /etc/apt/sources.list.d/nodesource.list

# Install NodeJS
RUN apt-get update -y
RUN apt-get install -y nodejs

# Enable package managers.
RUN corepack enable
