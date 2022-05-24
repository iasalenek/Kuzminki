FROM ubuntu:20.04

LABEL Description="Dockerised Simulation of Urban MObility(SUMO)"

ENV DEBIAN_FRONTEND noninteractive
ENV LIBSUMO_AS_TRACI 1
ENV SUMO_HOME /usr/share/sumo

# software-properties-common для последней версии SUMO
RUN apt-get update && apt-get install -y software-properties-common

# Python, SUMO и зависимости
RUN add-apt-repository ppa:sumo/stable \
    && apt-get -qq install \
    wget \
    g++ \
    make \
    git \
    python3-pip \
    python3.10 \
    sumo sumo-tools sumo-doc

# Библиотеки
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Модель
COPY nets nets

# Запуск внутри контейнера
CMD ["python3", "nets/Program1/my_QL.py"]



