import requests, json, datetime

key = "901db038817e40bc4789ce2fc1dde133"


def weekly():
    url = "https://api.darksky.net/forecast/" + key + "/40.730610,-73.935242?exclude=hourly,currently,minutely,alerts"
    #print url
    data = requests.get(url).json()
    data = data['daily']['data']
    #print data
    #for x in data:
      #  print datetime.datetime.fromtimestamp(x["time"]).strftime('%d')
    d = {datetime.datetime.fromtimestamp(x["time"]).strftime('%d') : {"min" : x["temperatureLow"], "max" : x["temperatureHigh"], 'desc' : x["icon"]} for x in data}
    #print d
    
    return d

weekly()
