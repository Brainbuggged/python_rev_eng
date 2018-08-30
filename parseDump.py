import mmap 
import argparse
import os
import sys
import pickle
import datetime as DT
import time
from lxml import etree


main_file = open("/home/brainbugged/Загрузки/prj/myReport.txt", 'r','utf-16')
listofPackages=[]
badInternet="android.permission.INTERNET"
badSmsSending="android.permission.SEND_SMS"
badSmsReceiving="android.permission.RECEIVE_SMS"
badReadingContacts="android.permission.READ_CONTACTS"



checkedList=[]
uncheckedList=[]
listofbads=[badInternet,badReadingContacts,badSmsReceiving,badSmsSending]



def parsePackagesFromBinary():
    maps =mmap.mmap(optional_file.fileno(),length=1024*1024*1024, offset=1536*1024*1024,access=mmap.ACCESS_READ)
    #looping here
    startPos=0
    while True:
    		number=maps.find("<package name=",startPos)
    		try:
    			maps.seek(number)
    		except:
    			break
    		anotherNumber= maps.find("</package>")
    		diff= anotherNumber+10-number
    		startPos=anotherNumber+10
    		try:
    			root= etree.fromstring(maps.read(diff))
    			for item in root.getchildren():
    				if item.tag=='perms' and root.get('name') not in seen:
    					seen.append(root.get('name'))
    					if doCompare(root.get('name')+"\n")==False:
    						uncheckedList.append( "\n" + str(DT.datetime.utcfromtimestamp(float(int(root.get('it'), 16))/1e3))+ "\n")
    						for nextitem in item.getchildren():
    							if nextitem.tag=='item':
    								uncheckedList.append( "\n" + str(nextitem.get('name')))
    							if nextitem.get('name') in listofbads:
    							    uncheckedList.append( "                    POTENTIAL WARNING !!!")   
    						for myItem in root.getchildren():
    							if myItem.tag=='sigs':
    								for sigItem in myItem.getchildren():
    									if sigItem.tag=='cert':
    										uncheckedList.append( "\n\n\n CERTIFICATE:   \n" + str(sigItem.get('key')))			   	 		
    					else:
    						checkedList.append( "\n" + str(DT.datetime.utcfromtimestamp(float(int(root.get('it'), 16))/1e3))+ "\n")
    						for nextitem in item.getchildren():
    							if nextitem.tag=='item':
    								checkedList.append( "\n" + str(nextitem.get('name'))) 
    						for myItem in root.getchildren():
    							if myItem.tag=='sigs':
    								for sigItem in myItem.getchildren():
    									if sigItem.tag=='cert':
    										checkedList.append( "\n\n\n CERTIFICATE:   \n" + str(sigItem.get('key')))			   	    						
    		except Exception as err:
    			print(err)
    	

def doCompare(item):
	if item in listofPackages:
		checkedList.append("\n\n\nCHECKED  \n" + item)	
		return True		
	else:
		uncheckedList.append("\n\n\n" + item + "\n" )    
		return False		



def compareDocuments():
	for line in main_file.readlines():
		if 'permission' not in line:
			listofPackages.append(line)
		

def doWrite(list):
	for line in list:
		new_hard_file.write(line)



def p_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("FromPath", type = str, help = "Path to file for work")
    args = parser.parse_args()
    return args


    	
args = p_parser()
objectName = os.path.splitext(args.FromPath)[0] + os.path.splitext(args.FromPath)[1]    	
seen=[]
optional_file = open(objectName, 'rb')
new_hard_file = open("bestReport.txt",'w')     

    
	

          
compareDocuments()
parsePackagesFromBinary()
doWrite(checkedList)
new_hard_file.write("\n\n-----------------------------------------UNCHECKED PACKAGES-----------------------------------------\n\n")
doWrite(uncheckedList)


