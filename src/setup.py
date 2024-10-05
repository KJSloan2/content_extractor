import os
from os import listdir
from os.path import isfile, join
import json

paths_ = {
	"00_resources":r"resources\\",
	"projectDir":r"",
	"content":{"main":None,"manifests":None,"images":None,"txt_files":None,"images_grouped":None,"images_thumbnails":None}
}
	
folders_ = list(listdir(paths_["projectDir"]))
if "content" not in folders_:
    path_content = "%s%s%s" % (paths_["projectDir"],"content","\\")
    paths_["content"]["main"] = path_content
    os.mkdir(path_content)
    for sf in ["manifest","images","txt_files","images_grouped","images_thumbnails"]:
        path_sf = "%s%s%s%s%s" % (paths_["projectDir"],"content","\\",sf,"\\")
        paths_["content"][sf] = path_sf
        os.mkdir(path_sf)

with open(str("%s%s" % (paths_["00_resources"],"paths.json")), "w", encoding='utf-8') as json_paths:
	json_paths.write(json.dumps(paths_, indent=4, ensure_ascii=False))
	
print("DONE")