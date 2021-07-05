import os, sys 
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import numpy as np
import cv2
#from camera import Camera
from sklearn.cluster import KMeans

from boardFinder.utils import ImageObject
#from boardFinder.main import detect

from matplotlib import pyplot as plt
from skimage import measure

LAYERS = 3
SQR_SIZE = 500

class DigitalBoard:

    def __init__(self, img):
        self.reference = img#cv2.resize(img, (500,500))
        self.red_pieces_pos = []
        self.black_pieces_pos = []
        self.width = 0
        self.height = 0
        self.points = []
        self.div_col = 80
        self.image = None
        self.points = []
        self.red = 130
        self.black = 100

    def get_homography(self, img):

        akaze = cv2.AKAZE_create()
        # find the keypoints and descriptors with Akaze
        kp1, des1 = akaze.detectAndCompute(self.reference, None)
        kp2, des2 = akaze.detectAndCompute(img, None)

        if des1.dtype != "float32":
            des1 = des1.astype("float32")
        if des2.dtype != "float32":
            des2 = des2.astype("float32")

        #des2 = np.float32(des2)
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        good = []

        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        MIN_MATCH_COUNT = 12
        if len(good) > MIN_MATCH_COUNT:
            print("enough matches")
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
            matchesMask = mask.ravel().tolist()
            
            h, w, d = self.reference.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            dst = np.int32(dst)
            img = cv2.polylines(img, [dst], True, 255, 3, cv2.LINE_AA)
            #cv2.imshow("img", img)
            #cv2.waitKey(0)

        else:
            print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))

        #self.image = img
        self.points = dst.reshape(4,2)
        return img

    def get_rect_board(self, img):
        dst = self.points#.reshape(4, 2)
        rect = np.zeros((4, 2), dtype="float32")

        s = dst.sum(axis=1)
        rect[0] = dst[np.argmin(s)]
        rect[2] = dst[np.argmax(s)]

        diff = np.diff(dst, axis=1)
        rect[1] = dst[np.argmin(diff)]
        rect[3] = dst[np.argmax(diff)]

        (tl, tr, br, bl) = rect
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        # ...and now for the height of our new image
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        # take the maximum of the width and height values to reach
        # our final dimensions
        maxWidth = max(int(widthA), int(widthB))
        maxHeight = max(int(heightA), int(heightB))
        # construct our destination points which will be used to
        # map the screen to a top-down, "birds eye" view
        dest = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
        # calculate the perspective transform matrix and warp
        # the perspective to grab the screen
        mat = cv2.getPerspectiveTransform(rect, dest)
        warp = cv2.warpPerspective(img, mat, (maxWidth, maxHeight))

        h, w, _ = warp.shape

        return warp  # cv2.resize(warp, (h,h))


    def set_points(self, pts):
        self.points = pts

    def set_pieces_pos(self, img, pieces, colors, show_board=True):

        if pieces is not None:
            colors = np.array(colors)
            color_clusters = KMeans(n_clusters=2, random_state=0).fit_predict(colors) 

            darker_label = 1 if np.mean(colors[color_clusters == 1]) < np.mean(colors[color_clusters == 0]) else 0
            for i, p in enumerate(pieces):
                y = p[0]
                x = p[1]
                if color_clusters[i] == darker_label:
                    self.black_pieces_pos.append([y, x])
                else:
                    self.red_pieces_pos.append([y, x])
                if show_board:
                    x_pos = int(x*img.shape[1]/8 + (img.shape[1]/8)/2)
                    y_pos = int(y*img.shape[0]/8 + (img.shape[0]/8)/2)
                    cv2.circle(img, (x_pos, y_pos), 25, (0, 255, 0), 3)

            if show_board:
                cv2.imshow("img", img)
                cv2.waitKey(0)
        else:
            print("there are no pieces")

        
    def get_pieces(self, img):

        img_rsz = cv2.resize(img, (500,500))

        
        blur = cv2.GaussianBlur(img_rsz, (5,5), 0)

         
        blur2 = cv2.resize(cv2.GaussianBlur(self.reference, (5,5), 0), (500,500))

        diff = cv2.absdiff(blur, blur2)
        diff = cv2.cvtColor(diff, cv2.COLOR_BGR2HSV)

        kernel = np.ones((5,5), np.uint8)
        diff = cv2.erode(diff, kernel, iterations=1)

        h, s, v = cv2.split(diff)    

        ret, th3 = cv2.threshold(v, 70, 255, cv2.THRESH_BINARY)  
        th3 = cv2.dilate(th3, kernel, iterations=1)
        
        contours, hierarchy = cv2.findContours(th3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.imshow("img", img_rsz)        
        #cv2.imshow("th3", th3)
        #cv2.waitKey(0)
        
        colors = []
        pieces = []

        for c in contours:
            M = cv2.moments(c)
            if cv2.contourArea(c) > 500:
                cx = int(M['m10']/M['m00'])
                cy = int(M['m01']/M['m00'])
                r = img_rsz.shape[0]/18
                x_size = img_rsz.shape[0]
                y_size = img_rsz.shape[1]
                
                roi = img_rsz[max(0, int(cy - r)) : min(int(cy + r), y_size), max(0, int(cx - r)) : min(int(cx + r), x_size)]
                w, h, _ = roi.shape
                mask = np.zeros((w,h, 3 ), roi.dtype)
                cv2.circle(mask, (int(w/2), int(h/2)), int(r), (255, 255, 255), -1)
                dst = cv2.bitwise_and(roi, mask)
                if dst is not None:
                    y_index = int(cy/(img_rsz.shape[0]/8))
                    x_index = int(cx/(img_rsz.shape[1]/8))

                    color = np.mean(dst, axis=0)
                    color = np.mean(color, axis=0)
                    pieces.append([y_index, x_index])
                    colors.append(color)
                    cv2.circle(img_rsz, (int(cx), int(cy)), int(r), (0, 255, 0), 3)

        return pieces, colors

    def del_positions(self):
        self.black_pieces_pos = []
        self.red_pieces_pos = []

    def __str__(self):
        rows = " x  0  1  2  3  4  5  6  7 \n"
        for yp in range(8):
            rows +=  " " + str(yp) + " "
            for xp in range(8):
                if [yp, xp] in self.black_pieces_pos:
                    rows += " B "
                elif [yp, xp] in self.red_pieces_pos:
                    rows += " R "
                else:
                    rows += " - "
            rows += "\n"
        return rows

    def digitalize_board(self, img_with_board, show=False):

        self.del_positions()  # Eliminates the elements in black_pieces_pos and red_pieces_pos

        d = self.get_homography(img_with_board)
        rect_img = self.get_rect_board(img_with_board)
        circles, colors = self.get_pieces(rect_img)
        self.set_pieces_pos(rect_img, circles, colors, show)
        
        return [self.black_pieces_pos, self.red_pieces_pos]


if __name__ == "__main__":
    cam = Camera()
    reference_img = cv2.imread('../boardFinder/output.jpg')
    board_img = cam.take_picture()

    board = DigitalBoard(reference_img)
    print(board.digitalize_board(board_img, True))
    print(board)
