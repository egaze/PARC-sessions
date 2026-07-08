from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
from os.path import join


DESCRIPTION_PACKAGE="parcbot_description"
ROBOT_DESCRIPTION=join(get_package_share_directory(DESCRIPTION_PACKAGE), 'urdf', 'parcbot.urdf.xacro')

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

    #rviz2
    rviz = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz",
        output="screen",
        parameters=[{
            'use_sim_true': True
        }]
    )

    #joint_state_publisher_gui
    jsp_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='jsp_gui'
    )

    #robot_state_publisher (rsp)
    rsp = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name='rsp',
        parameters=[{
            'use_sim_time': True,
            'robot_description': ParameterValue(
                Command(['xacro ', ROBOT_DESCRIPTION])
            )
        }]
    )

    # ld.add_action(temperature_node)
    # ld.add_action(listener_node)
    ld.add_action(rviz)
    ld.add_action(jsp_gui)
    ld.add_action(rsp)

    return ld