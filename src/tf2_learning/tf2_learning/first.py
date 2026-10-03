import rclpy

from rclpy.node import Node
from rclpy.qos import (
    QoSProfile,
    QoSReliabilityPolicy,
    QoSHistoryPolicy,
    QoSDurabilityPolicy
)

from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import JointState

import math

class UR5e(Node):

    def __init__(self):

        super().__init__('UR5e')

        qos = QoSProfile(
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.VOLATILE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=5
        )

        qos_jointStates = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            durability=QoSDurabilityPolicy.VOLATILE,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=5
        )

        # Publishers

        self.goal_pub = self.create_publisher(
            PoseStamped,
            '/goal_pose',
            qos
        )

        self.joint_pub = self.create_publisher(
            JointState,
            '/joint_states',
            qos
        )

        # Subscribers

        self.create_subscription(
            PoseStamped,
            '/goal_pose', 
            self.pose_cb,
            qos
        )

        # --- Initial State ---

        self.x = 0
        self.y = 0
        self.z = 0

        self.direction = 1.0
        self.angle = 0.0

        self.timer = self.create_timer(
            0.05,
            self.publish_test_joint_state
        )

    def publish_goal(self, x, y, z, qx, qy, qz, qw):

        msg = PoseStamped()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        msg.pose.position.x = float(x)
        msg.pose.position.y = float(y)
        msg.pose.position.z = float(z)

        # For orientation, it expects a quaternion as [x, y, z, w]
        # Passing an identity quaternion atm
        msg.pose.orientation.x = float(qx)
        msg.pose.orientation.y = float(qy)
        msg.pose.orientation.z = float(qz)
        msg.pose.orientation.w = float(qw)

        #self.goal_pub.publish(msg)

    def publish_joint_state(self, name, position, velocity, effort):

        msg = JointState()

        msg.header.stamp = self.get_clock().now().to_msg()

        msg.name = name
        msg.position = position
        msg.velocity = velocity
        msg.effort = effort

        self.joint_pub.publish(msg)

    def publish_test_goal(self):

        self.angle += math.radians(2.0)

        # Rotation about Z axis
        qx = 0.0
        qy = 0.0
        qz = math.sin(self.angle / 2.0)
        qw = math.cos(self.angle / 2.0)

        self.publish_goal(
            0.0,
            0.0,
            0.0,
            qx,
            qy,
            qz,
            qw
        )

    def publish_test_joint_state(self):

        self.angle += math.radians(2.0)

        if self.angle > math.pi:
            self.angle = -math.pi

        self.publish_joint_state(
        [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ],
        [
            self.angle,
            self.angle,
            self.angle,
            self.angle,
            self.angle,
            self.angle
        ],
        [
            0.0,
            0.1,
            0.0,
            0.0,
            0.0,
            0.0
            ],
        []
    )

    def transform(self, msg):
        
        return 0


    def pose_cb(self, msg):

        self.get_logger().info(
            f"x = {msg.pose.orientation.x} | "
            f"y = {msg.pose.orientation.y} | "
            f"z = {msg.pose.orientation.z}"
        )


def main(args=None):
    rclpy.init(args=args)

    node = UR5e()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        node.get_logger().info(
            "Minimal shutting down."
        )

    finally:

        node.destroy_node()

        rclpy.shutdown()

if __name__ == '__main__':
    main()