FROM quay.io/jupyter/datascience-notebook:notebook-7.2.1

RUN jupyter labextension disable @jupyterlab/docmanager-extension:download \
    && jupyter labextension disable @jupyterlab/filebrowser-extension:download

RUN pip install -Iv jupS3==0.0.2