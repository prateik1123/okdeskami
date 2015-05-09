# -*- coding: utf-8 -*-

"""
GetSonsorData.py
Subscribe sensor data and save them as CSV file.
"""

import sys
import numpy as np
import paho.mqtt.client as mqtt


#This method is called when mqtt is connected.
def on_connect(client, userdata, flags, rc):
    print('Connected with result code '+str(rc))
    client.subscribe("SLAM/input/#")


#Append new data array to the array.
def appendData(data):
	global isFirst
	global time
	global accel, linear_accel, gravity, gyro, magnet, orientation

	if(isFirst):
		time = long(data[0])

	accel0 = np.array([long(data[0])-time,float(data[1]),float(data[2]),float(data[3])])

	if(isFirst):
		accel = accel0
		isFirst = False
	else:
		accel = np.c_[accel, accel0]


#This method is called when message is arrived.
def on_message(client, userdata, msg):
	global isFirst
	global time
	global accel, linear_accel, gravity, gyro, magnet, orientation

    #print(msg.topic + ' ' + str(msg.payload))

	data = str(msg.payload).split('&')
    #Append data to the array
	if(str(msg.topic) == "SLAM/input/all"):
		appendData(data)
	elif(str(msg.topic) == "SLAM/input/stop"):
		np.savetxt('./data/accel.csv', accel, delimiter=',')
		#np.savetxt('./data/gravity.csv', gravity, delimiter=',')
		#np.savetxt('./data/gyro.csv', gyro, delimiter=',')
		#np.savetxt('./data/magnet.csv', magnet, delimiter=',')
		#np.savetxt('./data/orientation.csv', orientation, delimiter=',')
		sys.exit()


#Main method
if __name__ == '__main__':

	#global variables
	isFirst = True
	time = 0
	accel = np.array([])
	linear_accel = np.array([])
	gravity = np.array([])
	gyro = np.array([])
	magnet = np.array([])
	orientation = np.array([])

	#Mqtt
	username = 'admin'
	password = 'password'
	host = 'vps01.t-spots.jp'
	port = 61713

	#Mqtt connect
	client = mqtt.Client(client_id="GetSensorData", clean_session=True, protocol=mqtt.MQTTv311)
	client.on_connect = on_connect
	client.on_message = on_message
	client.username_pw_set(username, password=password)
	client.connect(host, port=port, keepalive=60)
	client.loop_forever()