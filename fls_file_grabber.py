#LIBRARIES USED
import subprocess
import os
import sys
import progressbar
import time
d = dict()

#PREVENTS FROM A DEADLOCK OR COMMAND EXECUTION FROM BAD FILE NAMES FOUND ON THE DISK.
def remove_bad_chars(a):
  a=a.replace(" ","\ ")
  a=a.replace("(","\(")
  a=a.replace(")","\)")
  a=a.replace("[","\[")
  a=a.replace("]","\]") 
  a=a.replace("{","\{")
  a=a.replace("}","\}")
  a=a.replace("*","\*")
  a=a.replace("$","\$")
  a=a.replace("-","\-")
  a=a.replace("+","\+")
  a=a.replace("=","\=")
  a=a.replace("%","\%")
  a=a.replace("&","\&")
  a=a.replace("!","\!")
  a=a.replace("@","\@")
  a=a.replace("#","\#")
  a=a.replace("^","\^")
  a=a.replace("`","\`")
  a=a.replace("~","\~")
  a=a.replace(":","\:")
  a=a.replace(";","\;")
  a=a.replace("|","\|")
  a=a.replace("?","\?")
  a=a.replace("<","\<")
  a=a.replace(">","\>")
  return a

  #SEGREGRATES USEFUL FILES FROM GARBAGE
def useful_files(fi,file_name,final_list,dir_name): 
  a = subprocess.check_output(["file","-b","-z","/root/Desktop/"+dir_name+"/"+file_name+"/"+fi])
  for j in final_list:
    if(a.startswith(j)):
      os.system("cp /root/Desktop/"+dir_name+"/"+file_name+"/"+fi+" /root/Desktop/"+dir_name+"/"+file_name+"/useful_files/"+fi)
  os.system("rm /root/Desktop/"+dir_name+"/"+file_name+"/"+fi)

def parse_filename(fil_name):
  fil_name=fil_name.split("/")
  fil=fil_name[len(fil_name)-1]
  return fil
  
  #GETS ALL VISIBLE FILES
def extract_visible_files(file_name,final_list,dir_name):
  location = "/dev/"+file_name
  d = {}
  try:
    n = subprocess.check_output(["fls","-u","-F","-r",location])
  except:
    return("Partition type for "+location+" unknown. Skipping.")
  else:
    n=n.split("\n")
    n.remove("")
    for i in n:    
      i=i.split(' ',1)
      tup = i[1].split('\t')
      if('.' in tup[1]):
        if '/' in tup[1]:
          tup[1]=parse_filename(tup[1])
        a=remove_bad_chars(tup[1])
        d[tup[0][:-1]]=a
      else:
        continue
    for i in d:
      os.system("icat "+location+" "+i+" > /root/Desktop/"+dir_name+"/"+file_name+"/"+d[i])
      useful_files(d[i],file_name,final_list,dir_name)
  
  #GETS ALL DELETED FILES
def extract_deleted_files(file_name,final_list,dir_name):
  location = "/dev/"+file_name
  d = {}
  try:
    n = subprocess.check_output(["fls","-u","-F","-r",location])
  except:
    return("Partition type for "+location+" unknown. Skipping.")
  else:
    n=n.split("\n")
    n.remove("")
    for i in n:    
      i=i.split(' ',1)
      tup = i[1].split('\t')
      if('.' in tup[1]):
        if '/' in tup[1]:
          tup[1]=parse_filename(tup[1])
        a=remove_bad_chars(tup[1])
        d[tup[0][:-1]]=a
      else:
        continue
    for i in d:
      os.system("icat "+location+" "+i+" > /root/Desktop/"+dir_name+"/"+file_name+"/"+d[i])
      useful_files(d[i],file_name,final_list,dir_name)
