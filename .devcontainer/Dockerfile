# It builds on a pre-built Python-optimized Dev Container from Microsoft and includes the azd tool. 
#Your own file could start from any Docker image that includes Python. 
#However, you will want the final command in the file that installs a PostgreSQL client.

FROM mcr.microsoft.com/vscode/devcontainers/python:0-3

RUN curl -fsSL https://aka.ms/install-azd.sh | bash

ENV PYTHONUNBUFFERED 1

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends postgresql-client