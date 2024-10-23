# AirSim Multirotor API Commands

This document provides a brief overview of the key commands available in the **AirSim Multirotor API**. These commands enable control of a drone, including movement, state management, and sensor interactions.

## Table of Contents
1. [Basic Drone Control](#1-basic-drone-control)
2. [Movement Commands](#2-movement-commands)
3. [Rotation Commands](#3-rotation-commands)
4. [Gimbal Control](#4-gimbal-control)
5. [Waypoint Navigation](#5-waypoint-navigation)
6. [Return Home](#6-return-home)
7. [State and Sensor Information](#7-state-and-sensor-information)
8. [Control and Arm](#8-control-and-arm)
9. [Miscellaneous](#9-miscellaneous)

## 1. Basic Drone Control

- **`takeoffAsync()`**: Commands the drone to take off asynchronously.
- **`landAsync()`**: Commands the drone to land asynchronously.
- **`hoverAsync()`**: Commands the drone to hover in place.

## 2. Movement Commands

- **`moveByVelocityAsync(vx, vy, vz, duration)`**: Moves the drone with specified velocities along the X, Y, and Z axes for a set duration.
- **`moveByVelocityZAsync(vx, vy, z, duration)`**: Moves the drone at a constant altitude `z` with velocities along the X and Y axes.
- **`moveByAngleRatesZAsync(roll_rate, pitch_rate, yaw_rate, z, duration)`**: Moves the drone using roll, pitch, and yaw rates, while maintaining altitude `z`.
- **`moveToZAsync(z, velocity)`**: Moves the drone to a specific altitude `z` at the given velocity.
- **`moveToPositionAsync(x, y, z, velocity)`**: Moves the drone to the specified X, Y, Z coordinates at the given velocity.
- **`moveByRollPitchYawZAsync(roll, pitch, yaw, z, duration)`**: Controls the drone's movement using roll, pitch, yaw commands while maintaining a set altitude `z`.
- **`moveByRollPitchYawThrottleAsync(roll, pitch, yaw, throttle, duration)`**: Moves the drone based on roll, pitch, yaw, and throttle inputs.

## 3. Rotation Commands

- **`rotateByYawRateAsync(yaw_rate, duration)`**: Rotates the drone at a specified yaw rate (degrees/sec) for a set duration.
- **`rotateToYawAsync(yaw)`**: Rotates the drone to a specific yaw angle.
- **`rotateByYawPitchRollAsync(yaw, pitch, roll)`**: Rotates the drone using yaw, pitch, and roll inputs.

## 4. Gimbal Control

- **`moveToGimbalPoseAsync(pitch, roll, yaw)`**: Adjusts the drone's gimbal (camera) to specific pitch, roll, and yaw angles.

## 5. Waypoint Navigation

- **`moveOnPathAsync(path, velocity)`**: Moves the drone along a predefined path (waypoints) at the given velocity.
- **`moveToWaypointAsync(x, y, z, velocity)`**: Moves the drone to a specific waypoint at X, Y, Z coordinates at a given velocity.

## 6. Return Home

- **`goHomeAsync()`**: Commands the drone to return to its home position (usually where it took off).

## 7. State and Sensor Information

- **`getMultirotorState()`**: Returns the drone’s current state (position, velocity, orientation, etc.).
- **`getGpsData()`**: Retrieves the current GPS data (latitude, longitude, altitude).
- **`getImuData()`**: Retrieves IMU (Inertial Measurement Unit) sensor data, including acceleration and orientation.
- **`getLidarData()`**: Retrieves data from the drone's LiDAR sensor.
- **`getBarometerData()`**: Retrieves the current altitude and pressure data from the drone's barometer.
- **`getCameraImage()`**: Captures an image from the specified camera on the drone.

## 8. Control and Arm

- **`enableApiControl(is_enabled)`**: Enables or disables API control of the drone.
- **`armDisarm(is_armed)`**: Arms or disarms the drone. Arming is necessary before flight.

## 9. Miscellaneous

- **`reset()`**: Resets the drone to its initial state.
- **`pauseAsync()`**: Pauses the simulation.
- **`continueAsync()`**: Resumes a paused simulation.
