import numpy as np
import cv2


class Board:

    def __init__(self, img):
        self.reference = img
        self.red_pieces_pos = []
        self.black_pieces_pos = []
        self.width = 0
        self.height = 0
        self.rows = []
        self.cols = []
        self.red = 130
        self.black = 100

    def get_homography(self, img):
        sift = cv2.SIFT_create()
        # find the keypoints and descriptors with SIFT
        kp1, des1 = sift.detectAndCompute(self.reference, None)
        kp2, des2 = sift.detectAndCompute(img, None)
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
        MIN_MATCH_COUNT = 9
        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
            M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

            h, w, d = self.reference.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, M)
            dst = np.int32(dst)
            img = cv2.polylines(img, [dst], True, 255, 3, cv2.LINE_AA)

        else:
            print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        return img, dst

    def get_rect_board(self, scr, img):
        dst = scr.reshape(4, 2)
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
        print(warp.shape)
        h, w, _ = warp.shape
        self.set_rows(h)
        self.set_cols(w)
        return warp  # cv2.resize(warp, (h,h))

    def set_cols(self, width):

        self.width = width
        dx = width / 8
        self.cols = [i * dx for i in range(9)]

    def set_rows(self, height):
        self.height = height
        dy = height / 8
        self.rows = [i * dy for i in range(9)]

    def set_pieces_pos(self, pieces, img, show_board):
        if pieces is not None:
            pieces = np.round(pieces[0, :]).astype("int")
            for (x, y, r) in pieces:
                pos_x = 0
                pos_y = 0
                color = img[y][x][2]
                if self.red > color > self.black:
                    continue
                else:
                    for i, col in enumerate(self.cols):
                        if x > col:
                            pos_x = i
                    for i, row in enumerate(self.rows):
                        if y > row:
                            pos_y = i
                    if color > self.red:
                        self.red_pieces_pos.append([pos_y, pos_x])
                    else:
                        self.black_pieces_pos.append([pos_y, pos_x])
                    if show_board:
                        cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                        cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    def get_pieces(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (9, 9), 2, 2)
        circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, blur.shape[0] / 8, param1=50, param2=40, minRadius=40,
                                   maxRadius=100)
        return circles

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

    def digitalized_board(self, img_with_board, show):
        self.del_positions()  # Eliminates the elements in black_pieces_pos and red_pieces_pos
        img_with_homography, dst = board.get_homography(img_with_board)
        board_img = board.get_rect_board(dst, img_with_homography)
        circles = self.get_pieces(board_img)
        self.set_pieces_pos(circles, board_img, show)

        if show:
            cv2.imshow('board', board_img)
            cv2.waitKey(0)
        return [self.black_pieces_pos, self.red_pieces_pos]


if __name__ == "__main__":
    reference_img = cv2.imread('../img/chess_board_straighten.jpg')
    board = Board(reference_img)

    img_with_board = cv2.imread('../img/Checkers_pieces_3.jpg')

    print(board.digitalized_board(img_with_board, False))

    print(board)
