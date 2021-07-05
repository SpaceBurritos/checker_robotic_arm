import os, sys 
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import gc, glob, argparse, boardFinder.utils as utils

print("<<< \x1b[5;32;40m neural-chessboard \x1b[0m >>>")

from boardFinder.config import *
from boardFinder.utils import ImageObject
from boardFinder.slid import pSLID, SLID, slid_tendency #== step 1
from boardFinder.laps import LAPS                       #== step 2
from boardFinder.llr import LLR, llr_pad                #== step 3
from boardFinder.camera import Camera
from keras import backend as K
import cv2; load = cv2.imread
#save = cv2.imwrite

#NC_SCORE = -1

################################################################################

def layer():
    global NC_LAYER, NC_IMAGE#, NC_SCORE
	
    print(utils.ribb("==", sep="="))
    print(utils.ribb("[%d] LAYER " % NC_LAYER, sep="="))
    print(utils.ribb("==", sep="="), "\n")

    # --- 1 step --- find all possible lines (that makes sense) ----------------
    print(utils.ribb(utils.head("SLID"), utils.clock(), "--- 1 step "))
    segments = pSLID(NC_IMAGE['main'])
    raw_lines = SLID(NC_IMAGE['main'], segments)
    lines = slid_tendency(raw_lines)

    # --- 2 step --- find interesting intersections (potentially a mesh grid) --
    print(utils.ribb(utils.head("LAPS"), utils.clock(), "--- 2 step "))
    points = LAPS(NC_IMAGE['main'], lines)
    #print(abs(49 - len(points)), NC_SCORE)
    #if NC_SCORE != -1 and abs(49 - len(points)) > NC_SCORE * 4: return
    #NC_SCORE = abs(49 - len(points))

    # --- 3 step --- last layer reproduction (for chessboard corners) ----------
    print(utils.ribb(utils.head(" LLR"), utils.clock(), "--- 3 step "))
    inner_points = LLR(NC_IMAGE['main'], points, lines)
    four_points = llr_pad(inner_points, NC_IMAGE['main']) # padcrop

    # --- 4 step --- preparation for next layer (deep analysis) ----------------
    print(utils.ribb(utils.head("   *"), utils.clock(), "--- 4 step "))
    print(four_points)
    try: 

        NC_IMAGE.crop(four_points)
        ret_points = four_points
        
    except:
        utils.warn("niestety, ale kolejna warstwa nie jest potrzebna")
        NC_IMAGE.crop(inner_points)
        ret_points = inner_points
    print("\n")
    return ret_points

################################################################################

def detect(img, output_str="output.jpg"):
    global NC_LAYER, NC_IMAGE, NC_CONFIG
    ret_points = []
    #NC_IMAGE, NC_LAYER = ImageObject(c.take_picture()), 0
    NC_IMAGE, NC_LAYER = ImageObject(img), 0
    for _ in range(NC_CONFIG['layers']):
        NC_LAYER += 1 
        ret_points.append(layer())
        print(ret_points)
    cv2.imwrite(output_str, NC_IMAGE['orig'])

    print("DETECTED")
    print(ret_points)
    return NC_IMAGE['orig']
    
def test(args):
	files = glob.glob('test/in/*.jpg')

	for iname in files:
		oname = iname.replace('in', 'out')
		args.input = iname; args.output = oname
		detect(args)

	print("TEST: %d images" % len(files))
	
################################################################################

if __name__ == "__main__":
	cam = Camera()
	
	utils.reset()
	pic = cam.take_picture()
	

	detect(pic)
	print(utils.clock(), "done")
	K.clear_session()
	gc.collect() # FIX: tensorflow#3388
