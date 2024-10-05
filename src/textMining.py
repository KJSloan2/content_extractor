import json
import numpy as np

fName_manifest = ".json"
#manifest_json = json.load(open("%s%s" % (r"02_output\manifests\\",fName_manifest),'r', encoding='cp1252')

with open("%s%s" % (r"output\manifests\\",fName_manifest), 'r') as json_file:
    manifest_json = json.load(json_file)

query_text = ["interview themes"]

for slideId, slideContent in manifest_json.items():
    for textId, textConent in slideContent["text"].items():
        if textConent["shape_top"] <= 4700000 and textConent["shape_left"] <= 10300000:
            text_joined = " ".join(textConent["text_no_stopwords"])
            print(text_joined)