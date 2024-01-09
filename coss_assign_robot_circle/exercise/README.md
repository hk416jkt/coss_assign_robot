# 1. Jarabot



<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/jarabot.png" alt="이미지 대체 텍스트" style="float: left;">



- HW

  - Rapsberry Pi 4 (4GB) 설정
  - memory : 16GB 이상(32GB 추천)
  - YDLIDAR X4 Pro or RPLIDAR A1M8
  - Odometry Wheel(1200 PPR)

- SW
  - Ubuntu 22.04.x

  - ROS 2 Humble Hawksbill 

    [ROS 2 Humble Desktop 설치](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)



+ 아두이노에 아래 OdomWheel 코드가 Upload 되어 RPI에 연결되어 있는 상태여야 함.

[motor arduino nano code](https://github.com/firstbot1/jarabot/blob/main/motor.ino)

* 원형 자라봇의 Wheel Diameter는  220mm, 사각 자라봇의 Wheel diameter는180mm임

<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/odom_param.png" alt="이미지 대체 텍스트" style="float: left;">


## 1. SW 설치

- 첫 부팅 후 wifi 설정하기 및 통신 확인하기
- 첫 부팅 후 터미널

```
sudo apt update
sudo apt upgrade
```



- network 관련 설치

```
sudo apt install git  
sudo apt install net-tools # ifconfg  명령 사용 가능
sudo apt install openssh-server  #ssh 접속 가능
```



- network 관련 설정(ssh 연결 가능하도록 설정)

```
sudo systemctl status ssh  # SSH 서버 실행 중인지 상태 확인
sudo systemctl start ssh # SSH 서버가 실행시키기 
sudo ufw allow 22
sudo ufw allow ssh
sudo ufw status
sudo ufw enable
sudo systemctl restart ssh

sudo reboot
```



- RPi의 network IP 알아오기

```
ifconfig
```

<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/ifconfig.png" alt="이미지 대체 텍스트" style="float: left;">

- RPi의 IP를 기록해 두었다가 PC에서 RPi에 기록한 IP를 사용하여 연결하기

```
ssh jarabot@172.30.1.15    #PC에서
```



## 2. YDLiDAR 및 jarabot ROS 2 패키지 설치



### 2.1 YDLIDAR SDK 및 빌드(home에서...)

```
#YDLidar-SDK 설치 및 빌드(home에서)
git clone https://github.com/YDLIDAR/YDLidar-SDK.git
cd YDLidar-SDK
mkdir build && cd build
cmake ..
make && sudo make install
sudo reboot
```



### 2.2 jarabot ROS2 패키지 및 YDLIDAR 패키지 설치 및 빌드

+ Ubuntu 22.04 설치된...

```
# ~/.bashrc에 source /opt/ros/humble/setup.bash 확인
sudo apt purge brltty
sudo apt install ros-humble-serial-driver \
ros-humble-teleop-twist-keyboard \
ros-humble-navigation2 \
ros-humble-nav2-bringup \
ros-humble-cartographer \
ros-humble-cartographer-ros \
udev \
ufw
```



```
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/firstbot1/ydlidar_ros2_driver   #for ydlidar X4-pro
git clone https://github.com/firstbot1/jarabot               #for ydlidar X4-pro
#git clone https://github.com/Slamtec/sllidar_ros2.git        #for rplidar A1M8
#git clone https://github.com/jarabot/jarabot.git             #for rplidar A1M8 
cd ~/ros2_ws
colcon build --symlink-install
```



### 2.3 udev 규칙 설정

```
sudo cp ~/ros2_ws/src/jarabot/jarabot_node/rule/99-jarabot.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```

+ 라이다와 아두이노 연결 확인

```
ls /dev/my*
```

<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/udev.png" alt="이미지 대체 텍스트" style="float: left;">

만약 위와 같이  장치를 인식하지 못했다면 권한설정 변경

```
sudo chmod 666 /dev/ttyUSB0
```

```
sudo chmod 666 /dev/ttyUSB1
```

또는

```
sudo chmod 666 /dev/mydriver
```

```
sudo chmod 666 /dev/mylidar
```



## 3. ROS_DOMAIN_ID 설정



- Jarabot과 내 PC가 서로 통신이 가능하게 하기 위해서 양쪽 모두 동일한 ID로 설정

ROS_DOMAIN_ID 환경 변수는 ROS 2 네트워크에서 서로 다른 ROS 2 시스템 간의 통신을 격리하기 위해 사용

```
#export ROS_LOCALHOST_ONLY=1 이부분은 코멘트처리하기

#~/.bashrc 파일에 맨 아래에 추가 ID 값은 각 조별로 1~232까지 설정
export export ROS_DOMAIN_ID=3
```

nano ~/.bashrc 로 확인가능.



## 4 방화벽 풀기(ROS_DOMAIN_ID 통신을 위해서)

- PC<->RPi 통신을 위해

ufw는 방화벽 관리 도구

```
#ufw가 설치되어 있지 않은 경우에 설치 : sudo apt-get install ufw
sudo ufw enable

sudo ufw allow 1:65535/tcp
sudo ufw allow 1:65535/udp

sudo ufw status # 확인

sudo reboot
```







# 2. PC 설정



SW

- Ubuntu 22.04.x

- [ROS 2 Humble Desktop 설치](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)



## 1 YDLiDAR 및 jarabot ROS 2 패키지 설치



### 1.2 YDLIDAR SDK 및 빌드(home에서...) ...for test

```
#YDLidar-SDK 설치 및 빌드(home에서)
git clone https://github.com/YDLIDAR/YDLidar-SDK.git
cd YDLidar-SDK
mkdir build && cd build
cmake ..
make && sudo make install
sudo reboot
```



### 1.2 jarabot ROS2 패키지 및 YDLIDAR 패키지 설치 및 빌드

```
# ~/.bashrc에 source /opt/ros/humble/setup.bash 확인
sudo apt purge brltty
sudo apt install ros-humble-serial-driver \
ros-humble-teleop-twist-keyboard \
ros-humble-navigation2 \
ros-humble-nav2-bringup \
ros-humble-cartographer \
ros-humble-cartographer-ros \
udev \
ufw
```



```
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/firstbot1/ydlidar_ros2_driver   #for ydlidar X4-pro
git clone https://github.com/firstbot1/jarabot               #for ydlidar X4-pro
#git clone https://github.com/Slamtec/sllidar_ros2.git        #for rplidar A1M8
#git clone https://github.com/jarabot/jarabot.git             #for rplidar A1M8 
cd ~/ros2_ws
colcon build --symlink-install
```



### 1.3 udev 규칙 설정

```
sudo cp ~/ros2_ws/src/jarabot/jarabot_node/rule/99-jarabot.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
sudo udevadm trigger
```





## 2.3 ROS_DOMAIN_ID 설정



- Jarabot과 내 PC가 서로 통신이 가능하게 하기 위해서 양쪽 모두 동일한 ID로 설정

```
#export ROS_LOCALHOST_ONLY=1 이부분은 코멘트처리하기

#~/.bashrc 파일에 맨 아래에 추가 ID 값은 각 조별로 1~232까지 설정 범위
export export ROS_DOMAIN_ID=2
```

nano ~/.bashrc 로 확인가능.



## 2.4 방화벽 풀기(ROS_DOMAIN_ID 통신을 위해서)



- PC<->RPi 통신을 위해

```
#ufw가 설치되어 있지 않은 경우에 설치 : sudo apt-get install ufw
sudo ufw enable

sudo ufw allow 1:65535/tcp
sudo ufw allow 1:65535/udp

sudo ufw status # 확인

sudo reboot
```





## 3. Jarabot 접속하기



+ PC 터미널에서... RPI에서 ifconfig로 확인한 IP 주소가 172.30.1.15라면\

```
ssh jarabot@172.30.1.15
```

<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/ssh.png" alt="이미지 대체 텍스트" style="float: left;">






## 4. jarabot cartographer RVIZ2 실행 (지도 생성 SLAM) 



* Local PC에서 ssh로 자로봇을 원격 제어한다.



### 4.1 jatabot  터미널1

```
cd ~/ros2_ws
source install/setup.bash
ros2 launch jarabot_node bringup.launch.py
```



### 4.2 jarabot 터미널2 : teleop_twist_keyboard로 Moving(키보드로 조종)

```
cd ~/ros2_ws
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap /cmd_vel:=/keyboard/cmd_vel
```



### 4.3 jarabot 터미널3 : 카토그라퍼 실행

```
cd ~/ros2_ws
source install/setup.bash
ros2 launch jarabot_node cartographer.launch.py # jarabot 터미널
```



### 4.4 PC 터미널1 : Cartographer Rviz2 실행(SLAM Map 생성)

```
cd ~/ros2_ws
source install/setup.bash
rviz2 -d ~/ros2_ws/src/jarabot/jarabot_cartographer/rviz/jarabot_cartographer.rviz #local pc 에서 실행
```

<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/slam.png" alt="이미지 대체 텍스트" style="float: left;">


### 4.5 지도 저장

+ teleop_twist_keyboard를 실행한 화면에서 키보드로 조정하며 충분히 맵 생성 후 저장.

```
ros2 run nav2_map_server map_saver_cli -f ~/map
```

[참조](https://turtlebot.github.io/turtlebot4-user-manual/tutorials/generate_map.html#save-the-map)





## 5. jarabot navigation2 RVIZ2 실행



### 5.1 jarabot 터미널1

```
cd ~/ros2_ws
source install/setup.bash
ros2 launch jarabot_node bringup.launch.py 
```



### 5.2 jababot 터미널2

```
cd ~/ros2_ws
source install/setup.bash
ros2 launch jarabot_node navigate.launch.py map:=$HOME/map.yaml #절대경로 사용
```



### 5.3 PC터미널1

```
#rviz 설정파일 불러오기
rviz2 -d ~/ros2_ws/src/jarabot/jarabot_navigation2/rviz/jarabot_navigation2.rviz
ros2 run rviz2 rviz2 ~/ros2_ws/src/jarabot/jarabot_navigation2/rviz/jarabot_navigation2.rviz
```

<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/navi.png" alt="이미지 대체 텍스트" style="float: left;">


#### 5.3.1 2D Pose Estimate 수행

RViz2에서 **"2D Pose Estimate"** 기능은 로봇의 초기 위치와 방향을 지도 상에 수동으로 지정하는 데 사용됩니다. 이 기능은 주로 로봇이 자신의 현재 위치를 지도에서 찾지 못하는 상황에서 로봇의 위치를 초기화하는 데 사용됩니다. 예를 들어, SLAM(Simultaneous Localization and Mapping)과 같은 애플리케이션에서 매우 유용합니다.

로봇의 위치 추정 및 내비게이션 시스템은 로봇이 환경에서 자신의 위치를 파악하고 이동할 경로를 계획하는 데 필수적입니다. 그러나 로봇이 처음 환경에 배치되거나, 로봇의 내부 위치 추정 시스템이 신뢰할 수 없는 데이터를 제공하는 경우, 로봇은 정확한 위치를 파악하는 데 어려움을 겪을 수 있습니다. 이때 "2D Pose Estimate" 기능을 사용하여, 사용자가 로봇의 시작 위치와 방향을 지도 상에서 직접 지정할 수 있습니다.

"2D Pose Estimate" 도구를 사용하는 방법은 다음과 같습니다:

1. RViz2에서 "2D Pose Estimate" 버튼을 클릭합니다.
2. 지도 상에서 로봇의 예상 위치를 클릭하고 드래그하여 로봇의 방향을 설정합니다. 이때, 클릭한 지점이 로봇의 위치가 되고, 드래그 방향이 로봇의 방향을 나타냅니다.

이 기능은 로봇이 새로운 환경에 처음 진입했을 때, 위치 추정 알고리즘에 초기 추정값을 제공하는 데 매우 중요하며, 로봇이 정확한 내비게이션을 수행하는 데 도움을 줍니다.



#### 5.3.2 2D Nav Goal 수행

RViz2에서 "2D Nav Goal" 기능은 로봇에게 특정 목적지까지 이동하라는 지시를 하는 데 사용됩니다. 이 기능을 통해 사용자는 지도 상에 로봇이 도달해야 할 최종 목적지의 위치와 방향을 지정할 수 있습니다. 이는 주로 로봇 내비게이션 시스템에서 경로 계획과 장애물 회피를 위해 사용됩니다.

"2D Nav Goal" 도구의 작동 방식은 다음과 같습니다:

1. **목적지 지정**: RViz2의 사용자 인터페이스에서 "2D Nav Goal" 버튼을 클릭하면, 사용자는 지도 상에서 로봇이 도달해야 할 목적지를 클릭하고 드래그하여 지정할 수 있습니다.
2. **방향 설정**: 목적지를 클릭한 후 드래그하면, 드래그의 방향이 로봇이 목적지에 도달했을 때 바라보아야 할 방향을 결정합니다.
3. **경로 계획 및 이동**: 목적지와 방향이 지정되면, 로봇의 내비게이션 시스템은 현재 위치에서 목적지까지의 최적 경로를 계산합니다. 이후 로봇은 계산된 경로를 따라 이동하며, 필요에 따라 장애물을 회피합니다.

이 기능은 로봇이 자율적으로 환경을 탐색하고 목적지까지 안전하게 이동하도록 하기 위해 사용됩니다. 로봇이 장애물을 피하고, 효율적인 경로를 선택하며, 정확한 위치에 정확한 방향으로 도착할 수 있도록 지원합니다. "2D Nav Goal"은 주로 로봇이 복잡한 실내 또는 실외 환경에서 목적지까지 내비게이션을 수행해야 할 때 사용됩니다.





## 6. Visual Studio Code로 JaraBot 접속하기

- Visual Studio Code : Extension -> Remote-SSH 설치
- Visual Studio Code에서 SSH로 연결하기 (RPi의 IP주소를 사용한다.)
  - myid@rpi_ip_address 로 연결(ex : ssh jarabot@172.30.1.15)
  - passwd 입력(ex : jarabot)
- Visual Studio Code에서 파일 열기

<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/vc01.png" alt="이미지 대체 텍스트" style="float: left;">

아래의 버튼을 눌러 RPI와 원격접속

<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/VC02.png" alt="이미지 대체 텍스트" style="float: left;">

RPI의 폴더를 선택하여 코드 개발이나 수정

<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/VC03.png" alt="이미지 대체 텍스트" style="float: left;">





+ **Assembly**

  

<img src="https://github.com/firstbot1/jarabot/blob/main/exercise/pic/assembly.png" alt="이미지 대체 텍스트" style="float: left;">
