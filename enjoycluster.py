import pymongo, datetime, json, math
from sklearn import cluster, preprocessing

conn = pymongo.Connection()
db = conn['enjoy']
shifts = list(db['shifts'].find({}))


def timeFeature(time):
	midnight = datetime.datetime(time.year, time.month, time.day, 0, 0, 0)
	delta = time - midnight
	return delta.seconds

def travelTimeFeature(shift):
	delta = shift['b_time'] - shift['a_time']
	return delta.seconds


X_shifts = [[shift['a_lat'], shift['a_lon'], shift['b_lat'], shift['b_lon'], timeFeature(shift['a_time']), travelTimeFeature(shift)] for shift in shifts]


k = 3000 #int(math.sqrt(len(shifts)/2)) *2
k_means = cluster.KMeans(n_clusters=k)
k_means.fit(preprocessing.normalize(X_shifts, axis=1, copy=False))


observation_vectors = json.dumps(X_shifts)
cluster_labels = json.dumps([int(cluster) for cluster in k_means.labels_])

# export data to .js file used for display visualization
f = open('data.js','w')
f.write('var coords = '+ observation_vectors+';\r\n')
f.write('var clusters = '+ cluster_labels+';\r\n')
f.write('var colors = [];\r\n') #TODO generate dinamically k different colors!

f.close()
