'''
Author: Marvin Schöffmann
Code to work with the root files in the "Air Shower Array"-experiment in the "Astroparticle-Physics-Lab-Course" in the Physics Masters at RWTH Aachen 
'''

from uproot import open
from h5py import File
from awkward import to_numpy
from matplotlib.pyplot import plot
from time import time

def open(rootFile):
    ''' String: file e.g. testData.root'''
    return open(rootFile)

def saveTreeH5(tree, path="data/", name="data"):
    ''' TTree: tree
        String: path (for h5 file)
        String: name {config, data}'''
    print("Start unpack tree:", name)
    timeStart = time()
    hf = File(path+name+"DICT.h5", "w")
    percent = 0.0
    for key in tree.keys():
        data = tree[key].array()
        if name == "data" and data.fields != []: data = data["fElements"]
        data = to_numpy(data)
        hf.update({key: data})
        percent += 1/len(tree.keys())
        print("Progress: {:.0%}".format(percent))
    hf.close()
    print("Time: {:.3f} seconds".format(time()-timeStart))
    return name+"DICT.h5"

def saveBothTreesH5(rootFile, path="data/"):
    ''' String: file e.g. testData.root'''
    file = open(rootFile)
    return (
        saveTreeH5(file["ConfigTree"], path, "config"),
        saveTreeH5(file["DataTree"], path, "data"))

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
    if data.fields != []: return to_numpy(data["fElements"])
    return to_numpy(data)

def getEventWithKey(rootFile, key, event):
    '''Int: event {1, ..., NEvents}'''
    data = getDataWithKey(rootFile, key)
    return data[event-1,]

def getDataAll(rootFile, timeORwave, board, ch):
    ''' String: file e.g. testData.root
        String: timeORwave {"time", "wave"}
        Int: board {49, 50}
        Int: ch {1, 2, 3, 4}'''
    key = timeORwave + "_sn26" + str(board) + "_ch" + str(ch)
    return getDataWithKey(rootFile, key)

def getData(rootFile, timeORwave, board, ch, event):
    ''' String: file e.g. testData.root
        String: timeORwave {"time", "wave"}
        Int: board {49, 50}
        Int: ch {1, 2, 3, 4}
        Int: event {1, ..., NEvents}'''
    key = timeORwave + "_sn26" + str(board) + "_ch" + str(ch)
    return getEventWithKey(rootFile, key, event)

def getPlot(rootFile, board, ch, event):
    dataTime = getData(rootFile, "time", board, ch, event)
    dataWave = getData(rootFile, "wave", board, ch, event)
    return plot(dataTime, dataWave)