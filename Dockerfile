FROM jupyter/datascience-notebook:latest

RUN conda install --quiet --yes \
    'pandas' \
    'boto3' \
 && conda clean --all -f -y


CMD ["start-notebook.sh", "--NotebookApp.token=''", "--NotebookApp.password=''"]

