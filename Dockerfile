# Use the OSRF ROS Humble Desktop image as the base
FROM osrf/ros:humble-desktop

# Update package lists
RUN apt-get update