#!/usr/bin/env python3
"""
Test publisher that uses BEST_EFFORT QoS.

Without the QoS override patch, rqt_topic defaults to RELIABLE and cannot
subscribe to this topic. With the patch, rqt_topic overrides its subscriber
QoS to match the publisher.

Usage:
    ros2 run rqt_topic test_qos_publisher
    # or
    python3 scripts/test_qos_publisher.py
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy
from std_msgs.msg import String


class TestQosPublisher(Node):

    def __init__(self):
        super().__init__('test_qos_publisher')

        # Sensor-data-like QoS: BEST_EFFORT, VOLATILE, depth 1
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=1,
        )

        self.publisher = self.create_publisher(String, '/test_qos_topic', qos)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.count = 0

        self.get_logger().info(
            'Publishing /test_qos_topic with BEST_EFFORT QoS. '
            'Run `ros2 topic info /test_qos_topic --verbose` to inspect.'
        )

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello {self.count}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Published: {msg.data}')
        self.count += 1


def main(args=None):
    rclpy.init(args=args)
    node = TestQosPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
