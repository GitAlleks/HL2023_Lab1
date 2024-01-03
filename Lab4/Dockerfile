FROM alpine

RUN apk add openjdk8-jdk

RUN apk add bash

RUN mkdir /opt/java

RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz -O /opt/hadoop.tar.gz

RUN tar -xvf /opt/hadoop.tar.gz -C /opt/

ENV JAVA_HOME=/usr/lib/jvm/default-jvm

ENV HADOOP_HOME=/opt/hadoop-3.3.6

ENV PATH=/opt/hadoop-3.3.6/bin:$PATH
