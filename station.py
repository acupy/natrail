import urllib2

URL = 'http://ojp.nationalrail.co.uk/find/stationsDLRLU/'

class Station(object):
    def __init__(self, abbrevation, name, latitude, longitude, postcode):
        self.abbrevation = abbrevation
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.postcode = postcode
         
    def __repr__(self, *args, **kwargs):
        return '{0}({1}, {2}) latitude: {3} / longitude {4}'.format(self.name,
                                                                    self.abbrevation,
                                                                    self.postcode,
                                                                    self.latitude,
                                                                    self.longitude)
    @staticmethod
    def get_all_station():

        urls = []

        for i in range(97, 123):
            urls.append('{0}{1}'.format(URL, chr(i)))

        stations = []
        for url in urls:
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)

            arr = eval(response.read())

            for station in filter(lambda i: i[0] != 'All Stations', arr):
                stations.append(Station(station[0], station[1], station[7], station[8], station[9]))

        return stations
