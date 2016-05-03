from station import Station

stations = Station.get_all_station()
for s in stations:
    print s
print 'number of stations: {0}'.format(len(stations))