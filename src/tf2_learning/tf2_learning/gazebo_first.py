import rclpy

from rclpy.node import Node
from rclpy.qos import (
    QoSProfile,
    QoSReliabilityPolicy,
    QoSHistoryPolicy,
    QoSDurabilityPolicy
)

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

import math
import sympy as sp

class UR5e(Node):

    def __init__(self):

        super().__init__('UR5e')

        qos = QoSProfile(
                reliability=QoSReliabilityPolicy.RELIABLE,
                durability=QoSDurabilityPolicy.VOLATILE,
                history=QoSHistoryPolicy.KEEP_LAST,
                depth=5
            )


        # --- Publishers ---

        self.joint_trajectory_pub = self.create_publisher(
            JointTrajectory,
            '/scaled_joint_trajectory_controller/joint_trajectory',
            qos
        )

        # --- Initial State ---

        self.timer = self.create_timer(
            0.05,
            self.publish_joint_trajectory
        )

    # --- Callbacks ---

    def joint_trajectory_cb(self):
        # Not necessary to have, I just like having it up here, so in case I want to log stuff from that topic, I can make a sub and then 
        # use self.get_logger().info()

        return 0

    # -- Helpers ---


    def IK():
        T = 0
        return T

    def formatNpublish_joint_trajectory(self, positions, velocities, accelerations, efforts):

        msg = JointTrajectory()

        # msg.header.stamp = self.get_clock().now().to_msg()

        msg.joint_names = [
            'shoulder_pan_joint',
            'shoulder_lift_joint',
            'elbow_joint',
            'wrist_1_joint',
            'wrist_2_joint',
            'wrist_3_joint'
        ]

        point = JointTrajectoryPoint()

        point.positions = positions
        point.velocities = velocities
        point.accelerations = accelerations
        point.effort = efforts

        point.time_from_start.sec = 0.05

        msg.points.append(point)

        self.joint_trajectory_pub.publish(msg)


    def publish_joint_trajectory(self):

        self.get_logger().info("Publishing trajectory...")

        self.formatNpublish_joint_trajectory(
            positions=[
                0.0,
                1.492,
                0.0,
                0.0,
                0.0,
                0.0
            ],
            velocities=[],
            accelerations=[],
            efforts=[]
        )

        self.timer.cancel()

# --- Main ---

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