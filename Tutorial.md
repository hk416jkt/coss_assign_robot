FMCL research assignment with Park JS, Seong YW, Seong WC
#FMCL COSS assignment
# Circle Robot version setting(원형 자율 주행 로봇 셋팅)
## 1. 로봇형 자율 주행 플랫폼 셋팅 방법

### 1.1 기본 하드웨어 설정
https://github.com/hk416jkt/KMU_COSS_FMCL
해당 링크 참조

### 1.2 ROS2 SLAM 실행
원격 접속 터미널을 총 3개 띄운 후 각 터미널에서 다음 코드들을 실행한다.
#### 1번쨰 터미널
````
cd ~/ros2_ws
source install/setup.bash
ros2 launch circle_node bringup.launch.py
````
#### 2번째 터미널
````
cd ~/ros2_ws
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap /cmd_vel:=/keyboard/cmd_vel
````
#### 3번째 터미널
````
cd ~/ros2_ws
source install/setup.bash
ros2 launch circle_node cartographer.launch.py
````
위 코드 실행 후 PC에서 다음 코드를 통해 Rviz2를 실행한다.
#### PC 터미널
````
cd ~/ros2_ws
source install/setup.bash
rviz2 -d ~/ros2_ws/src/coss_assign_robot_circle/circle_cartographer/rviz/circle_cartographer.rviz 
````
이후 다음과 같이 맵을 완성한다. 이때 중요한 것은 맵이 완전히 닫혀 있어야 한다. 그렇지 않을 경우, 추후 경로 생성 시 문제가 생기는 결과가 생길 수 있으므로, 최대한 꼼꼼히 생성한다.
이미지 삽입 하기

#### Map 저장
````
ros2 run nav2_map_server map_saver_cli -f ~/map
````
해당 코드를 꼭 **라즈베리파이 터미널**에서 실행하여 저장한다. 이때 뜨는 맵의 저장 위치를 잘 기억 혹은 복사한다. (리눅스의 터미널에서 복사는 Ctrl + Shift + c, 붙여 넣기는 Ctrl + Shift + v)

### 1.2 nav2 실행하기

#### ssh 터미널 1
````
cd ~/ros2_ws
source install/setup.bash
ros2 launch circle_node bringup.launch.py
````
#### ssh 터미널 2
````
cd ~/ros2_ws
source install/setup.bash
ros2 launch circle_node navigate.launch.py map:=$HOME/map.yaml #절대경로 사용
# 위 코드가 안될 경우, ros2 launch jarabot_node navigate.launch.py map:=<맵저장위치> 로 시도 
````
#### PC 터미널 1
````
#rviz 설정파일 불러오기
rviz2 -d ~/ros2_ws/src/coss_assign_robot_circle/circle_nav2/rviz/circle_nav2.rviz
# 위 명령어 안될 경우 :ros2 run rviz2 rviz2 ~/ros2_ws/src/jarabot/jarabot_navigation2/rviz/jarabot_navigation2.rviz
````
이후 다음 화면에서 초기 위치를 지정. 너무 다르게만 지정하지 않으면 되고, 너무 세세히 하지 않아도 해당 오차를 nav2 플러그인에서 계산한다.




