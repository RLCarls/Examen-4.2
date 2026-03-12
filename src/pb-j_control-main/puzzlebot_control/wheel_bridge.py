import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float32
import math

WHEEL_RADIUS = 0.05  # meters — update to your actual wheel radius

class WheelBridge(Node):
    def __init__(self):
        super().__init__('wheel_bridge')
        self.left_pub  = self.create_publisher(Float32, '/motor_left_ref',  10)
        self.right_pub = self.create_publisher(Float32, '/motor_right_ref', 10)
        self.create_subscription(JointState, '/joint_states', self.cb, 10)

    def cb(self, msg: JointState):
        if len(msg.velocity) < 2:
            return
        left  = Float32()
        right = Float32()
        # rad/s → RPM, take absolute value (PID handles magnitude, direction separate)
        left.data  = abs(float(msg.velocity[0])) * 60.0 / (2.0 * math.pi)
        right.data = abs(float(msg.velocity[1])) * 60.0 / (2.0 * math.pi)
        # Clamp to MAX_RPM
        left.data  = min(60.0, left.data)
        right.data = min(60.0, right.data)
        self.left_pub.publish(left)
        self.right_pub.publish(right)

def main():
    rclpy.init()
    rclpy.spin(WheelBridge())

if __name__ == '__main__':
    main()