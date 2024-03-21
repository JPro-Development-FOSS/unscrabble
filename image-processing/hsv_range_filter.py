#!/usr/bin/env python
''' 
Apply an HSV range filter to all files in the current directory.
'''
import sys
import os
import glob
import argparse
import cv2 as cv
           
 
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply an HSV range filter to all files in the current directory.')
    parser.add_argument("-i","--input", default='./', help="Input directory.")
    args = parser.parse_args()
    path = args.input
 
    '''Loop through all the images in the directory'''
    for infile in glob.glob( os.path.join(path, '*.*') ):
        ext = os.path.splitext(infile)[1][1:] #get the filename extenstion
        if ext == "png" or ext == "jpg" or ext == "bmp" or ext == "tiff" or ext == "pbm":
            print infile
            
            img=cv.imread(infile)
            if img == None:
                continue
            rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            hsv = cv.cvtColor(rgb, cv.COLOR_RGB2HSV)
            #hsv = cv.cvtColor(rgb, cv.COLOR_RGB2HSV_FULL)
            #filtered = cv.inRange(hsv, (14, 92, 150), (44, 173, 208))
            filtered = cv.inRange(hsv, (0, 0, 150), (44, 255, 255))
            #cv.imshow("filtered", filtered)
            #cv.waitKey()
            cv.imwrite("{}_filtered.png".format(os.path.split(infile)[-1][:-4]), filtered)
    cv.destroyAllWindows() 			
