from ikpy.chain import Chain
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import ikpy.utils.plot as plot_utils

DIST_ROBOT2BOARD = 0.08
BOARD_LENGTH = 0.27
DIFF_HEIGHT = 0


class IK:

    def __init__(self):
        self.dofbot = Chain.from_urdf_file("URDF/dofbot.URDF")
        self.target = []

    def move(self, x, y, z):
        self.target = [x, y, z]
        self.dofbot.inverse_kinematics(self.target)
        print("The angles of each joints are : ", self.dofbot.inverse_kinematics(self.target))

    def show(self):
        ax = plt.figure().add_subplot(111, projection='3d')
        self.dofbot.plot(self.dofbot.inverse_kinematics(self.target), ax)
        plt.show()

    def setTargetFromBoard(self, pos):
        #  pos = [y, x]
        sqr_len = BOARD_LENGTH / 8
        sqr_center = sqr_len / 2
        y = DIST_ROBOT2BOARD + + sqr_center + sqr_len * (7 - pos[0])
        x = sqr_center + sqr_len * (pos[1] - 4)
        self.target = [y, x, DIFF_HEIGHT]


if __name__ == "__main__":
    move = IK()
    move.setTargetFromBoard([7, 6])
    move.show()
