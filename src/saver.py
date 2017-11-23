#!/usr/bin/env python
import rospy
import json, yaml, datetime
from std_msgs.msg import Int64MultiArray
from geometry_msgs.msg import PoseWithCovarianceStamped
class save_sensors_data():
    
    def __init__(self):
        rospy.init_node('air_sensors_saver', anonymous=True)
        rospy.Subscriber("/sensors", Int64MultiArray, self.callback)
        rospy.Subscriber("/amcl_pose", PoseWithCovarianceStamped, self.get_pos)
        self.position = PoseWithCovarianceStamped()
        now = datetime.datetime.now()
        self.file_name = str(now.year) + "_" + str(now.month) + "_" + str(now.day) + "__" + str(now.hour) + "_" + str(now.minute) + "_" + str(now.second)
        self.save_data = {}
        self.frame = 0

    def get_pos(self, data):
        self.position = data

    def callback(self, data):
        sensors = data.data
        now = datetime.datetime.now()
        self.save_data.update({self.frame:{"hour": now.hour, "minute": now.minute, "second": now.second, 
				"position": yaml.load(str(self.position.pose.pose.position)), 
				"VOC": sensors[0], "CO2": sensors[1], "pm2_5": sensors[2], "pm10": sensors[3]}})
        self.frame+=1
    
    def save(self):
        with open(self.file_name + ".json", 'w') as outfile:
            json.dump(self.save_data, outfile)
            print "file saved"

if __name__ == "__main__":
    try:
        saving = save_sensors_data()
        rospy.spin()
        saving.save()        
    except rospy.ROSInterruptException:
        pass
