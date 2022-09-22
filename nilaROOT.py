'''
Author: Marvin Schöffmann
Code to work with the root files in the "Air Shower Array"-experiment in the "Astroparticle-Physics-Lab-Course" in the Physics Masters at RWTH Aachen 
'''

import uproot
import h5py
import awkward as ak

def open(rootFile):
    ''' String: file e.g. testData.root'''
    return uproot.open(rootFile)

def saveTreeH5(tree, name="data"):
    ''' TTree: tree
        String: name {config, data}'''
    hf = h5py.File(name+"DICT.h5", "w")
    for key in tree.keys():
        data = tree[key].array()
        if name == "data" and data.fields != []: data = data["fElements"]
        data = ak.to_numpy(data)
        hf.update({key: data})
    hf.close()
    return name+"DICT.h5"

def saveBothTreesH5(rootFile):
    ''' String: file e.g. testData.root'''
    file = open(rootFile)
    return (
        saveTreeH5(file["ConfigTree"], name="config"),
        saveTreeH5(file["DataTree"], name="data"))

def getDataKeys(rootFile):
    ''' String: file e.g. testData.root'''
    return open(rootFile)["DataTree"].keys()

def getNEvents(rootFile):
    ''' String: file e.g. testData.root'''
    return getDataWithKey(rootFile, "id")[-1]

def getDataWithKey(rootFile, key):
    ''' String: file e.g. testData.root
        String: key'''
    data = open(rootFile)["DataTree"][key].array()
    if data.fields != []: return ak.to_numpy(data["fElements"])
    return ak.to_numpy(data)

def getEventWithKey(rootFile, key, event):
    '''Int: event {1, ..., NEvents}'''
    data = getDataWithKey(rootFile, key)
    return data[event-1,]

def getDataAll(rootFile, timeORwave, board, ch):
    ''' String: file e.g. testData.root
        String: timeORwave {"time", "wave"}
        Int: board {49, 50}
        Int: ch {1, 2, 3, 4}'''
    key = timeORwave + "_sn26" + board + "_" + ch
    return getDataWithKey(rootFile, key)

def getData(rootFile, timeORwave, board, ch, event):
    ''' String: file e.g. testData.root
        String: timeORwave {"time", "wave"}
        Int: board {49, 50}
        Int: ch {1, 2, 3, 4}
        Int: event {1, ..., NEvents}'''
    key = timeORwave + "_sn26" + board + "_" + ch
    return getEventWithKey(rootFile, key, event)
