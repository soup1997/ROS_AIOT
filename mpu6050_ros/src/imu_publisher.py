#!/usr/bin/env python

import smbus
import rospy
import time
import tf
from math import pi, atan2, sqrt, radians
import geometry_msgs.msg
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
import __main__

################## get IMU DATA #############################

if not "pwm_time_log" in dir(__main__):
    __main__.pwm_time_log = 0


class axis6:
    address=0x68

    PW_MGMT_1 = 0x6b
    PW_MGMT_2 = 0x6c

    bus = None

    def __init__(self):
        self.bus = smbus.SMBus(8)
        self.bus.write_byte_data(self.address, self.PW_MGMT_1, 0)

    def __del__(self):
        self.bus.close()

    def read_word(self, adr):
        while time.time()-__main__.pwm_time_log<0.05: time.sleep(0.01)
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr+1)
        val = (high << 8) + low
        __main__.pwm_time_log=time.time()
        return val

    def read_word_2c(self, adr):
        #for _ in range(10):
            #try:
        val = self.read_word(adr)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val 

    def getGyro(self, axis=None):
        if type(axis)==str:
            if axis.lower()=="x":
                return self.read_word_2c(0x43)
            elif axis.lower()=="y":
                return self.read_word_2c(0x45)
            elif axis.lower()=="z":
                return self.read_word_2c(0x47)
            else:
                x=self.read_word_2c(0x43)
                y=self.read_word_2c(0x45)
                z=self.read_word_2c(0x47)
                return {"x":x, "y":y, "z":z}
        else:
            x=self.read_word_2c(0x43)
            y=self.read_word_2c(0x45)
            z=self.read_word_2c(0x47)
            return {"x":x, "y":y, "z":z}

    def getAccel(self, axis=None):
        if type(axis)==str:
            if axis.lower()=="x":
                return self.read_word_2c(0x3b)
            elif axis.lower()=="y":
                return self.read_word_2c(0x3d)
            elif axis.lower()=="z":
                return self.read_word_2c(0x3f)
            else:
                x=self.read_word_2c(0x3b)
                y=self.read_word_2c(0x3d)
                z=self.read_word_2c(0x3f)
                return {"x":x, "y":y, "z":z}
        else:
            x=self.read_word_2c(0x3b)
            y=self.read_word_2c(0x3d)
            z=self.read_word_2c(0x3f)
            return {"x":x, "y":y, "z":z}

##################################################

def make_RPY_tf_to_quaternion(value):
    Roll = atan2(value[1] , sqrt(pow(value[0], 2) + pow(value[2], 2)))
    Pitch = atan2(value[0] , sqrt(pow(value[1], 2) + pow(value[2], 2)))
    Yaw = atan2(sqrt(pow(value[0], 2) + pow(value[1], 2)) , value[2])
    result = tf.transformations.quaternion_from_euler(Roll, Pitch, Yaw)
    return result
    
def scaling_data(Accel, Gyro):
    Scaled_Acc = list(map(lambda x: x / 16384.0, Accel))
    Scaled_Gyro = list(map(lambda x: x / 131.0, Gyro)) # max +- 250 degree
    return [Scaled_Acc, Scaled_Gyro]
    
if __name__ == '__main__':
    rospy.init_node('mpu6050')
    rate = rospy.Rate(10.0)
    
    axis_6 = axis6() # mpu6050
    imu_data = Imu()
    
    pub = rospy.Publisher('imu/data', Imu, queue_size = 10)
    
    while not rospy.is_shutdown():
        gyro_val = list(map(float, list((axis_6.getGyro()).values())))
        accel_val = list(map(float, list((axis_6.getAccel()).values())))
        
        scaled_data = scaling_data(accel_val, gyro_val)
        RPY = make_RPY_tf_to_quaternion(scaled_data[0])
        
        imu_data.header.stamp = rospy.Time.now()
        imu_data.header.frame_id = 'base_link'
        imu_data.header.seq = 0
        
        imu_data.orientation.x = RPY[0]
        imu_data.orientation.y = RPY[1]
        imu_data.orientation.z = RPY[2]
        imu_data.orientation.w = RPY[3]
        
        imu_data.linear_acceleration.x = scaled_data[0][0]
        imu_data.linear_acceleration.y = scaled_data[0][1]
        imu_data.linear_acceleration.z = scaled_data[0][2]
        
        imu_data.angular_velocity.x = scaled_data[1][0]
        imu_data.angular_velocity.y = scaled_data[1][1]
        imu_data.angular_velocity.z = scaled_data[1][2]
        
        pub.publish(imu_data)
        rate.sleep()
