import os
import psutil
import json
from dicttoxml import dicttoxml
from zipfile import ZipFile
import xml.etree.ElementTree as ET

def get_disk_info():
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                continue
        usage = psutil.disk_usage(part.mountpoint)
        print(f"Name: {part.device}")
        print(f"Type: {part.opts}")
        print(f"File System: {part.fstype}")
        hdd = psutil.disk_usage(part.device)
        print("Size:")
        print(f"    Total: {int(hdd.total) / (2 ** 30)} GiB")
        print(f"    Free: {int(hdd.free) / (2 ** 30)} GiB")
        print("====================================\n")

def file():
    print("File:")
    text = input("Please enter smth: ")
    with open("text.txt", 'w') as f:
        f.write(text + '\n')
    with open("text.txt", 'r') as f:
        print("File data: " + f.read())

def jsonfile():
    my_dog = {
        'name': "Snoopy",
        'age': 5
    }
    with open("dog.json", "w") as f:
        json.dump(my_dog, f)
    print("JSON:")
    with open("dog.json", "r") as f:
        imported_dog = json.load(f)
    print(imported_dog)

def xmlfile():
    root = ET.Element("root")
    doc = ET.SubElement(root, "doc")

    ET.SubElement(doc, "name").text = "Snoopy"
    ET.SubElement(doc, "age").text = "5"

    tree = ET.ElementTree(root)
    tree.write("file.xml")

    tree = ET.parse('file.xml')
    root = tree.getroot()
    print("XML:")
    for elem in root:
       for subelem in elem:
          print(subelem.tag, " : ", subelem.text)

def zip():
    name = "filetozip.txt"
    name_zip = "archive.zip"
    with open(name, 'w') as f:
        f.write("String 1 2 3 Test")
        f.close()
    with ZipFile(name_zip, "w") as zip:
            zip.write(name)
    with ZipFile(name_zip, 'r') as z:
        z.extractall('extracted')
    print("ZIP:")
    with open('extracted/'+name) as f:
        print("File data: " + f.read())

if __name__ == '__main__':
    get_disk_info()
    file()
    jsonfile()
    xmlfile()
    zip()

