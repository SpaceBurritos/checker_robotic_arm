from ikpy.chain import Chain
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import ikpy.utils.plot as plot_utils
#import Arm_Lib
import time

DIST_ROBOT2BOARD = 0.11
BOARD_LENGTH = 0.222
DIFF_HEIGHT = 0


class IK:

    def __init__(self):
        self.urdf = Chain.from_urdf_file("URDF/dofbot.urdf")
        #self.dofbot = Arm_Lib.Arm_Device()
        self.target = []
        self.joints = []
        self.gripper = 135

    def plan(self):
        self.joints = self.urdf.inverse_kinematics(self.target)
        print("The angles of each joints are : ", self.joints)

    def show(self):
        print(self.target)
        ax = plt.figure().add_subplot(111, projection='3d')
        self.urdf.plot(self.joints, ax)
        plt.show()

    def set_target_from_board(self, pos):
        #  pos = [y, x]
        sqr_len = BOARD_LENGTH / 8
        sqr_center = sqr_len / 2
        y = DIST_ROBOT2BOARD + + sqr_center + sqr_len * (7 - pos[0])
        x = sqr_center + sqr_len * (pos[1] - 4)
        self.target = [y, x, DIFF_HEIGHT]

    def execute(self):
        self.dofbot.Arm_serial_servo_write6(self.target, self.gripper, 1000)
        time.sleep(1)


if __name__ == "__main__":
    move = IK()
    move.set_target_from_board([7, 6])
    move.plan()
    move.show()
