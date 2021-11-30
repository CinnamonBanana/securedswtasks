import os
import psutil
import json
import xml.etree.ElementTree as ET
from zipfile import ZipFile

def get_disk_info():
    disk_info = []
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
    return disk_info

def file():
    text = input("Please enter smth: ")
    with open("text.txt", 'w') as f:
        f.write(text + '\n')
    with open("text.txt", 'r') as f:
        print(f.read())

def jsonfile():
    my_dog = {
        'name': "Snoopy",
        'age': 5
    }
    with open("dog.json", "w") as f:
        json.dump(my_dog, f)
    with open("dog.json", "r") as f:
        imported_dog = json.load(f)
    print(imported_dog)

def xmlfile():
    name = "file.xml"
    root = ET.Element("data")
    tree = ET.ElementTree(root)
    tree.write("%s" %(name))
    with open("%s" % (name), "r") as file:
        tree = ET.fromstring(file.read())
    print(ET.tostring(tree))

def zip():
    name = "filetozip.txt"
    name_zip = "archive.zip"
    with open(name, 'w') as f:
        f.write("String 1 2 3 Test")
        f.close()
    with ZipFile(name_zip, "w") as zip:
            zip.write(name)
    z = ZipFile(name_zip, 'r')
    z.extractall()
    z.close()
    file = open(name)
    print("File data: " + file.read())
    file.close()
    print("File info:")
    print("     Size: " + str(os.path.getsize(name)) + " Bytes")
    print("     Updated: " + str(os.path.getmtime(name)))
    print("     Created: " + str(os.path.getctime(name)))
    os.remove(name)
    os.remove(name_zip)

if __name__ == '__main__':
    get_disk_info()
    file()
    jsonfile()
    xmlfile()
    zip()

