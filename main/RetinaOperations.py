from main import Fileparser
import re
import numpy as np
import math
Fingerprint_size=16384
Fingerprint_width=128


def cleanFingerPrints(fingerprints):
    # removes unnecessary information from the fingerprint files that isn't directly related to the fingerprints themselves
    fingerPrintList=[]
    for f in fingerprints:
        fingerprint= f.split(",")
        fingerprint[0]=re.sub("[^0-9]","",fingerprint[0])
        fingerprint[len(fingerprint)-1]=re.sub("[^0-9]","",fingerprint[len(fingerprint)-1])
        print=[]
        for p in fingerprint:
            p=re.sub(r"\s+", "", p)
            print.append(p)
        fingerPrintList.append(print)
    return fingerPrintList

def getFingerprintOverlap(print1,print2):
        # returns the indices that have a value of 1 from both fingerpritns
        temp = set(print2)
        overlap = [value for value in print1 if value in temp]
        return overlap


def SDRFromFingerprint(print):
    # creates an SDR vector from fingerprints indices
    SDR = np.zeros((Fingerprint_width, Fingerprint_width),dtype=np.int16)
    for p in print:
        idx=int(p)
        rowIdx=idx//Fingerprint_width
        columnIdx= idx % Fingerprint_width
        SDR[rowIdx][columnIdx]=1;
    return SDR


def getSimilarityMetrics(print1,print2):
    # returns the euclidean distance, cosine similarity, jaccard index and jaccard distance from the comparison of two fingerprints
    overlapSize = len(getFingerprintOverlap(print1,print2))
    length1 = len(print1)
    length2 = len(print2)
    unionSize = length1+length2-overlapSize
    dissimilaritySize = unionSize-overlapSize
    euclideanDistance= math.sqrt(dissimilaritySize)
    cosineSimilarity = overlapSize/(math.sqrt(length1)*math.sqrt(length2))
    jaccardIndex=overlapSize/unionSize
    jaccardDistance=1-jaccardIndex
    return euclideanDistance, cosineSimilarity, jaccardIndex, jaccardDistance



def aggregateFingerPrints(printList):
    # returns a dictionary of non-zero indices and their number of occurences within a list of fingerprints
    indexDict = {}
    for print in printList:
        for p in print:
             if p in indexDict:
                 indexDict[p]=(int(indexDict[p])+1)
             else:
                 indexDict.update({p:1})
    return indexDict

def kSparsify(indexDict, k):
    # sparsifies the aggregated fingerprint representation to create a merged print
    print=[]
    for idx in indexDict:
        if(int(indexDict[idx])>=k):
            print.append(idx)
    print.sort(key=int)
    return print

def mergePrints(printList):
    # merges multiple fingerprints into a single print by aggregation and sparsification
    k=round(math.sqrt(len(printList)))
    indexDict = aggregateFingerPrints(printList)
    return kSparsify(indexDict, k)

def saveCleanFingerPrints(prints,path):
    # saves the clean fingerprints to a file
    prints = cleanFingerPrints(prints)
    with open(path, 'w', encoding="utf-8", errors='ignore') as cleanFile:
        for i in range(len(prints)):
            for j in range(len(prints[i])):
                cleanFile.write(prints[i][j])
                cleanFile.write(",")
            cleanFile.write("|")



fingerprintPath="C:\DiplomaProject\AlmarimiFingerprints\Fingerprints3.txt"
indexPath="C:\DiplomaProject\AlmarimiIndices\Indices3.txt"
cleanPath="C:\DiplomaProject\CleanFingerprints\Fingerprints3.txt"
prints = Fileparser.get_fingerprint_from_file(cleanPath)
print(len(prints[0]))
print(len(prints[1]))
print(len(prints[2]))
print(len(prints[3]))
printList=[prints[0],prints[1]]
merged=mergePrints(printList)
print(len(merged))
#indices = Fileparser.get_indices_from_file(indexPath)



