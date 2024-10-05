import os
from os import listdir
from os.path import isfile, join
import zipfile
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import random
######################################################################################
######################################################################################
paths_ = json.load(open("%s%s" % ("resources\\","paths.json")))

def calc_color_moments(image):
	# Convert image to the Lab color space
	#lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
	#b_channel,l_channel, a_channel = cv2.split(lab_image)
	b_channel, g_channel, r_channel = cv2.split(image)
	# Calculate moments for each channel
	b_mean = np.mean(b_channel)
	g_mean = np.mean(g_channel)
	r_mean = np.mean(r_channel)
	b_std = np.std(b_channel)
	g_std = np.std(g_channel)
	r_std = np.std(r_channel)
	b_skew = np.mean(((b_channel - b_mean) / b_std) ** 3)
	g_skew = np.mean(((g_channel - g_mean) / g_std) ** 3)
	r_skew = np.mean(((r_channel - r_mean) / r_std) ** 3)
	b_kurt = (np.mean((b_channel - b_mean)**4)) / b_std**4
	g_kurt = (np.mean((g_channel - g_mean)**4)) / g_std**4
	r_kurt = (np.mean((r_channel - r_mean)**4)) / r_std**4
	r_var = np.var(r_channel)
	b_var = np.var(b_channel)
	g_var = np.var(g_channel)
	return b_mean, g_mean, r_mean, b_std, g_std, r_std, b_skew, g_skew, r_skew, b_kurt, g_kurt, r_kurt,r_var, b_var, g_var;

def calc_midpoint(point1, point2, point3):
	x_mid = round(((point1[0] + point2[0] + point3[0]) / 3),5)
	y_mid = round(((point1[1] + point2[1] + point3[1]) / 3),5)
	z_mid = round(((point1[2] + point2[2] + point3[2]) / 3),5)
	return [x_mid, y_mid, z_mid]

def normailize_val(val,d_min,d_max):
	return round(((val-d_min)/(d_max-d_min)),4)

def has_nan(lst):
    for item in lst:
        if isinstance(item, (float, int)) and math.isnan(item):
            return True
    return False
######################################################################################
ledger_ = json.load(open(r"output\ledger.json"))

imageStats_ = {}
poolData_ = {"mean":[],"std":[],"skew":[],"kurt":[],"var":[]}
files_ = [f for f in listdir(paths_["content"]["images"]) if isfile(join(paths_["content"]["images"], f))]
files_random = list(map(lambda idx: files_[idx],[random.randint(0, len(files_)) for _ in range(len(files_))]))
for f in files_random:
	parse_f  = f.split(".")
	if parse_f[-1] == "jpg":
		date_modified = ledger_[str(parse_f[0].split("_")[1])]["modified_mdy"]
		impath =  "%s%s" % (paths_["content"]["images"],f)
		image = cv2.imread(impath)

		try:
			print(parse_f[0])
			b_mean, g_mean, r_mean, b_std, g_std, r_std, b_skew, g_skew, r_skew, b_kurt, g_kurt, r_kurt, r_var, b_var, g_var = calc_color_moments(image)

			'''print(f"L-channel: Mean={l_mean:.2f}, Std={l_std:.2f}, Skewness={l_skewness:.2f}")
			print(f"A-channel: Mean={a_mean:.2f}, Std={a_std:.2f}, Skewness={a_skewness:.2f}")
			print(f"B-channel: Mean={b_mean:.2f}, Std={b_std:.2f}, Skewness={b_skewness:.2f}")'''

			moments_ = [[b_mean,g_mean,r_mean],[b_std, g_std, r_std],[b_skew, g_skew, r_skew],[b_kurt, g_kurt, r_kurt],[r_var, b_var, g_var]]
			for mKey,mLst in zip(list(poolData_.keys()),moments_):
				for v in mLst:
					poolData_[mKey].append(v)

			imHeight, imWidth, imChannels = image.shape
			imageStats_[parse_f[0]] = {
				"b_channel":{
					"mean": round((b_mean),3),
					"std": round((b_std),3),
					"skew": round((b_skew),3),
					"kurt": round((b_kurt),3),
					"var":round((b_var),3),
					"mean_norm":None,
					"std_norm":None,
					"skew_norm":None,
					"kurt_norm":None,
					"var_norm":None
				},
				"g_channel":{
					"mean": round((g_mean),3),
					"std": round((g_std),3),
					"skew": round((g_skew),3),
					"kurt": round((g_kurt),3),
					"var":round((g_var),3),
					"mean_norm":None,
					"std_norm":None,
					"skew_norm":None,
					"kurt_norm":None,
					"var_norm":None
				},
				"r_channel":{
					"mean": round((r_mean),3),
					"std": round((r_std),3),
					"skew": round((r_skew),3),
					"kurt": round((r_kurt),3),
					"var":round((r_var),3),
					"mean_norm":None,
					"std_norm":None,
					"skew_norm":None,
					"kurt_norm":None,
					"var_norm":None
				},
				"coords":[],
				"color":[],
				"path":impath,
				"group":None,
				"source_date_modified":date_modified,
				"images_match":[],
				"width":imHeight,
				"height":imWidth
			}
		except Exception as e:
			print(e)
			pass
		
######################################################################################
min_mean = min(poolData_["mean"])
max_mean = max(poolData_["mean"])
min_std = min(poolData_["std"])
max_std = max(poolData_["std"])
min_skew = min(poolData_["skew"])
max_skew = max(poolData_["skew"])
min_kurt = min(poolData_["kurt"])
max_kurt = max(poolData_["kurt"])
min_var = min(poolData_["var"])
max_var = max(poolData_["var"])
######################################################################################
for isKey,imObj in imageStats_.items():
	for channelKey in ["b_channel","g_channel","r_channel"]:
		channelStats = imObj[channelKey]
		norm_std = normailize_val(channelStats["std"],min_std,max_std)
		norm_skew = normailize_val(channelStats["skew"],min_skew,max_skew)
		imObj[channelKey]["mean_norm"] = round((normailize_val(channelStats["mean"],min_mean,max_mean)),3)
		imObj[channelKey]["std_norm"] = round((normailize_val(channelStats["std"],min_std,max_std)),3)
		imObj[channelKey]["skew_norm"] = round((normailize_val(channelStats["skew"],min_skew,max_skew)),3)
		imObj[channelKey]["kurt_norm"] = round((normailize_val(channelStats["kurt"],min_kurt,max_kurt)),3)
		imObj[channelKey]["var_norm"] = round((normailize_val(channelStats["var"],min_var,max_var)),3)
######################################################################################
toDel_ = []
for imKey,imObj in imageStats_.items():
	b_channel = imObj["b_channel"]
	g_channel = imObj["g_channel"]
	r_channel = imObj["r_channel"]

	pt1 = [b_channel["mean_norm"],b_channel["var_norm"],b_channel["skew_norm"]]
	pt2 = [g_channel["mean_norm"],g_channel["var_norm"],g_channel["skew_norm"]]
	pt3 = [r_channel["mean_norm"],r_channel["var_norm"],r_channel["skew_norm"]]

	'''pt1 = [b_channel["mean_norm"],b_channel["mean_norm"],b_channel["mean_norm"]]
	pt2 = [g_channel["skew_norm"],g_channel["skew_norm"],g_channel["skew_norm"]]
	pt3 = [r_channel["std_norm"],r_channel["std_norm"],r_channel["std_norm"]]
	pt4 = [r_channel["kurt_norm"],r_channel["kurt_norm"],r_channel["kurt_norm"]]'''

	remove = False
	for pt in [pt1,pt2,pt3]:
		if has_nan(pt) == True:
			remove = True
			toDel_.append(imKey)
			break
	if remove == False:
		pt0 = calc_midpoint(pt1,pt2,pt3)
		print(pt0)
		#imObj["plot"] = [pt0[0],pt0[1],pt0[2]]
		imObj["coords"] = pt0
		imObj["color"] = [r_channel["mean"],g_channel["mean"],b_channel["mean"]]

for imKey in toDel_:
    del imageStats_[imKey]
######################################################################################
with open(str(
	"%s%s" % (r"02_output\\","imageStats.json")
	), "w", encoding='utf-8') as json_manifest:
	json_manifest.write(json.dumps(imageStats_, indent=4, ensure_ascii=False))

print("DONE")
