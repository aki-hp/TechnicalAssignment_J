#
# Ubuntu Dockerfile for ROMS task
#
# edited from https://github.com/dockerfile/ubuntu
#

# Pull base image.
FROM ubuntu:latest

# Install.
RUN \
  apt update && \
  apt upgrade -y && \
  apt install -y build-essential && \
  apt install -y software-properties-common && \
  apt install -y byobu curl git htop man unzip vim wget

RUN apt install -y python3
RUN apt install -y python3-pip
RUN apt install -y git
RUN apt install -y libgl1-mesa-dev
RUN pip install opencv-python
RUN pip install matplotlib

# For good measures, install Tensorflow
# RUN pip install tensorflow

# Set environment variables.
ENV HOME /root

# Define working directory.
WORKDIR /root
COPY ./necessaryFiles ./necessaryFiles

# Define default command.
CMD tail -f /dev/null