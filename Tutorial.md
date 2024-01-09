# FMCL research assignment with Park JS, Seong YW, Seong WC

## 1. 로봇형 자율 주행 플랫폼 셋팅 방법
### 1.1 raspberry pi 설정
16기가 이상의 micro SD 카드를 준비하고, https://www.raspberrypi.com/software/에서 raspberry pi imager를 다운 후 Ubuntu desktop 22.04.3 LTS를 설치.
이후 micro hdmi to hdmi 선을 사용해 모니터와 연결 후 인터넷 연결 하고 초기 설정 후 다음 코드를 사용하여 git을 설치
````
sudo apt update && sudo apt upgrade
sudo apt install git
````
이후 다음 코드로 해당 파일 다운 및 실행
````
git clone https://github.com/hk416jkt/KMU_COSS_FMCL
cd KMU_COSS_FMCL/install
chmod +x Coss_ROS2_install_rasp.sh
./Coss_ROS2_install_rasp.sh
````
재부팅 이후 다음 코드를 통해 라즈베리파이의 주소 파악 및 라이다 및 아두이노 연결 확인
````
ifconfig
ls /dev/my*
````
![image](https://github.com/hk416jkt/KMU_COSS_FMCL/assets/125014941/04c2f6b6-7072-4852-8337-339dd9929fd9)
위 사진과 같이 뜨면 연결 된 것.
안 된 경우 
````
sudo chmod 666 /dev/ttyUSB0 #또는 sudo chmod 666 /dev/mydriver
sudo chmod 666 /dev/ttyUSB1 #또는 sudo chmod 666 /dev/mylidar
````

### 1.2 PC 설정
Ubuntu desktop 환경을 추천하며, 윈도우에서 시도 시 WSL2를 설정 후 하는 것이 필수. 모두 22.04 버전으로 실행하며, 터미널에서 다음과 같은 코드로 git 및 코드 다운을 한다.
````
sudo apt update && sudo apt upgrade
sudo apt install git
git clone https://github.com/hk416jkt/KMU_COSS_FMCL
cd KMU_COSS_FMCL/install
chmod +x PC_install.sh
./PC_install.sh
````

### 1.3 플랫폼 접속
앞서 파악한 라즈베리파이의 주소를 PC에서 사용해 다음과 같이 접속.
```
ssh FMCL_coss@<rasp-ip> # 라즈베리 파이 주소
```
초기 접속시 yes라고 입력 후 비밀번호 입력.(해당 비밀번호는 ubuntu 세팅 시 사용한 비밀번호)

### 1.4 ROS2 SLAM 실행
원격 접속 터미널을 총 3개 띄운 후 각 터미널에서 다음 코드들을 실행한다.
#### 1번쨰 터미널
````
cd ~/ros2_ws
source install/setup.bash
ros2 launch jarabot_node bringup.launch.py
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
ros2 launch jarabot_node cartographer.launch.py # jarabot 터미널
````
위 코드 실행 후 PC에서 다음 코드를 통해 Rviz2를 실행한다.
#### PC 터미널
````
cd ~/ros2_ws
source install/setup.bash
rviz2 -d ~/ros2_ws/src/jarabot/jarabot_cartographer/rviz/jarabot_cartographer.rviz #local pc 에서 실행
````
이후 다음과 같이 맵을 완성한다. 이때 중요한 것은 맵이 완전히 닫혀 있어야 한다. 그렇지 않을 경우, 추후 경로 생성 시 문제가 생기는 결과가 생길 수 있으므로, 최대한 꼼꼼히 생성한다.
이미지 삽입 하기

#### Map 저장
````
ros2 run nav2_map_server map_saver_cli -f ~/map
````
해당 코드를 꼭 **라즈베리파이 터미널**에서 실행하여 저장한다. 이때 뜨는 맵의 저장 위치를 잘 기억 혹은 복사한다. (리눅스의 터미널에서 복사는 Ctrl + Shift + c, 붙여 넣기는 Ctrl + Shift + v)

### 1.5 nav2 실행하기

#### ssh 터미널 1
````
cd ~/ros2_ws
source install/setup.bash
ros2 launch jarabot_node bringup.launch.py
````
#### ssh 터미널 2
````
cd ~/ros2_ws
source install/setup.bash
ros2 launch jarabot_node navigate.launch.py map:=$HOME/map.yaml #절대경로 사용
# 위 코드가 안될 경우, ros2 launch jarabot_node navigate.launch.py map:=<맵저장위치> 로 시도 
````
#### PC 터미널 1
````
#rviz 설정파일 불러오기
rviz2 -d ~/ros2_ws/src/jarabot/jarabot_navigation2/rviz/jarabot_navigation2.rviz
ros2 run rviz2 rviz2 ~/ros2_ws/src/jarabot/jarabot_navigation2/rviz/jarabot_navigation2.rviz
````
이후 다음 화면에서 초기 위치를 지정. 너무 다르게만 지정하지 않으면 되고, 너무 세세히 하지 않아도 해당 오차를 nav2 플러그인에서 계산한다.




