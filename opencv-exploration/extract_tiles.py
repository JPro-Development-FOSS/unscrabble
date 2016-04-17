#!/usr/bin/env python
''' 
Split one image into individual tile images, taking keyboard input to tag tiles.
'''
import argparse
import cv2 as cv
import hashlib

__OUT_ROWS = 100
__OUT_COLS = 91

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='split an image into NxM little images')
    parser.add_argument("-i", "--input", default='./', help="Input file.")
    parser.add_argument("-r", "--rows", default=10, help="Rows.")
    parser.add_argument("-c", "--columns", default=10, help="Columns.")
    # initial training scan seems to like rt = 1.008
    parser.add_argument("-rt", "--row_tweak", default=1, help="Linear factor to tweak row slicing.")
    parser.add_argument("-ct", "--column_tweak", default=1, help="Linear factor to tweak column slicing.")
    parser.add_argument("-d", "--dry_run", default=False, help="Don't write files")
    args = parser.parse_args()
    path = args.input
    rows = int(args.rows)
    cols = int(args.columns)
    row_tweak = float(args.row_tweak)
    col_tweak = float(args.column_tweak) 
    dry_run = bool(args.dry_run)

    cv.namedWindow("gray",1)
    img=cv.imread(path)
    if img == None:
       print "Problem opening image"
       exit(1) 
    height, width, channels = img.shape
    print "input: {}".format(img.shape)
    print "rows: {} cols:{}".format(rows, cols)
    tile_height = height / rows
    tile_width = width / cols

    for curr_row in xrange(0,rows-1):
      for curr_col in xrange(0,cols-1):
        print "curr row {} curr col {}".format(curr_row, curr_col)
        from_row = curr_row * tile_height * row_tweak
        to_row = (curr_row + 1) * tile_height * row_tweak
        from_col = curr_col * tile_width * col_tweak
        to_col = (curr_col + 1) * tile_width * col_tweak
        tile = img[from_row:to_row, from_col:to_col]
        tile = cv.resize(tile, (__OUT_COLS, __OUT_ROWS))
        cv.imshow("in", tile)
        # kind of kludgy, but grab the char from input and overwrite any files in that location
        try:
          letter = chr(cv.waitKey())
        except:
          letter = "_"
        h = hashlib.md5(cv.imencode(".png", tile)[1]).hexdigest()
        p = "{}_{}.png".format(letter, h)
        if dry_run:
          print p
        else:
          print "writing {}".format(p)
          cv.imwrite(p, tile)
    cv.destroyAllWindows() 			
