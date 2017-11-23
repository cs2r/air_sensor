#!/usr/bin/env python
import serial
import rospy
from std_msgs.msg import Int64, Int64MultiArray


def publisher():
    sensor1 = serial.Serial('/dev/ttyACM0', 57600)
    voc_pub = rospy.Publisher('VOC', Int64, queue_size=10)
    coo_pub = rospy.Publisher('CO2', Int64, queue_size=10)
    pm2_5_pub = rospy.Publisher('pm2_5', Int64, queue_size=10)
    pm10_pub = rospy.Publisher('pm10',Int64 , queue_size=10)
    sensors_pub = rospy.Publisher('sensors',Int64MultiArray , queue_size=10)
    rospy.init_node('air_sensors_publisher', anonymous=True)
    rate = rospy.Rate(0.5) 
    print "CO2 and VOC publisher started"
    sensors_data = Int64MultiArray()
    while not rospy.is_shutdown():
	try:
		voc = sensor1.readline()
		voc_pub.publish(int(voc))
		co2 = sensor1.readline()
		coo_pub.publish(int(co2))
		pm2_5 = sensor1.readline()
		pm2_5_pub.publish(int(pm2_5))
		pm10 = sensor1.readline()
		pm10_pub.publish(int(pm10))
                sensors_data.data = [int(voc), int(co2), int(pm2_5), int(pm10)]
                sensors_pub.publish(sensors_data)
        except ValueError:
            print "error type"
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass
