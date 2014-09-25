import urllib
import urllib2


# class Station(object):
#     def __init__(self, abbrevation, name, latitude, longitude, postcode):
#         self.abbrevation = abbrevation
#         self.name = name
#         self.latitude = latitude
#         self.longitude = longitude
#         self.postcode = postcode
#         
#     def __repr__(self, *args, **kwargs):
#         return '{0}({1}, {2}) latitude: {3} / longitude {4}'.format(self.name, self.abbrevation, self.postcode, self.latitude, self.longitude)
# 
# base_url = 'http://ojp.nationalrail.co.uk/find/stationsDLRLU/'
# 
# urls = []
# 
# for i in range(97, 123):
#     urls.append('{0}{1}'.format(base_url, chr(i))) 
# 
# stations = []
# for url in urls:
#     req = urllib2.Request(url)
#     response = urllib2.urlopen(req)
#             
#     arr = eval(response.read())
# 
#     for station in filter(lambda i: i[0] != 'All Stations', arr):
#         stations.append(Station(station[0], station[1], station[7], station[8], station[9]))

#############################################################################################################################################################

from HTMLParser import HTMLParser

class Ticket(object):
    def __init__(self, duration, change, fare):
        self.duration = duration
        self.change = change
        self.fare = fare

class NatRailHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_in_table = False
        self.is_in_row = False
        self.is_in_cell = False
        self.embedded_table_cnt = 0
        self.embedded_row_cnt = 0
        self.embedded_cell_cnt = 0
        
        self.processing_type = ''
        
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'table' and attrs.has_key('id') and attrs['id'] == 'oft':
            self.is_in_table = True
            print tag, dict(attrs)
        elif tag == 'table':
            self.embedded_table_cnt +=1
            
        if tag == 'tr' and self.is_in_table and attrs.has_key('class') and 'mtx' in attrs['class']:
            self.is_in_row = True
            print tag, attrs
        elif tag == 'tr':
            self.embedded_row_cnt +=1
        
        is_interesting_cell = (tag == 'td' and self.is_in_row)
        
        if is_interesting_cell:
            self.is_in_cell = True
            print tag, attrs
        elif tag == 'td':
            self.embedded_cell_cnt +=1
        
        
        is_interesting_cell = is_interesting_cell and attrs.has_key('class')
        
        if tag == 'span':
            print tag, attrs
        
        if tag == 'span' and self.is_in_cell and attrs['class'] == 'label-text':
            self.processing_type = 'fare'
        elif is_interesting_cell and 'dur' in attrs['class']:
            self.processing_type = 'dur'
        elif is_interesting_cell and 'chg' in attrs['class']:
            self.processing_type = 'chg'
        else:
            self.processing_type = ''
                        
    def handle_endtag(self, tag):
        if tag == 'table' and self.is_in_table and self.embedded_table_cnt == 0:
            self.is_in_table = False
        elif tag == 'table':
            self.embedded_table_cnt -=1
            
        if tag == 'tr' and  self.is_in_row and self.embedded_row_cnt == 0:
             self.is_in_row = False
        elif tag == 'tr':
            self.embedded_row_cnt -=1
        
        if tag == 'td' and self.is_in_cell and self.embedded_cell_cnt == 0:
            self.is_in_cell = False
        elif tag == 'td':
            self.embedded_cell_cnt -= 1

    def handle_data(self, data):
        if self.is_in_cell and self.processing_type in ('dur', 'chg', 'fare'):
            print self.processing_type, data

from_station = 'London'
to_station = 'Brighton'
date = 'today'
time = '1900'
when = 'dep'

# 'http://ojp.nationalrail.co.uk/service/timesandfares/LDY/BLE/today/1545/dep'
planner_url = 'http://ojp.nationalrail.co.uk/service/timesandfares'
planner_url = '/'.join([planner_url, from_station, to_station, date, time, when])
print planner_url
req = urllib2.Request(planner_url)
response = urllib2.urlopen(req)

html = response.read()
parser = NatRailHTMLParser()
parser.feed(html.replace("</scr' + 'ipt>", "</scr>"))

# for s in stations:
#     print s
# print 'number of stations: {0}'.format(len(stations))

