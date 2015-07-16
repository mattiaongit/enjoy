import json, requests, pymongo, datetime

class Enjoy:

    def __init__(self):

        self.endpoint = 'https://enjoy.eni.com'

        self.api = {
            'vehicles': self.endpoint+'/get_vetture'
            }

        self.sleeptime = 0.5

        connection = pymongo.Connection()
        self.db = connection['enjoy']
        self.vehicles = self.db['vehicles']
        self.shifts = self.db['shifts']


    def get_vehicles(self):
        response = None
        backoff = 20
        while response == None:
            try:
                response = json.loads(requests.get(self.api['vehicles']).text)
            except Exception:
                print "Somenthing went wrong with the requests, retrying in {0} seconds.".format(backoff)
                time.sleep(backoff)
                backoff *= 1.2
                continue

        return response

    def update(self):
        vehicles_data = self.get_vehicles()

        for _vehicle in vehicles_data:
            vehicle = {
                '_id': _vehicle['car_plate'],
                'lat': _vehicle['lat'],
                'lon': _vehicle['lon'],
                'time': datetime.datetime.now()
            }

            self.vehicles.save(vehicle)
            _vehicle = self.vehicles.find({'_id': _vehicle['car_plate']})

            if vehicle['lat'] != _vehicle['lat'] and vehicle['lon'] != _vehicle['lon']:
                print "shift!"
                shift = {
                    'plate': vehicle['plate'],
                    'a_lat': _vechile['lat'],
                    'a_lon': _vehicle['lon'],
                    'b_lat': vehicle['lat'],
                    'b_lon': vehicle['lon']
                }

                self.shifts.insert(shift)

    def observe(self):
        while(True):
            self.update()
            time.sleep(5)
