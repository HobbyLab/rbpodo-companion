FROM osrf/ros:humble-desktop-full

# Install build tools and system dependencies
RUN apt update && apt install -y \
    build-essential \
    cmake \
    git \
    sudo \
    ros-humble-ament-cmake \
    ros-humble-joint-state-publisher \
    ros-humble-moveit \
    ros-humble-pluginlib \
    ros-humble-robot-state-publisher \
    ros-humble-ros2-controllers \
    ros-humble-ros2-control \
    ros-humble-rviz2 \
    ros-humble-urdf-launch \
    ros-humble-xacro \
    && rm -rf /var/lib/apt/lists/*

# Set environment
SHELL ["/bin/bash", "-c"]
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

# Clone and build rbpodo
WORKDIR /root
RUN git clone https://github.com/RainbowRobotics/rbpodo.git \
 && mkdir -p rbpodo/build \
 && cd rbpodo/build \
 && cmake -DCMAKE_BUILD_TYPE=Release .. \
 && make -j$(nproc) \
 && make install

# Create ROS2 workspace and clone rbpodo_ros2
RUN mkdir -p /root/rbpodo_ros2_ws/src \
 && cd /root/rbpodo_ros2_ws/src \
 && git clone https://github.com/RainbowRobotics/rbpodo_ros2.git \
 && cd /root/rbpodo_ros2_ws \
 && source /opt/ros/humble/setup.bash \
 && colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release

# Set environment for shell
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc \
 && echo "source /root/rbpodo_ros2_ws/install/setup.bash" >> ~/.bashrc

WORKDIR /root/rbpodo_ros2_ws
CMD ["bash"]