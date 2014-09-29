import urllib
import urllib2


class Station(object):
    def __init__(self, abbrevation, name, latitude, longitude, postcode):
        self.abbrevation = abbrevation
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.postcode = postcode
         
    def __repr__(self, *args, **kwargs):
        return '{0}({1}, {2}) latitude: {3} / longitude {4}'.format(self.name, self.abbrevation, self.postcode, self.latitude, self.longitude)
 
base_url = 'http://ojp.nationalrail.co.uk/find/stationsDLRLU/'
 
urls = []
 
for i in range(97, 123):
    urls.append('{0}{1}'.format(base_url, chr(i))) 
 
stations = []
for url in urls:
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
             
    arr = eval(response.read())
 
    for station in filter(lambda i: i[0] != 'All Stations', arr):
        stations.append(Station(station[0], station[1], station[7], station[8], station[9]))

#############################################################################################################################################################

from HTMLParser import HTMLParser

class Ticket(object):
    def __init__(self, duration, change, fare):
        self.duration = duration
        self.change = change
        self.fare = fare
        
    def __repr__(self, *args, **kwargs):
        return '/'.join([self.duration,self.change,self.fare])

tix = []
class NatRailHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_dur = False
        self.in_chg = False
        self.in_fare = False
        
        self.is_new_ticket = True
        self.fare_was_processed_last = False
        
        self.actual_duration = ''
        self.actual_chage = ''
        self.actual_fare = ''
        
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'td' and 'dur' in attrs.get('class', ''):
            self.in_dur = True
        if tag == 'td' and 'chg' in attrs.get('class', ''):
            self.in_chg = True
        if tag == 'input' and 'outward.option' in attrs.get('name', ''):
            self.in_fare = True
            
    def handle_endtag(self, tag):
        if tag == 'td' and self.in_dur:
            self.in_dur = False
            
        if tag == 'td' and self.in_chg:
            self.in_chg = False
        
        if tag == 'label' and self.in_fare:
            self.in_fare = False
            self.fare_was_processed_last = True
    def handle_data(self, data):
        if self.in_dur:
            if self.fare_was_processed_last:
                tix.append(Ticket(self.actual_duration.replace(' ', '').replace('\n', '').replace('\t', ''), self.actual_chage.replace(' ', '').replace('\n', '').replace('\t', ''), self.actual_fare.replace(' ', '').replace(' ', '').replace('\n', '').replace('\t', '')))
                self.actual_duration = ''
                self.actual_chage = ''
                self.actual_fare = ''
                self.fare_was_processed_last = False
                
            self.actual_duration += data
        if self.in_chg:
            self.actual_chage += data
        if self.in_fare:
            self.actual_fare += data
            
    
from_station = 'London'
date = 'today'
time = '1900'
when = 'dep'

for station in stations:
    to_station = station.abbrevation
    planner_url = 'http://ojp.nationalrail.co.uk/service/timesandfares'
    planner_url = '/'.join([planner_url, from_station, to_station, date, time, when])
    #print planner_url
    req = urllib2.Request(planner_url)
    response = urllib2.urlopen(req)
    
    html = response.read()
    parser = NatRailHTMLParser()
    parser.feed(html.replace("</scr' + 'ipt>", "</scr>"))

    print station.name
    
    for t in tix:
        print t
    tix[:] = []
# for s in stations:
#     print s
# print 'number of stations: {0}'.format(len(stations))

