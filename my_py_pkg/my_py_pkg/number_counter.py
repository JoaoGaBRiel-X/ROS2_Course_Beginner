#! /usr/bin/env python3
import rclpy
from rclpy.node import Node

from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class NumberCounterNode(Node):
    def __init__(self):
        super().__init__("number_counter")
        self.counter_ = 0
        self.publisher_ = self.create_publisher(Int64, "number_count", 10)
        self.subscriber_ = self.create_subscription(Int64, "number", self.callback_number, 10)
        self.reset_counter_service_ = self.create_service(SetBool, "reset_counter", self.callback_reset_number_count)
        self.get_logger().info("Number Counter Publisher has been started.")


    def callback_number(self, msg):
        if msg.data == 29:
            self.counter_ += 1
        new_msg = Int64()
        new_msg.data = self.counter_
        self.publisher_.publish(new_msg)

    def callback_reset_number_count(self, request, response):
        if request.data == True:
            self.counter_ = 0
            self.get_logger().info("Number Counter Zerado!")
            response.success = True
            response.message = "Number counter zerado com sucesso!"
        else:
            response.success = False
            response.message = "Serviço chamado mas não foi zerado o contador!"
        
        return response


def main(args=None):
    rclpy.init(args=args)
    node = NumberCounterNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()