#LIBRARIES USED
import subprocess
import os
import sys
import progressbar
import time

def bulk_extractor(file_name,dir_name):
  location = "/dev/"+file_name
  subprocess.call(["bulk_extractor", location, "-o", "/root/Desktop/"+dir_name+"/"+file_name])

