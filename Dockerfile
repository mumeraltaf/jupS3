FROM quay.io/jupyter/datascience-notebook:lab-4.2.4


USER root

# Docker install
RUN apt-get update && apt-get install --no-install-recommends -y \
       apt-transport-https \
       ca-certificates \
       curl \
       gnupg-agent \
       software-properties-common
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN apt-key fingerprint 0EBFCD88

RUN add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable"
RUN apt-get update && apt-get install --no-install-recommends -y docker-ce docker-ce-cli containerd.io

#RUN sudo groupadd docker
RUN sudo usermod -aG docker $NB_USER

RUN jupyter labextension disable @jupyterlab/docmanager-extension:download \
    && jupyter labextension disable @jupyterlab/filebrowser-extension:download

RUN pip install -Iv jupS3==0.0.6 geopandas==1.0.1

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"
