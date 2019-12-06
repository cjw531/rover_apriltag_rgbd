# rover_apriltag_rgbd
The location differences between april tag and Intel Tracking camera will be checked, and the movement will be made by the 4-wheeled robot.

## How to Run
#### * Update clock by using ntp command 
#### 0. roscore running on Fry
#### 1. Run Intel Tracking Camera T265 node on castor (robot)
#### 2. Run rosmon motion_mapping (ctrl. part of the robot) on castor (robot)
#### 3. Run kinect (global xbox camera) on turanga
#### 4. Run rviz on turanga
#### 5. Run teleop_twist_keyboard.py to control the movement of the robot on anywhere

## References
### Modules:
1.	https://github.com/IntelRealSense/realsense-ros
2.	https://github.com/IntelRealSense/realsense-ros/issues/772#issuecomment-493132694
3.	https://github.com/ros-teleop/teleop_twist_keyboard

### Intel Realsense module Official Website for SDK:
1.	https://www.intelrealsense.com/developers/?cid=sem&source=sa360&campid=2019_q2_egi_us_ntgrs_nach_revs_text-link_brand_bmm_cd_realsense-realsense_o-1lngr_google&ad_group=realsense%5Eus%5Erealsense%5Eexact&intel_term=%2Brealsense&sa360id=43700043668081492&gclid=EAIaIQobChMIm4-90MaA5AIVCSaGCh1oiAPVEAAYASABEgJHvfD_BwE&gclsrc=aw.ds

### Source Code:
1.	Existing code (*.launch, Transformation.py)
2.	Existing code from the physics_param_analysis (for the analysis part)

### ROS Wiki:
1.	http://wiki.ros.org/tf/Tutorials (Every tutorial in 2. Learning tf -> Python)

#### *Note: Code for modules are not committed.
