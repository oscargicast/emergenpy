import urllib2
import socket
import re
from urllib2 import URLError, HTTPError
from lxml import html
from lxml import etree


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
        print '-' * 30
    except URLError, e:
        print e.reason
        print '-' * 30
    except socket.timeout, e:
        print "There was an error: %r" % e


tree = html.fromstring(response.read())
events = tree.xpath('//tr[@class="TextoContenido"]')
print len(events)

emergency = []
for event in events:
    item = etree.tostring(event, pretty_print=True)
    elem = event.xpath('.//div/text()')
    coordinates = event.xpath('.//img/@onclick')
    if elem:
        if coordinates:
            cc = re.findall("'([^']*)'", coordinates[0])
            lat = cc[0]
            lon = cc[1]
            state = cc[5]
            elem.append(state)
            elem.append(lat)
            elem.append(lon)
        for index, item in enumerate(elem):
            elem[index] = ' '.join(
                elem[index].replace(u'\xa0', '').strip().split()
            )
        emergency.append(elem)

print emergency
print len(emergency)

print response.info().get('date')
print response.info().get('content-length')

print '-' * 30
print 'finish operation'
