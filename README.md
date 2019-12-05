# rover_apriltag_rgbd
The location differences between april tag and Intel Tracking camera will be checked, and the movement will be made by the 4-wheeled robot.

## How to Run
#### 0. roscore running on Fry
#### 1. Run Intel Tracking Camera T265 node on castor (robot)
#### 2. Run rosmon motion_mapping (ctrl. part of the robot) on castor (robot)
#### 3. Run kinect (global xbox camera) on turanga
#### 4. Run rviz on turanga
#### 5. Run teleop_twist_keyboard.py to control the movement of the robot on anywhere
