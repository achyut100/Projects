
from __future__ import print_function
import glob
import argparse
import numpy as np
import cv2
import csv


class BookDescriptor:
    #this function finds all the keypoints in an image and describes area surrounding
    #each keypoint
    def describe(self, image):
        descriptor = cv2.BRISK_create()
        (kps, descs) = descriptor.detectAndCompute(image, None) 
        kps = np.float32([kp.pt for kp in kps]) #x,y coordinates of keypts
        return (kps, descs)





class BookMatcher:
    
    def __init__(self, descriptor, coverPaths, ratio = 0.7,minMatches = 40, useHamming = True):
        self.descriptor = descriptor
        self.coverPaths = coverPaths
        self.ratio = ratio
        self.minMatches = minMatches
        self.distanceMethod = "BruteForce"

        if useHamming:
            self.distanceMethod += "-Hamming"
            
            
    #this search method is to take the keypoints and descriptors from the query image and 
    #then match them against a database of keypoints and descriptors    
    def search(self, queryKps, queryDescs):
        #dictionary to store result for match accuracy
        results = {}
        for coverPath in self.coverPaths:
            cover = cv2.imread(coverPath)
            gray = cv2.cvtColor(cover, cv2.COLOR_BGR2GRAY)
            (kps, descs) = self.descriptor.describe(gray)
            score = self.match(queryKps, queryDescs, kps, descs)
            results[coverPath] = score
            
        #sorting results in descending order
        if len(results) > 0:
            results = sorted([(v, k) for (k, v) in results.items() if v > 0],reverse = True) 
        
        return results
    
    
    
    #this function matches features of the queried image with all the stored image using KNN
    def match(self, kpsA, featuresA, kpsB, featuresB):
        matcher = cv2.DescriptorMatcher_create(self.distanceMethod)
        
        #K-Nearest Neighbours is used
        rawMatches = matcher.knnMatch(featuresB, featuresA, 2)
        
        matches = []
        for m in rawMatches:
            if len(m) == 2 and m[0].distance < m[1].distance*self.ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        if len(matches) > self.minMatches:
            ptsA = np.float32([kpsA[i] for (i, _) in matches])
            ptsB = np.float32([kpsB[j] for (_, j) in matches])
            (_, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, 4.0)
            return float(status.sum())/status.size
        return -1.0
        
        
#main
#parsing cmdl args
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--db", required = True,help = "path to the book database")
ap.add_argument("-b", "--books", required = True,help = "path to the directory that contains our book covers")
ap.add_argument("-q", "--query", required = True,help = "path to the query book cover")

args = vars(ap.parse_args())


db={}
for l in csv.reader(open(args["db"])):
     db[l[0]] = l[1:]
     
     
#using BRISK which produces binary feature vectors
useHamming = True
ratio = 0.7
minMatches = 40


#display 
cd = BookDescriptor()
cv = BookMatcher(cd, glob.glob(args["books"] + "/*.jpeg"),ratio = ratio, minMatches = minMatches, useHamming =useHamming)
queryImage = cv2.imread(args["query"])
gray = cv2.cvtColor(queryImage, cv2.COLOR_BGR2GRAY)

(queryKps, queryDescs) = cd.describe(gray) 
results = cv.search(queryKps, queryDescs)
cv2.imshow("Query", queryImage)    


if len(results) == 0:
    print("Sorry, could not find a match for the Book")
    cv2.waitKey(0)
else:
    for (i, (score, coverPath)) in enumerate(results):
       (author, title) = db[coverPath[coverPath.rfind("/") +1:]]
       print("{}. {:.2f}% : {} - {}".format(i + 1, score * 100,author, title))
       result = cv2.imread(coverPath)
       cv2.imshow("Result", result)
       cv2.waitKey(0)
