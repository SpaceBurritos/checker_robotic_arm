import cv2
from time import sleep, time

class Camera:

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2304)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1536)
        self.frame = None
        pass
        
    def set_cam(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 2304)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1536)
        
    def take_picture(self):
        counter = 0
        while counter < 10:
            success, frame = self.cam.read()
            timeCheck = time()
            future = 10*60 # delay
            while success:
                if time() >= timeCheck:
                    success,frame = self.cam.read()
                    # Do your staff here
                    return frame  
                else:
                    # Read from buffer, but skip it
                    success = self.cam.grab() # note that grab() function returnt only status code,not the frame

            if not success:
                print("couldn't take picture")
                counter += 1
        return None
        
        timeCheck = time.time()
        future = 10*60 # delay
        while ret:
            if time.time() >= timeCheck:
                ret,frame = cam.read()
                # Do your staff here
                timeCheck = time.time()+future
            else:
                # Read from buffer, but skip it
                ret = cam.grab() # note that grab() function returnt only status code,not the frame

        
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
    #cam = cv2.VideoCapture(0)
    #w = cam.get(3)
    #h = cam.get(4)
    #print (w,h)
    #while cam.isOpened():
    #    err,img = cam.read()
    #    cv2.imshow("lalala", img)
    #    k = cv2.waitKey(10) & 0xff
    #    if k==27:
    #        break
