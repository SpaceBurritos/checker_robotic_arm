from ikpy.chain import Chain
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import ikpy.utils.plot as plot_utils
import Arm_Lib
import time
import numpy as np
import math

DIST_ROBOT2BOARD = 0.103
BOARD_SQR_Y = 0.02775
BOARD_SQR_X = 0.0293
DIFF_HEIGHT = 0.033 #0.007
OPEN_GRIPPER = 120
CLOSE_GRIPPER = 169

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

    def show(self):

        ax = plt.figure().add_subplot(111, projection='3d')
        self.urdf.plot(self.joints, ax)
        plt.show()

    def set_target_from_board(self, pos):
        #  pos = [y, x]
        sqr_center = BOARD_SQR_X / 2
        y = DIST_ROBOT2BOARD + sqr_center + BOARD_SQR_Y * (7 - pos[0])
        x = (sqr_center + BOARD_SQR_X * (pos[1] - 4))
        z = (DIFF_HEIGHT)*math.exp((7-pos[0])*0.06)#DIFF_HEIGHT+(7-pos[0])*0.0029
        self.target = [x,y, z]
        
    def changeGripper(self):
        if self.is_closed:
            self.gripper = OPEN_GRIPPER
        else:
            self.gripper = CLOSE_GRIPPER
            
        self.standby_pose[5] = self.gripper
        self.is_closed = not self.is_closed

    def execute(self, make_king = False):
        self.joints = [(math.degrees(x)+90) for x in self.joints][1:-1]
        if make_king:
            self.joints.append(90)
        else:
            self.joints.append(270)
        self.joints.append(self.gripper)
        self.dofbot.Arm_serial_servo_write6_array(self.joints, 2000)
        time.sleep(2)
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
       
    def jumpPiece(self, pos1, pos2):
        self.movePiece(pos1, pos2)
        jump_y = (pos1[0] + pos2[0])/2
        jump_x = (pos1[1] + pos2[1])/2
        self.planAndExecute([jump_y, jump_x])
        self.dofbot.Arm_serial_servo_write6_array([30,45,90,90,90,self.gripper], 1000)
        time.sleep(1)
        self.changeGripper()
        self.dofbot.Arm_serial_servo_write(6, self.gripper, 500)
        time.sleep(1)
        self.dofbot.Arm_serial_servo_write6_array(self.standby_pose, 1000)
        time.sleep(1)
        
    def make_king(self, pos1, pos2):
        self.planAndExecute(pos1)
        self.set_target_from_board(pos2)
        self.plan()
        self.execute(True)
        
        pass
        


if __name__ == "__main__":
    move = IK()
    move.make_king([1,0],[0,1])

    #move.movePiece([7,4],[0,1])
    #move.movePiece([0,1],[6,5])
    #move.jumpPiece([6,6])
