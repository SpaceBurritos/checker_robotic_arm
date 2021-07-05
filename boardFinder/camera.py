import cv2
from time import sleep

class Camera:

    def __init__(self):
        self.cam = cv2.VideoCapture(-1)
        self.frame = None
        pass
    
    def take_picture(self):
        counter = 0
        while counter < 10:
            success, self.frame = self.cam.read()
            if success:
                return self.frame
            else:
                print("couldn't take picture")
                counter += 1
        return None
        
    def show(self):
        if self.frame is not None:
            cv2.imshow("webcam", self.frame)
            cv2.waitKey(0)
        else:
            print("there is no frame to show")    
    
    def exit(self):
        cv2.destroyAllWindows()
        self.cam.release()

if __name__ == "__main__":
    cam = Camera()
    cam.take_picture()
    cam.show()
    cam.exit()
