#!/usr/bin/env python
''' 
Split one image into individual tile images, taking keyboard input to tag tiles.
'''
import argparse
import cv2 as cv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='split an image into NxM little images')
    parser.add_argument("-i", "--input", default='./', help="Input file.")
    parser.add_argument("-r", "--rows", default=1, help="Rows.")
    parser.add_argument("-c", "--columns", default=1, help="Columns.")
    args = parser.parse_args()
    path = args.input
 
    cv.namedWindow("gray",1)
    img=cv.imread(path)
    if img == None:
       print "Problem opening image"
       exit(1) 
    #gray=cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #cv.imshow("gray",gray)
    height, width, channels = img.shape
    rows = int(args.rows)
    cols = int(args.columns)
    print "input: {}".format(img.shape)
    print "rows: {} cols:{}".format(rows, cols)
    tile_height = height / rows
    tile_width = width / cols

    __ROW_TWEAK_FACTOR = 1.008
    __COL_TWEAK_FACTOR = 1.0
    for curr_row in xrange(0,rows-1):
      for curr_col in xrange(0,cols-1):
        print "curr row {} curr col {}".format(curr_row, curr_col)
        from_row = curr_row * tile_height * __ROW_TWEAK_FACTOR
        to_row = (curr_row + 1) * tile_height * __ROW_TWEAK_FACTOR
        from_col = curr_col * tile_width * __COL_TWEAK_FACTOR
        to_col = (curr_col + 1) * tile_width * __COL_TWEAK_FACTOR
        tile = img[from_row:to_row, from_col:to_col]
        cv.imshow("in", tile)
        # kind of kludgy, but grab the char from input and overwrite any files in that location
        try:
          letter = chr(cv.waitKey())
        except:
          letter = "_"
        cv.imwrite("{}.png".format(letter), tile)
    cv.destroyAllWindows() 			
