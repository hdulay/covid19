import requests
import json
import time
from confluent_kafka import Producer

def delivery_report(self, err = None, msg = None):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def send(p, js, topic):
    # Trigger any available delivery report callbacks from previous produce() calls
    p.poll(0)

    # Generate Key
    key = "{country}-{state}".format(country=js['country'], state=js['state'])

    # json
    value = json.dumps(js)

    # Asynchronously produce a message, the delivery report callback
    # will be triggered from poll() above, or flush() below, when the message has
    # been successfully delivered or failed permanently.
    p.produce(topic=topic, value=value.encode('utf-8'), callback=delivery_report, key=key)

    # Wait for any outstanding messages to be delivered and delivery report
    # callbacks to be triggered.
    p.flush()

def poll(url, topic, p):
    response = requests.get(url)
    results = json.loads(response.text)
    
    for j in results:
        send(p, j, topic)

def main():
    config_file = '/project/config.json'
    url = 'https://health-api.com/api/v1/covid-19/all'
    topic = 'covid19'
    with open(config_file) as f:
        config = json.load(f)
    p = Producer(config)

    while True:
        poll(url, topic, p)
        time.sleep(10)
  
if __name__== "__main__":
    main()