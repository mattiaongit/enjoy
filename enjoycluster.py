import pymongo, datetime, json, math
from sklearn import cluster

conn = pymongo.Connection()
db = conn['enjoy']
shifts = list(db['shifts'].find({}))


def timeFeature(time):
	midnight = datetime.datetime(time.year, time.month, time.day, 0, 0, 0)
	delta = time - midnight
	return delta.seconds


X_shifts = [[shift['a_lat'], shift['a_lon'], shift['b_lat'], shift['b_lon'], timeFeature(shift['a_time']) ] for shift in shifts]

k_means = cluster.KMeans(n_clusters=math.sqrt(len(shifts)/2))
k_means.fit(X_shifts)


observation_vectors = json.dumps(X_shifts)
cluster_labels = json.dumps([int(cluster) for cluster in k_means.labels_])

# export data to .js file used for display visualization
f = open('data.js','w')
f.write('var coords = '+ observation_vectors+';\r\n')
f.write('var clusters = '+ cluster_labels+';\r\n')
f.close()
