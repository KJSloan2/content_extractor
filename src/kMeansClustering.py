import json
import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans

paths_ = json.load(open("%s%s" % ("resources\\","paths.json")))
#data_ = json.loads(open(r"\\dfw-01-data01\Design$\Hugo\01_Computational Tools\03_harvester\02_output\imageStats.json"))
with open(r"output\imageStats_cleaned.json", 'r') as data_:
    data_string = data_.read()
imageStats_ = json.loads(data_string)

shuttleFIles = False
imPoints_ = []
imColors_ = []
imPaths_ = []
imIds_ = []
n = 1

for imKey,imStats in imageStats_.items():
    coords = imStats["coords"]
    color = imStats["color"]
    #a.append(imStats["path"])
    imPoints_.append([
        float(coords[0])*n,
        float(coords[1])*n,
        float(coords[2])*n
        ])
    #c.append((color[0],color[1],color[2]))
    imPaths_.append(imStats["path"])
    imIds_.append(imKey)

imPoints_ = np.array(imPoints_)
n_clusters = 25
# Perform K-means clustering
kmeans = KMeans(n_clusters=n_clusters)
kmeans.fit(imPoints_)
labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_
print(cluster_centers)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

if shuttleFIles == True:
    for label in list(dict.fromkeys(labels)):
        #labelCount = [i for i, val in enumerate(labels) if val == label]
        os.mkdir("%s%s" % (paths_["content"]["images_grouped"],label))

for i in range(len(labels)):
    pt = imPoints_[i]
    label = labels[i]
    path_source = imPaths_[i]
    imId = imIds_[i]
    imageStats_[imId]["group"] = str(label)
    if shuttleFIles == True:
        shutil.copy(path_source, "%s%s%s%s%s" % (paths_["content"]["images_grouped"],"\\",label,"\\",imId+".jpg"))

for i in range(n_clusters):
    cluster_points = imPoints_[labels == i]
    ax.scatter(cluster_points[:, 0], cluster_points[:, 1], cluster_points[:, 2])

with open(str(
	"%s%s" % (r"output\\","imageStats_custered.json")
	), "w", encoding='utf-8') as json_imageStats:
	json_imageStats.write(json.dumps(imageStats_, indent=4, ensure_ascii=False))

ax.scatter(cluster_centers[:, 0], cluster_centers[:, 1], cluster_centers[:, 2], c='black', marker='x', s=200, label='Cluster Centers')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Image Similarity - Clustered')
ax.legend()

plt.show()
print("DONE")