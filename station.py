import urllib2
from threads import NatrailThread

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

        threads = []
        stations = {}

        for i in range(97, 123):
            the_thread = NatrailThread(Station.__get_stations, chr(i), stations)
            the_thread.start()
            threads.append(the_thread)

        for the_thread in threads:
            the_thread.join()

        return sorted(stations.values(), key=lambda s: s.name)

    @staticmethod
    def __get_stations(station_name, stations):

        url = '{0}{1}'.format(URL, station_name)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)

        arr = eval(response.read())

        for station in filter(lambda i: i[0] != 'All Stations', arr):
            if station[8] and station[9]:
                stations[station[1]] = Station(station[0], station[1], station[7], station[8], station[9])
