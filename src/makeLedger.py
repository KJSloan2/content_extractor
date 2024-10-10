import os
from os import listdir
from os.path import isfile, join
import json
import datetime
from datetime import datetime, timezone
######################################################################################
paths_ = json.load(open("%s%s" % (r"resources/","paths.json")))
######################################################################################
def format_number(number):
    number_str = str(number)
    num_zeros = 5 - len(number_str)
    num_zeros = min(num_zeros, 3)
    formatted_number = '0' * num_zeros + number_str
    return formatted_number
######################################################################################
files_ = [f for f in listdir(r"data/") if isfile(join(r"data/", f))]
ledger_ = {}
id = 0
for f in files_:
	parse_f  = f.split(".")
	if parse_f[-1] in ["pptx","docx"]:
		f_path =  "%s%s" % (r"data/",f)
		f_stats = os.stat(f_path)
		print(f_stats)
		f_size = f_stats.st_size
		f_created = f_stats.st_ctime
		f_modified = f_stats.st_mtime
		f_cretaed_formated = datetime.fromtimestamp(f_stats.st_ctime, tz=timezone.utc)
		f_modified_formated = datetime.fromtimestamp(f_stats.st_mtime, tz=timezone.utc)
		f_modified_mdy = f_modified_formated.strftime("%m/%d/%Y")
		split_fMod_mdy = f_modified_mdy.split("/")
		f_lastAccess_formated = datetime.fromtimestamp(f_stats.st_atime, tz=timezone.utc)
		ledger_ [format_number(id)] = {
			"name": parse_f[0],
		    "ext":parse_f[-1],
			"size":f_size,
		    "created_mdy":f_cretaed_formated.strftime("%m/%d/%Y"),
		    "modified_mdy":f_modified_formated.strftime("%m/%d/%Y"),
		    "last_accessed_mdy":f_lastAccess_formated.strftime("%m/%d/%Y"),
			}
	id+=1
######################################################################################
with open(str(
	"%s%s" % (r"resources/","ledger.json")
	), "w", encoding='utf-8') as json_manifest:
	json_manifest.write(json.dumps(ledger_, indent=4, ensure_ascii=False))

		