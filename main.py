import urllib2
import socket
import re
import json
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

emergency = {}
for event in events:
    item = etree.tostring(event, pretty_print=True)
    elem = event.xpath('.//div/text()')
    state = event.xpath('.//div/font/text()')
    coordinates = event.xpath('.//img/@onclick')
    if elem:
        if state:
            elem.append(state[0])
        lat = None
        lng = None
        if coordinates:
            cc = re.findall("'([^']*)'", coordinates[0])
            lng = cc[0]
            lat = cc[1]
            elem.append(lat)
            elem.append(lng)
        for index, item in enumerate(elem):
            elem[index] = ' '.join(
                item.replace(u'\xa0', '').strip().split()
            )
        emergency[elem[1]] = {
            'order': elem[0],
            'datetime': elem[2],
            'address': elem[3],
            'district': elem[3],
            'event_type': elem[4],
            'status': elem[6],
            'unit': elem[5],
            'lat': lat,
            'lng': lng,
        }

result = json.dumps(emergency)
with open("result.json", "w") as f:
    f.write(result)

print '-' * 30
print 'response info ...'

print response.info().get('date')
print response.info().get('content-length')
print response.info()

print '-' * 30
print 'operation completed!'
