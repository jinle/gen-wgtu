#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import zipfile
import hashlib
import json
from xml.dom.minidom import Document

def md5sum(str):
    hash = hashlib.md5()
    hash.update(str)
    return hash.hexdigest()

def generateXml(newId, oldVersion, delNameList):
    doc = Document()
    wgtu = doc.createElement("wgtu")
    wgtu.setAttribute("appid", newId)
    doc.appendChild(wgtu)
    basis = doc.createElement("basis")
    basis.setAttribute("version", oldVersion)
    wgtu.appendChild(basis)

    if (len(delNameList) > 0 ):
        remove = doc.createElement("remove")
        for it in delNameList:
            item = doc.createElement("item")
            item.setAttribute("path", it)
            remove.appendChild(item)
        wgtu.appendChild(remove)

    return doc.toprettyxml(indent="\t", encoding="utf-8")

def compareWgt(oldZf, newZf):
    newNameSet = set(newZf.namelist())
    oldNameSet = set(oldZf.namelist())

    addNameList = list(newNameSet - oldNameSet)
    #print "addNameList:", addNameList
    delNameList = list(oldNameSet - newNameSet)
    #print "delNameList:", delNameList
    commNameList = list(newNameSet & oldNameSet)
    #print "commNameList:", commNameList

    newNameMd5TupList = zip(commNameList, [md5sum(newZf.read(x)) for x in commNameList])
    oldNameMd5TupList = zip(commNameList, [md5sum(oldZf.read(x)) for x in commNameList])
    modNameMd5TupSet = set(newNameMd5TupList) - set(oldNameMd5TupList)

    modNameList = [x for x, y in modNameMd5TupSet]
    #print "modNameList:", modNameList

    return addNameList, delNameList, modNameList


def main(oldWgt, newWgt, outWgtu = None):

    try:
        oldZf = zipfile.ZipFile(oldWgt, "r")
        newZf = zipfile.ZipFile(newWgt, "r")
    except IOError, e:
        print >> sys.stderr, e
        return False


    newManifest = json.loads(newZf.read("manifest.json"), "utf-8")
    oldManifest = json.loads(oldZf.read("manifest.json"), "utf-8")
    newInfo = {"id": newManifest["id"], "version": newManifest["version"]["name"] }
    oldInfo = {"id": oldManifest["id"], "version": oldManifest["version"]["name"] }

    if (newInfo["id"] != oldInfo["id"]):
        print >> sys.stderr, "app id are not equals in thier mainfest.json"
        return False

    if (newInfo["version"] <= oldInfo["version"]):
        print >> sys.stderr, "new app version must greater than old app"
        return False

    addNameList, delNameList, modNameList = compareWgt(oldZf, newZf) 
    if (len(addNameList) == 0 and len(delNameList) == 0 and len(modNameList) == 0):
        print >> sys.stderr, "two wgt files are identical, do not need generate wgtu package."
        return False

    if (outWgtu is None):
        outWgtu = "update-diff-" + oldInfo["version"] + "-" + newInfo["version"] + ".wgtu"

    try:
        outZf = zipfile.ZipFile(outWgtu, "w", zipfile.ZIP_DEFLATED)

        for name in modNameList:
            outZf.writestr("www/" + name, newZf.read(name))
        for name in addNameList:
            outZf.writestr("www/" + name, newZf.read(name))

        xml = generateXml(newInfo["id"], oldInfo["version"], delNameList)
        outZf.writestr("update.xml", xml)
        outZf.close()

        print "output: " + outWgtu

    except IOError, e:
        print >> sys.stderr, e
        return False
    finally:
        oldZf.close()
        newZf.close()        


if __name__ == "__main__":
    myargv = sys.argv[1:]
    if (len(myargv) > 3 or len(myargv) < 2):
        print >> sys.stderr, "\nUsage:  %s <old.wgt>  <new.wgt>  [out.wgtu]\n"  % sys.argv[0]
        exit(1)
    else:
        main(*myargv)
