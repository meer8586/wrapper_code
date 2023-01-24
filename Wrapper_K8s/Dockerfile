FROM ubuntu:20.04
ENV USER root
WORKDIR /
COPY . .
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get install -y python3.8
RUN ln -s /usr/bin/python3.8 /usr/bin/python

RUN apt-get update && apt-get install -y python3-pip && apt-get -y install sudo && apt-get install -y wget && apt-get install -y apt-utils && apt-get install -y curl

RUN pip install -r requirement.txt

#ENV COUNT=""
#ARG COUNT

ENTRYPOINT ["python", "-m", "app"]
#CMD ["${COUNT}"]
CMD [""]
