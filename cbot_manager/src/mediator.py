import rospy
import serial, time
from cbot_ros_msgs.msg import *
from cbot_ros_msgs.srv import *

rospy.init_node("mediator")

ser = serial.Serial("/home/mohit/nio/src/GUI-read",timeout=0.01,baudrate=9600, rtscts=True, dsrdtr=True)
controlClient = rospy.ServiceProxy("/controller_inputs", ControllerInputs)
thrusterClient = rospy.ServiceProxy("/thruster_control", ThrusterControl)
thrPub = rospy.Publisher("/Thrusters",ThrusterData,queue_size=10)

message = {}

safetyParams = {"MaxDepth": 10,"MaxPitch":15, "MaxVelocity": 1}

sendData = {"Battery": 100, "Latitude": 15.4507, "Longitude": 73.8041, "Speed": 0.0, "Course": 0.0, "Roll": 0.0, "Pitch":0.0, "Yaw":0.0}

heartbeatCount = 5
lastHearbeatTime = time.time()

def ahrsCallback(data):
	global sendData
	sendData["Roll"] = round(data.Roll,2)
	sendData["Pitch"] = round(data.Pitch,2)
	sendData["Yaw"] = round(data.YawAngle,2)

def gpsCallback(data):
	global sendData
	sendData["Latitude"] = round(data.latitude,5)
	sendData["Longitude"] = round(data.longitude,5)
	sendData["Course"] = round(data.course,2)
	sendData["Speed"] = round(data.vel,2)

def getData():
	global lastHearbeatTime, heartbeatCount
	line = ser.readline().strip().split(',')
	if(line[0]=="GUI"):
		for data in line:
			data = data.strip().split(":")
			if(len(data)==2):
				if(data[1]!="null"):
					message[data[0].strip()] = float(data[1].strip())
		print(message)
		parseData()
	if(line[0] == "GUIHEARTBEAT"):
		lastHearbeatTime = time.time()
		heartbeatCount = 5


def updateSafetyParams():
	for param in safetyParams:
		if(rospy.has_param(param)):
			safetyParams[param] = rospy.get_param(param)
		else:
			print(param + " not set")

def parseData():
	if(rospy.has_param("Controller_ON")):
		rospy.set_param("Controller_ON",message["CONTROLLER_ON"])
	else:
		print("Controller not set")
	if(rospy.has_param("GUIDANCE_ON")):
		rospy.set_param("GUIDANCE_ON",message["GUIDANCE_ON"])
	else:
		print("GUIDANCE not set")
	if(rospy.has_param("HIL_ON")):
		rospy.set_param("HIL_ON",message["THRUSTERS_ON"])
	else:
		print("THRUSTERS not set")

	if(message["GUIDANCE_ON"]):
		pass
	elif(message["CONTROLLER_ON"]):
		ctr = ControllerInputsRequest()
		if(rospy.has_param("HeadingCtrl")):
			rospy.set_param("HeadingCtrl",message["HeadingControlON"])
		else:
			print("Heading Control not set")

		if(rospy.has_param("VelocityCtrl")):
			rospy.set_param("VelocityCtrl",message["SpeedControlON"])
		else:
			print("Velocity Control not set")

		if(rospy.has_param("PitchCtrl")):
			rospy.set_param("PitchCtrl",message["PitchControlON"])
		else:
			print("Pitch Control not set")

		if(rospy.has_param("DepthCtrl")):
			rospy.set_param("DepthCtrl",message["DepthControlON"])
		else:
			print("Depth Control not set")		

		if(message["HeadingControlON"]):
			ctr.desired_heading = float(message['HCtrl'])
			print(message['HCtrl'])
		if(message["PitchControlON"]):
			ctr.desired_pitch = float(message['PCtrl'])
		if(message["DepthControlON"]):
			ctr.desired_depth = float(message['DCtrl'])
		if(message["SpeedControlON"]):
			ctr.desired_u = float(message['SCtrl'])
		controllerResp = controlClient(ctr)

	elif(message["THRUSTERS_ON"]):
		if(message["Thruster_M1"]):
			thr = ThrusterData()
			thr.T1 = message["T1"]
			thr.T2 = message["T2"]
			thr.T3 = message["T3"]
			thr.T4 = message["T4"]
			thrPub.publish(thr)
		elif(message["Thruster_M2"]):
			thr = ThrusterControlRequest()
			thr.comm_mode_F = float(message["CMFCtrl"])
			thr.diff_mode_F = float(message["DMFCtrl"])
			thr.comm_mode_V = float(message["CMVCtrl"])
			thr.diff_mode_V = float(message["DMVCtrl"])
			thr.update = 1
			thrusterClient(thr)
	# if(message["Compile"]!="")

def Timer():
	global heartbeatCount, lastHearbeatTime
	timeElapsed = time.time() - lastHearbeatTime
	timeout = 0
	try:
		timeout = float(message["HeartTimeout"])
	except:
		timeout = float("inf")
	if(heartbeatCount>0 and timeElapsed<float(timeout)):
		return
	elif(heartbeatCount>0 and timeElapsed>float(timeout)):
		lastHearbeatTime = time.time()
		heartbeatCount-=1
		return
	else:
		print("/////////////")
		print("GUI Heartbeat Timeout\n Setting Thrusters OFF")
		rospy.set_param("/HIL_ON",0)
		while(timeElapsed>timeout):
			getData()
			timeElapsed = time.time() - lastHearbeatTime
		print("GUI Heartbeat Recieved\n You can set Thrusters ON manually")
		return

def sendStatusUpdate():
	global sendData
	message = "MED,"
	for param in sendData:
		message += param + ":" + str(sendData[param]) + ","
	message += "\r\n"
	ser.flushOutput()
	ser.write(bytes(message))

if __name__ == "__main__":
	while not rospy.is_shutdown():
		rospy.Subscriber("/AHRS",AHRS,ahrsCallback)
		rospy.Subscriber("/GPS",GPS,gpsCallback)
		Timer()
		# try:
		updateSafetyParams()
		getData()
		sendStatusUpdate()
			# print(message)
		# except:
		# 	print("Could not parse GUI data")