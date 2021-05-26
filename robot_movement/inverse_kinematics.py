from ikpy.chain import Chain
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import ikpy.utils.plot as plot_utils
import Arm_Lib
import time
import numpy as np
import math

DIST_ROBOT2BOARD = 0.11
BOARD_SQR = 0.028
DIFF_HEIGHT = 0.00
OPEN_GRIPPER = 140
CLOSE_GRIPPER = 165

class IK:
    def __init__(self):
        self.urdf = Chain.from_urdf_file("URDF/dofbot.urdf")
        self.dofbot = Arm_Lib.Arm_Device()
        self.target = []
        self.joints = []
        self.is_closed = False
        self.gripper = OPEN_GRIPPER
        self.standby_pose = [90,135,0,0,90,self.gripper]

    def plan(self):
        self.joints = self.urdf.inverse_kinematics(self.target)
        print("The angles of each joint are : ", [(math.degrees(x)+90) for x in self.joints])
        print("target: ", self.target)
        print("forward actual: ", self.urdf.forward_kinematics(self.joints)[:,3])



    def show(self):

        ax = plt.figure().add_subplot(111, projection='3d')
        self.urdf.plot(self.joints, ax)
        plt.show()

    def set_target_from_board(self, pos):
        #  pos = [x, y]
        sqr_center = BOARD_SQR / 2
        x = DIST_ROBOT2BOARD + sqr_center + BOARD_SQR * (7 - pos[0])
        y = (sqr_center + BOARD_SQR * (pos[1] - 4))
        self.target = [y,x, DIFF_HEIGHT]
        
    def changeGripper(self):
        if self.is_closed:
            self.gripper = OPEN_GRIPPER
        else:
            self.gripper = CLOSE_GRIPPER
            
        self.standby_pose[5] = self.gripper
        self.is_closed = not self.is_closed

    def execute(self):
        self.joints = [(math.degrees(x)+90) for x in self.joints][1:-1]
        self.joints.append(270)
        self.joints.append(self.gripper)
        self.dofbot.Arm_serial_servo_write6_array(self.joints, 2000)
        time.sleep(3)
        self.changeGripper()
        self.dofbot.Arm_serial_servo_write(6, self.gripper, 500)
        time.sleep(1)
        self.dofbot.Arm_serial_servo_write6_array(self.standby_pose, 2000)
        time.sleep(2)
        
    def planAndExecute(self, pos):
        self.set_target_from_board(pos)
        self.plan()
        self.execute()
        
    def movePiece(self, pos1, pos2):
        self.planAndExecute(pos1)
        self.planAndExecute(pos2)
       
    def jumpPiece(self, pos):
        self.planAndExecute(pos)
        self.dofbot.Arm_serial_servo_write6_array([30,45,90,90,90,OPEN_GRIPPER], 500)
        wait(1)
        
        


if __name__ == "__main__":
    move = IK()
    move.movePiece([5,5],[4,4])
    #move.jumpPiece([6,6])
