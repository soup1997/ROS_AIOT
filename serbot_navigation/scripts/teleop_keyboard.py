#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import sys, select, termios, tty
from geometry_msgs.msg import Twist

msg = '''
Control Your SerBot!
--------------------
Moving Around:
   w
a  s  d
   x
w/x : forward/backward accel velocity
a/d: left/right steering
s: stop

CTRL-C to quit
---------------------
'''
key_mapping = {'w':[0, 0.5], 'x':[0, 0.1], 'a':[-1, 0], 'd':[1, 0], 's':[0, 0]}

def keys_cb(key, twist_pub):
    if len(key) == 0 or not key_mapping.has_key(key):
        return 
    
    vels = key_mapping[key]
    t = Twist()
    t.angular.z= vels[0]
    t.linear.x = vels[1]
    twist_pub.publish(t)
    
def getKey(): 
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1) 
    if rlist: 
        key = sys.stdin.read(1) 
    else: 
        key = '' 
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings) 
    return key 
    
if __name__ == '__main__': 
    print(msg)
    rospy.init_node('teleop_keyboard') 
    settings = termios.tcgetattr(sys.stdin)
    rate = rospy.Rate(10)
    twist_pub = rospy.Publisher('cmd_vel', Twist, queue_size=1) 
    while not rospy.is_shutdown(): 
        key = getKey()
        if (key == '\x03'): 
            break 
        keys_cb(key, twist_pub)
        rate.sleep()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

