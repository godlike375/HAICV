import requests
import logging




def setup():
    logging.basicConfig(
       filename='app.log',
       filemode='w',
       format='%(funcName)s-%(levelname)s-%(message)s'
    )

def send_counters(rooms, link='http://localhost:8080/set.php'):
    counters = {}
    for i in rooms:
        counters[i.name] = i.total
    print(counters)
    try:
        res = requests.get(link, params=counters)
    except requests.ConnectionError:
        logging.warning('Connection failed!')



#send_counters(100, 200, 3)