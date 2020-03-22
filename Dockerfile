FROM python:3

RUN pip3 install requests confluent_kafka
COPY . /project
CMD python3 /project/producer.py
