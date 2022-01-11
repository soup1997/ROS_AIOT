#!/usr/bin/env python3

import rospy
from pop import Pilot
import time
from geometry_msgs.msg import Twist

bot = Pilot.SerBot()

def callback(msg):
    global bot
    
    ####### Deciding Steering Angle #########
    if 0.18 < msg.angular.z <= 0.5: # left Direction
        bot.setSpeed(30)
        bot.steering = 0.1
        print('Left Direction')
    
    elif -0.18 > msg.angular.z >= -0.5: # right Direction
        bot.setSpeed(30)
        bot.steering = -0.1
        print('Right Direction')
    
    elif -0.18 <=msg.angular.z <= 0.18: # go forward
        bot.setSpeed(35)
        bot.steering = 0
        print("Go Straight")
    
    elif 0.5 < msg.angular.z < 0.8:
        bot.setSpeed(25)
        bot.steering = 0.2
        print('Left Direction <<<<<<<')
    
    elif -0.8 < msg.angular.z < -0.5:
        bot.setSpeed(25)
        bot.steering = -0.2 
        print('Right Direction >>>>>>')
        
    else:
        pass
    #########################################
    
    if msg.linear.x >= 0:
        bot.forward()
        
    elif msg.linear.x == 0 and msg.angular.z >= 0.8:
        bot.setSpeed(20)
        bot.turnLeft()
        print("Turn Left")
        
    elif msg.linear.x == 0 and msg.angular.z <= -0.8:
        bot.setSpeed(20)
        bot.turnRight()
        print("Turn Right")
            
    else:
        bot.stop()
        print("Stop")
    
    print('')
    
if __name__ == '__main__':
    rospy.init_node('SerBot', disable_signals = True)
    rospy.loginfo(rospy.get_name())
    print("Navigation Start Now!")
    rospy.Subscriber('cmd_vel', Twist, callback)
    rospy.spin()
