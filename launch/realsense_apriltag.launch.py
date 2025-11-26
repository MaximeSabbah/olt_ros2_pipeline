from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # 1) RealSense launch from realsense2_camera
    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("realsense2_camera"),
                "launch",
                "rs_launch.py",
            ])
        ),
        # Optional: you can add launch_arguments here if needed, e.g. disable IMU
        launch_arguments={
            # "enable_gyro": "false",
            # "enable_accel": "false",
            # "unite_imu_method": "none",
        }.items(),
    )

    # 2) AprilTag YAML in olt_ros2_pipeline
    apriltag_params = PathJoinSubstitution([
        FindPackageShare("olt_ros2_pipeline"),
        "config",
        "tags_36h11.yaml",
    ])

    # 3) AprilTag node wired to the RealSense topics
    apriltag_node = Node(
        package="apriltag_ros",
        executable="apriltag_node",
        name="apriltag",
        output="screen",
        remappings=[
            ("image_rect", "/camera/camera/color/image_raw"),
            ("camera_info", "/camera/camera/color/camera_info"),
        ],
        parameters=[apriltag_params],
    )

    return LaunchDescription([
        realsense_launch,
        apriltag_node,
    ])
