import json
import math
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans
from PIL import Image
######################################################################################
def calc_dist_3d(x1, y1, z1, x2, y2, z2):
    # Calculate the squared differences in x, y, and z coordinates
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    squared_distance = dx**2 + dy**2 + dz**2
    distance = squared_distance**0.5
    return distance

def show_image(image_path):
  image = mpimg.imread(image_path)
  imgplot = plt.imshow(image)
  plt.show()

def has_nan(lst):
    for item in lst:
        if isinstance(item, (float, int)) and math.isnan(item):
            return True
    return False

paths_ = json.load(open("%s%s" % ("00_resources\\","paths.json")))

with open(r"output\imageStats.json", 'r') as data_:
    data_string = data_.read()
imageStats_ = json.loads(data_string)

######################################################################################
toDel_ = []
toKeep_ = []
distMax = .001
for im1Key,im1Stats in imageStats_.items():
    #color = imStats["color"]
    for im2Key,im2Stats in imageStats_.items():
        if im2Key != im1Key:
            dist = calc_dist_3d(
                im1Stats["coords"][0],
                im1Stats["coords"][1],
                im1Stats["coords"][2],
                im2Stats["coords"][0],
                im2Stats["coords"][1],
                im2Stats["coords"][2],
            )
            if dist <= distMax:
                print(dist)
                if im1Key not in toDel_:
                    toKeep_.append(im1Key)
                if im2Key not in toKeep_:
                    if im2Key not in toDel_:
                        toDel_.append(im2Key)
                        im1Stats["images_match"].append(im2Key)
                #show_image(im1Stats["path"]), show_image(im2Stats["path"])
######################################################################################
for imKey in toDel_:
    if imKey not in toKeep_:
        del imageStats_[imKey]
######################################################################################
for imKey,imStats in imageStats_.items():
    imWidth = imStats["width"]
    imHeight = imStats["height"]
    max_dimension = 100
    if imWidth > imHeight:
        new_width = max_dimension
        new_height = int(imHeight * (max_dimension / imWidth))
    elif imWidth < imHeight:
        new_height = max_dimension
        new_width = int(imWidth * (max_dimension / imHeight))
    elif imWidth == imHeight:
        new_height = max_dimension
        new_width = max_dimension

    pil_image = Image.open(imStats["path"])
    imageResized = pil_image.resize((new_width,new_height))
    imageResized = imageResized.convert("RGB")
    imageResized.save(os.path.join(paths_["content"]["images_thumbnails"], f"{imKey}.jpg"))
######################################################################################
'''for imKey,imStats in imageStats_.items():
    images_ = []
    images_widths = []
    images_heights = []
    imStats["images_match"].append(imKey)
    tilesX = 10
    if len(imStats["images_match"]) >=3:
        for im in imStats["images_match"]:
            im = Image.open("%s%s%s" % (paths_["content"]["images"],im,".jpg"))
            images_.append("%s%s%s" % (paths_["content"]["images"],im,".jpg"))
            images_widths.append(im.width)
            images_heights.append(im.height)

        canvas_width = int(max(images_widths)*.25)
        canvas_height = int(sum(images_heights)*.25)

        # Create a new blank canvas
        canvas = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))

        # Paste the images onto the canvas
        y_offset = 0
        for imPath,imHeight,imWidth in zip(images_,images_heights,images_widths):
            im = Image.open(imPath)
            imResized = im.resize((int(imWidth*.25),int(imHeight*.25)))
            canvas.paste(imResized, (0, y_offset))
            y_offset += imHeight

        # Save the canvas as a new JPEG image
        canvas.save("%s%s%s" % (r"02_output\\",imKey,".jpg"))'''
######################################################################################
with open(str(
	"%s%s" % (r"output\\","imageStats_cleaned.json")
	), "w", encoding='utf-8') as json_imageStats:
	json_imageStats.write(json.dumps(imageStats_, indent=4, ensure_ascii=False))
######################################################################################