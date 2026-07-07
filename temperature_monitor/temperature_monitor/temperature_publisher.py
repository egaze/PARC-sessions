import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

import random

class TemperaturePublisher(Node):
    def __init__(self):
        super().__init__('temperature_publisher')
        self.publisher_ = self.create_publisher(Float32, 'temperature_C', 10)
        timer_period = 2  # seconds
        self.get_logger().info('Temperature publisher started!')
        self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0

    def timer_callback(self):
        msg = Float32()
        temperature = random.uniform(10,50)
        msg.data = temperature

        self.publisher_.publish(msg)

        self.get_logger().info('Pub. Temperature: "%.2f"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    node = TemperaturePublisher()

    rclpy.spin(node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

    