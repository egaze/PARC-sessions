from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    # publisher node
    temperature_node = Node(
        package="temperature_monitor",
        executable="readings",
    )

    #  subscriber node
    listener_node = Node(
        package="temperature_monitor",
        executable="subscriber",
    )


    ld.add_action(temperature_node)
    ld.add_action(listener_node)

    return ld