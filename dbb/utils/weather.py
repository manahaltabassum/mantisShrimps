import requests, json, datetime
from os import path

#g = path.dirname(__file__)
#print g

key = open('data/api.txt', 'r').read()


def weekly():
    url = "https://api.darksky.net/forecast/" + key + "/40.730610,-73.935242?exclude=hourly,currently,minutely,alerts"
    #print url
    data = requests.get(url).json()
    data = data['daily']['data']
    #print data
    #for x in data:
      #  print datetime.datetime.fromtimestamp(x["time"]).strftime('%d')
    d = {datetime.datetime.fromtimestamp(x["time"]).strftime('%d') :
         {"min" : int(x["temperatureLow"]),
          "max" : int(x["temperatureHigh"]),
          'desc' : x["icon"].replace("-", " ").title()}
         for x in data
         }
    keys = sorted(d.keys())
    print keys
    
    #print d
    return [keys, d]

weekly()
