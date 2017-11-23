#!/usr/bin/env python
import rospy
from std_msgs.msg import Int64, Int64MultiArray
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray


markerArray = MarkerArray()
marker = Marker()
marker.header.frame_id = "/map"
marker.type = marker.CYLINDER
marker.scale.x = 0.2
marker.scale.y = 0.2
marker.color.a = 1.0
marker.pose.orientation.w = 1.0
marker.pose.position.z = 0.0
marker.action = marker.ADD
id = 0

def voc_callback(data):
    global id
    marker.id = id
    id += 1
    marker.scale.z = data.data / 91.6
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 0.0
    marker.pose.position.x = 1.0
    marker.pose.position.y = 0.0
    markerArray.markers.append(marker)
    pub.publish(markerArray)

def coo_callback(data):
    global id
    marker.id = id
    id += 1
    marker.scale.z = data.data / 200.0
    marker.color.r = 1.0
    marker.color.g = 0.0
    marker.color.b = 1.0
    marker.pose.position.x = -1.0
    marker.pose.position.y = 0.0
    markerArray.markers.append(marker)
    pub.publish(markerArray)

def pm2_5_callback(data):
    global id
    marker.id = id
    id += 1
    marker.scale.z = data.data / 1.0
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0
    marker.pose.position.x = 0.0
    marker.pose.position.y = 1.0
    markerArray.markers.append(marker)
    pub.publish(markerArray)

def pm10_callback(data):
    global id
    marker.id = id
    id += 1
    marker.scale.z = data.data / 1.0
    marker.color.r = 0.0
    marker.color.g = 0.0
    marker.color.b = 1.0
    marker.pose.position.x = 0.0
    marker.pose.position.y = -1.0
    markerArray.markers.append(marker)
    pub.publish(markerArray)

def pub_marker(sensor, Id, position):
    marker.id = Id
    marker.scale.z = sensor 
    marker.color.r = 0.0
    marker.color.g = 0.0
    marker.color.b = 1.0
    marker.pose.position.x = position[0]
    marker.pose.position.y = position[1]
    markerArray.markers.append(marker)
    pub.publish(markerArray)

def callback(data):
    sensors = data.data
    global id
    for sensor in sensors:
        pub_marker(sensor, id, position):
        id += 1
    

if __name__ == '__main__':
    try:
        rospy.init_node('air_sensors_markers_publisher', anonymous=True)
        pub = rospy.Publisher('air_sensors', MarkerArray, queue_size=10)
        rospy.Subscriber('/VOC', Int64, voc_callback)
        rospy.Subscriber('/CO2', Int64, coo_callback)
        rospy.Subscriber('/pm2_5', Int64, pm2_5_callback)
        rospy.Subscriber('/pm10', Int64, pm10_callback)
        rospy.Subscriber('/sensors', Int64MultiArray, callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
