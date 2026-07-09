from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory
import os
from os.path import join
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource

DESCRIPTION_PACKAGE="parcbot_description"
ROBOT_DESCRIPTION=join(get_package_share_directory(DESCRIPTION_PACKAGE), 'urdf', 'parcbot.urdf.xacro')
BRIDGE_PARAMS=os.path.join(
    get_package_share_directory('bringup_pkg'),
    'config',
    'gz_bridge.yaml'
)

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

    default_world = os.path.join(
        get_package_share_directory('bringup_pkg'),
        'worlds',
        'empty.world.sdf'
    )

    world = LaunchConfiguration('world')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='World to load'
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
        launch_arguments={'gz_args': ['-r ', world], 'on_exit_shutdown':'true'}.items()
    )

    spawn = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'parcbot'],
        output='screen'
    )

    gz_ros_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "--ros-args",
            "-p",
            f"config_file:={BRIDGE_PARAMS}"
        ]
    )

    # ld.add_action(temperature_node)
    # ld.add_action(listener_node)
    ld.add_action(world_arg)
    ld.add_action(gazebo)
    ld.add_action(spawn)
    ld.add_action(rviz)
    ld.add_action(jsp_gui)
    ld.add_action(rsp)
    ld.add_action(gz_ros_bridge)

    return ld