from lxml import etree
import argparse


def parseXML(xmlFile):
    with open(xmlFile) as fobj:
        xml = fobj.read()
    root = etree.fromstring(xml)
    for appt in root.getchildren():
            if  appt.tag=="uses-permission":
                 parseConstant1("FirstConst.xml",appt.get('{http://schemas.android.com/apk/res/android}name'))   

def parseConstant1(xmlFile, statement):
    with open(xmlFile) as fobj:
        xml = fobj.read()
    
    root = etree.fromstring(xml)
    for appt in root.getchildren():
        if appt.tag=="permission":
            if appt.get('{http://schemas.android.com/apk/res/android}name')==statement:
                 parseConstant2("SecondConst.xml",appt.get('{http://schemas.android.com/apk/res/android}label'))
    writeList(listOfStates)   


def parseConstant2(xmlFile,statement):
    newStatement= statement[8:]
    with open(xmlFile) as fobj:
        xml = fobj.read()
    root = etree.fromstring(xml)
    for appt in root.getchildren():
         if(appt.get('name')==newStatement):
             print(appt.text)
             listOfStates.append( "\n" + appt.text.encode('utf-8').strip())
    

def writeList(list):
    my_file = open("some.txt", 'w')
    
    for item in list:
        my_file.write(item)

    my_file.close()




listOfStates=[]
parseXML("AndroidManifest.xml")






        




