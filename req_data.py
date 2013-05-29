import datetime
import requests

url = 'http://thevoice-on-itunes.appspot.com'

for i in range(64):
    day = datetime.date.today() - datetime.timedelta(days=i)
    print day
    res = requests.get('{}/{}'.format(url, day.strftime('%Y/%m/%d')))
    res = requests.get('{}/aus/{}'.format(url, day.strftime('%Y/%m/%d')))
