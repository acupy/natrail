from station import Station
import time

start_time = time.time()
stations = Station.get_all_station()
for s in stations:
    print s
print 'number of stations: {0}'.format(len(stations))
print 'it took: {0}s'.format(time.time()-start_time)