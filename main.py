import urllib2
from urllib2 import URLError, HTTPError


url = 'http://www.bomberosperu.gob.pe/po_diario.asp'
headers = {'User-Agent': 'Mozilla 5.10'}
request = urllib2.Request(url, None, headers)

response = None

while response is None:
    try:
        response = urllib2.urlopen(request, timeout=2)
        print 'url is opened!'
    except HTTPError as e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
            print '-'*30
    except URLError, e:
        print e.reason
        print '-'*30

print response.info().get('date')
print response.info().get('content-length')
print 'finish operation'
