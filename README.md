
# Robotic Arm that plays Checkers

The idea of this project was to get a better understanding of different topics related to robotics and to create a project without the direct help of external help (i.e following a tutorial/course, with the help of a tutor/teacher)

I divided this project into 3 sections 

## 1. Computer Vision
I used this [machine learning algorithm](https://github.com/maciejczyzewski/neural-chessboard) for the recognition of the chessboard, after running this model the four points of the chessboard with respect to the camera were saved. 

Every time that it was the arm's move, it would grab a screenshot of the board and rectify the chessboard using those four points, then it would alter the image and grab the position and color of all the pieces and recreate the pieces into a matrix.

## 2. Checkers Logic

A minmax algorithm with an Alpha-Beta cutoff was used to generate the next best move for the arm, using the pieces positions and number of queens and pieces on eachside to get the best possible move 

## 3. Forward Kinematics

Using the URDF model of the arm it is possible to get position of the gripper at everytime, so, depending on the outcome of the checker's algorithm the robot would just move a piece or eat a piece/s


https://user-images.githubusercontent.com/59981149/177919457-915a34ec-17de-4277-aa87-0c1bc34a6e8b.mp4

