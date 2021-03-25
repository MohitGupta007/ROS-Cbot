# C-Bot
The coral-reef monitoring bot (C-Bot) is an unmanned underwater vehicle developed by the Marine Instrumentation Department, CSIR-National Institute of Oceaography, Dona Paula, Goa.

# ROS-CBOT
This repository contains the software to be used on CBOT. It contains the algorithms for control, guidance and mission planning.

#### The C-Bot has following capabilities:
1. Heading Control
2. Depth Control
3. Altitude Control
4. Way Point Guidance
5. Path following of straight line and sectors of arc in the presence of oceanic currents
6. Navigation - Dead Reckoning, Acoustic based use range and bearing from iUSBL and Rnage only based navigation.
7. Docking uisng acoustics and vision
8. Capabale of self docking and release can be deployed for 6 months with one survey mission per month, and static monitoring twice a day while docked.


## Pre-requisites
This assumes that you have ROS-Kinetic or ROS-Melodic installed on your machine. 

You should have the following packages installed:
1. UUV-Simulator (provide link)
2. CBOT-Gazebo (provide link)
3. ros_rtsp (provide link)
4. CBOT-GCS (provide link)

## Installation instructions
- Create a workspace:
```
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws
$ catkin init  # initialize your catkin workspace
```
The src should also contain the previously mentioned packages.

- Clone this repository:
```
$ git clone https://github.com/MohitGupta007/ROS-Cbot.git
```

- Create a ports.sh file to open the virtual serial ports(required for software in the loop simulation when not using real hardware).
```
socat PTY,link=/tmp/gps-write,raw,echo=0 PTY,link=/tmp/gps-read,raw,echo=0&
echo "GPS port ready: gps-write, gps-read"
sleep 0.1

socat PTY,link=/tmp/ahrs-write,raw,echo=0 PTY,link=/tmp/ahrs-read,raw,echo=0&
echo "AHRS port ready: ahrs-write, ahrs-read"
sleep 0.1

socat PTY,link=/tmp/thr-write,raw,echo=0 PTY,link=/tmp/thr-read,raw,echo=0&
echo "Thruster port ready: thr-write, thr-read"
sleep 0.1

echo "GUI port ready: GUI-write, GUI-read"
socat PTY,link=/tmp/GUI-write,raw,echo=0 PTY,link=/tmp/GUI-read,raw,echo=0
```

## Running the package
- Run the ports.sh file by running:
```
$ bash ports.sh 
```

- Run the CBOT-Gazebo package to launch the UUV in Gazebo environment. See the repo for more information.
```
$ roslaunch cbot_description upload_cbot.launch 
```

- Run this repositiory
```
$ roslaunch cbot cbot.launch
```

#### Developers:
1. Pramod Maurya,
2. Lakshadeep Naik
3. Mohit Sushil Gupta
