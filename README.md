# Covid-19 real time feed to Confluent Cloud

## Steps

```bash
docker run -it -v $PWD:/project python:3 bash
pip3 install requests
pip3 install confluent_kafka
python3 /project/producer.py
```
