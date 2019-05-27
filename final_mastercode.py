#LIBRARIES USED
import subprocess
import os
import sys
import progressbar
import time
import bulk_extract as be
import fls_file_grabber as fl

#DOC RELATED STRUCTS USED TO EXTRACT THE SPECIFIC DOCUMENTS OUT
doc_file = ["Microsoft Word","PDF","Microsoft OOXML","Microsoft Excel","XML","ASCII text"] #DOCUMENT TYPES
pic_file = ["PNG","JPEG","PC Bitmap","GIF","GIMP","JFIF"] #PICTURE TYPES
media_file = ["MPEG","Apple QuickTime"] #MEDIA TYPES

'''
THE DOCUMENT TYPES DEFINED ABOVE CAN BE MODIFIED TO READ MORE TYPES, AS A DEMONSTRATION I HAVE USED A LIMITED NUMBER OF THEM
'''
def clean_input(a): #CLEANS INPUT
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
'''
THE CLEAN_INPUT FUNCTION IS RESPONSIBLE FOR CLEANING USER INPUT THAT IS GIVEN TO THE PROGRAM TO PREVENT ANY
 UNNECESSARY BREAKS IN CODE OR COMMAND INJECTIONS via BAD CHARACTERS.
'''
#Disk Identifier
'''
THIS FUNCTION IS USED TO IDENTIFY THE DISKS ON THIS SYSTEM WITH THE HELP OF LSBLK. I HAVE MADE NOTE TO DISPLAY
 ONLY PARTITIONS ON THE SYSTEM.
'''
def disk_identify():
  partition_list = [] #PARTITION LIST DEFINITION
  disk_list = subprocess.check_output("lsblk | grep part",shell=True)
  disk_list= disk_list.split("\n")
  for i in disk_list[:-1]:
    i = i.split()
    if(len(i)==7): #Removing disk entries
      continue
    else:
      partition_list.append(i[0].decode('utf8').encode('ascii', errors='ignore')) # ADDING THE PARTITION NAMES TO THE LIST
  return partition_list

# Bulk Extract
'''
CALLS THE BULK_EXTRACT.py PROGRAM TO GENERATE A REPORT OF THE DISK BEING ANALYZED.
THE OPERAATIONS IN THIS FUNCTION INCLUDE:
1) SELECT THE DISK.
2) MOUNTING THE DISK IN READONLY
3) CALLING BULK_EXTRACT.py TO GENERATE THE BULK EXTRACTOR REPORT.
'''
def bulk_extract():
#PROGRESSBAR
  bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('#', '[', ']'), ' ', progressbar.Percentage()])
  
  print("\n\n[Bulk Extracting]\n\n")
  dir_name = raw_input("Enter a Directory name you want to store the Bulk Extract in:\n\n")
  dir_name = clean_input(dir_name)
  os.system("mkdir /root/Desktop/"+dir_name)
  print("\nDirectory /root/Desktop/"+dir_name+" successfully created!\n")
  print("\n\nChoose a Method to Extract: \n\n")
  print("1.Manual (Choose the Disks Yourself!)")
  print("2.Automated (Get Everything! Fails if Space is insufficient!)")
  part_choice = int(raw_input("\nEnter Choice:\n"))
  if(part_choice == 1):
    print("\n\n[Partitions found on the Computer]\n\n")
    disk_list = subprocess.check_output("lsblk | grep part",shell=True)
    print("\n"+disk_list+"\n")
    print("\n\n[NOTE: Mounted Partitions may not be recognized!]\n\n")
    partition_list = raw_input("Enter a CSV list of Partition Names (Eg: sda,sda1): \n")
    partition_list = partition_list.split(",")
    part_list = disk_identify()
    bar.start()
    for i in partition_list:
      if(i in part_list): #CHECKS THE USER FOR VALID ENTRIES
        mount_name = "/media/"+i
        os.system("mkdir "+mount_name)
        os.system("mount -r /dev/"+i+" "+mount_name)
        be.bulk_extractor(i,dir_name)
        os.system("umount "+mount_name)
        os.system("rm -R "+mount_name)
      else:
        print("\n\nDisk "+i+" Mentioned not Found!\n\n")
        continue
    bar.finish()
    print("\n\n[User Requested File Extraction Complete.]\n\n")

  elif(part_choice == 2):
    partition_list = disk_identify()
    print("\nFound "+str(len(partition_list))+" Partition/s")
    bar.start()
    for i in partition_list:
      mount_name = "/media/"+i
      os.system("mkdir "+mount_name)
      os.system("mount -r /dev/"+i+" "+mount_name)
      be.bulk_extractor(i,dir_name)
      os.system("umount "+mount_name)
      os.system("rm -R "+mount_name)
    bar.finish()
    print("\n\n[User Requested File Extraction Complete.]\n\n")

  else:
    print("\n\n[Wrong Choice! Exiting!]\n\n")
    main()

#File Grabber
'''
CALLS THE FLS_FILE_GRABBER.py PROGRAM TO CARVE FILES OF A DISK.
THE OPERATIONS IN THIS FUNCTION INCLUDE:
1) SELECT THE DISK.
2) MOUNTING THE DISK IN READONLY
3) CALLING FLS_FILE_GRABBER.py TO CARVE FILES OFF A DISK MENTIONED IN STEP 1.
'''
def fls_file_grabber():
#PROGRESSBAR
  bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('#', '[', ']'), ' ', progressbar.Percentage()])
  print("\n\n[File Grabbing]\n\n")
  print("What kind of Files do you want to extract?\n\n")
  print("1. Documents")
  print("11. Pictures")
  print("111. Media Files (Music, Video)\n\n")
  file_choice = int(raw_input("Enter the choice or sum of choices: "))
  if(file_choice == 1):
    final_list = doc_file

  elif(file_choice == 11):
    final_list = pic_file

  elif(file_choice == 111):
    final_list = media_file

  elif(file_choice == 12):
    final_list = doc_file+pic_file

  elif(file_choice == 112):
    final_list = pic_file+media_file

  elif(file_choice == 122):
    final_list = doc_file+media_file

  elif(file_choice == 123):
    final_list = doc_file+pic_file+media_file
  else:
    print("\n\nBad Option. Goodbye\n\n")
    main()

  dir_name = raw_input("\n\nEnter a Directory name you want to store the Carved Files in...\n")
  dir_name = clean_input(dir_name) #CLEANS USER INPUT
  print("\n\nChoose a Method to Extract: \n\n")
  print("1.Manual (Choose the Disks Yourself!)")
  print("2.Automated (Get Everything! Fails if Space is insufficient!)")
  part_choice = int(raw_input("Enter Choice:\n"))
  if(part_choice == 1):
    os.system("mkdir /root/Desktop/"+dir_name)
    print("\n\nDirectory /root/Desktop/"+dir_name+" successfully created!\n")
    print("\n\n[Partitions found on the Computer]\n\n")
    disk_list = subprocess.check_output("lsblk | grep part",shell=True)
    print("\n"+disk_list+"\n")
    print("\n\n[NOTE: Mounted Partitions may not be recognized!]\n\n")
    partition_list = raw_input("\n\nEnter a CSV list of Partition Names (Eg: sda,sda1): \n")
    partition_list = partition_list.split(",")
    part_list = disk_identify()
    bar.start()
    for i in partition_list:
      if(i in part_list): #CHECKS FOR VALID USER ENTRIES
        os.system("mkdir /root/Desktop/"+dir_name+"/"+i)
        os.system("mkdir /root/Desktop/"+dir_name+"/"+i+"/useful_files")
        mount_name = "/media/"+i
        os.system("mkdir "+mount_name)
        os.system("mount -r /dev/"+i+" "+mount_name)
        fl.extract_visible_files(i,final_list,dir_name)
        fl.extract_deleted_files(i,final_list,dir_name)
        os.system("umount "+mount_name)
        os.system("rm -R "+mount_name)
    
      else:
        print("\n\nDisk "+i+" Mentioned not Found!\n\n")
        continue
    bar.finish()
    print("\n\n[Requested files stored in /root/Desktop/"+dir_name+"/useful_files. User Requested File Extraction Complete.]\n\n")
  elif(part_choice == 2):
    os.system("mkdir /root/Desktop/"+dir_name)
    os.system("mkdir /root/Desktop/"+dir_name+"/useful_files")
    print("\n\nDirectory /root/Desktop/"+dir_name+" successfully created!\n")
    partition_list = disk_identify()
    print("\nFound "+str(len(partition_list))+" Partition/s")
    bar.start()
    for i in partition_list:
      os.system("mkdir /root/Desktop/"+dir_name+"/"+i)
      os.system("mkdir /root/Desktop/"+dir_name+"/"+i+"/useful_files")
      mount_name = "/media/"+i
      os.system("mkdir "+mount_name)
      os.system("mount -r /dev/"+i+" "+mount_name)
      fl.extract_visible_files(i,final_list,dir_name)
      fl.extract_deleted_files(i,final_list,dir_name)
      os.system("umount "+mount_name)
      os.system("rm -R "+mount_name)
    bar.finish()
    print("\n\n[Requested files stored in /root/Desktop/"+dir_name+"/useful_files. User Requested File Extraction Complete.]\n\n")
  else:
    print("\n\n[Wrong Choice! Exiting!]\n\n")
    main()
    
'''
THE MAIN DRIVER PROGRAM THAT HELPS THE USER INTERACT WITH THE ABOVE CODE.
'''
def main():
  print("\n\nWelcome to the Automated File Disk Inspector!\n\n")
  print("Please specify the Type of operations you want to perform...\n\n")
  print("1.Bulk Extract Info")
  print("11.FLS File Grab")
  print("111.Exit")
  print("\nFor mutiple operations except [Exit] offcourse, please use the sum of the option numbers...\n")
  choice = int(raw_input("Enter your option here: \n"))
  #Progress Bar
  bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('#', '[', ']'), ' ', progressbar.Percentage()])

  if(choice == 1):
    bulk_extract()
    main()

  elif(choice == 11):
    fls_file_grabber()
    main()

  elif(choice == 12):
    fls_file_grabber()
    bulk_extract()
    main()

  elif(choice == 111):
    print("\n\nProgram Exit! Thank you for using Disk Inspector\n\n")
    exit()

  else:
    print("Bad OPTION. Shutting Down!")
    main()

main() #ONE LINE THAT DECIDES THE FATE OF THIS PROGRAM
