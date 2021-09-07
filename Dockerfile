# pull official base image
FROM continuumio/miniconda:latest

# set work directory
WORKDIR /code/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create environment
ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml

# activate environment
RUN echo "conda activate myvcf" > ~/.bashrc
ENV PATH /opt/conda/envs/myvcf/bin:$PATH

# copy project
COPY . /code/