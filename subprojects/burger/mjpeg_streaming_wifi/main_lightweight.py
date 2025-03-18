#!/usr/bin/env python3

from pathlib import Path
import cv2
import depthai as dai
import numpy as np
import time
import blobconverter

def create_pipeline():
    # Create pipeline
    pipeline = dai.Pipeline()

    # --------------------------
    # Stereo & Spatial Branch
    # --------------------------
    # Create mono cameras for stereo depth
    left = pipeline.create(dai.node.MonoCamera)
    left.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    left.setBoardSocket(dai.CameraBoardSocket.LEFT)

    right = pipeline.create(dai.node.MonoCamera)
    right.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
    right.setBoardSocket(dai.CameraBoardSocket.RIGHT)

    # Create StereoDepth node
    stereo = pipeline.createStereoDepth()
    stereo.initialConfig.setConfidenceThreshold(130)
    stereo.initialConfig.setLeftRightCheckThreshold(150)
    stereo.setLeftRightCheck(True)
    stereo.setSubpixel(True)
    stereo.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)

    # Link mono cameras to stereo node
    left.out.link(stereo.left)
    right.out.link(stereo.right)

    # Create SpatialLocationCalculator node
    spatialLocationCalculator = pipeline.create(dai.node.SpatialLocationCalculator)
    spatialLocationCalculator.setWaitForConfigInput(False)
    stereo.depth.link(spatialLocationCalculator.inputDepth)

    # Configure the spatial calculator
    config = dai.SpatialLocationCalculatorConfigData()
    config.depthThresholds.lowerThreshold = 200
    config.depthThresholds.upperThreshold = 15000
    config.calculationAlgorithm = dai.SpatialLocationCalculatorAlgorithm.MIN

    # Set up ROIs for 9 regions
    # First row (i=0,1,2) with fixed top at 0.20, bottom at 0.3
    for i in range(3):
        topLeft = dai.Point2f((i % 3) * 0.3, 0.20)
        bottomRight = dai.Point2f(((i % 3) + 1) * 0.3, (0 + 1) * 0.3)
        config.roi = dai.Rect(topLeft, bottomRight)
        spatialLocationCalculator.initialConfig.addROI(config)

    # Second row (i=3,4,5): from 0.3 to 0.6 vertically
    for i in range(3, 6):
        topLeft = dai.Point2f((i % 3) * 0.3, 1 * 0.3)
        bottomRight = dai.Point2f(((i % 3) + 1) * 0.3, (1 + 1) * 0.3)
        config.roi = dai.Rect(topLeft, bottomRight)
        spatialLocationCalculator.initialConfig.addROI(config)

    # Third row (i=6,7,8): from 0.6 to 0.8 vertically
    for i in range(6, 9):
        topLeft = dai.Point2f((i % 3) * 0.3, 2 * 0.3)
        bottomRight = dai.Point2f(((i % 3) + 1) * 0.3, 0.8)
        config.roi = dai.Rect(topLeft, bottomRight)
        spatialLocationCalculator.initialConfig.addROI(config)

    # XLinkOut node for depth frames
    xoutDepth = pipeline.createXLinkOut()
    xoutDepth.setStreamName("depth")
    spatialLocationCalculator.passthroughDepth.link(xoutDepth.input)

    # XLinkOut node for spatial location data (to host)
    xoutSpatialData = pipeline.createXLinkOut()
    xoutSpatialData.setStreamName("spatialData")
    spatialLocationCalculator.out.link(xoutSpatialData.input)

    # SPIOut node for spatial data
    spiOutSpatialData = pipeline.create(dai.node.SPIOut)
    spiOutSpatialData.setStreamName("spatialData")
    spiOutSpatialData.setBusId(0)
    spiOutSpatialData.input.setBlocking(False)
    spiOutSpatialData.input.setQueueSize(4)
    spatialLocationCalculator.out.link(spiOutSpatialData.input)

    # --------------------------
    # MJPEG Preview Branch
    # --------------------------
    # Create ColorCamera node for video preview/encoding
    cam_color = pipeline.createColorCamera()
    cam_color.setPreviewSize(300, 300)
    cam_color.setVideoSize(640, 480)
    cam_color.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    cam_color.setInterleaved(False)
    cam_color.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

    # Create VideoEncoder node for MJPEG encoding
    videnc = pipeline.createVideoEncoder()
    videnc.setDefaultProfilePreset(640, 480, 30, dai.VideoEncoderProperties.Profile.MJPEG)

    # Link color camera to video encoder
    cam_color.video.link(videnc.input)

    # Create SPIOut node for MJPEG preview
    spiout_preview = pipeline.createSPIOut()
    spiout_preview.setStreamName("spipreview")
    spiout_preview.setBusId(0)
    videnc.bitstream.link(spiout_preview.input)
    spiout_preview.input.setBlocking(False)
    spiout_preview.input.setQueueSize(1)

    return pipeline

if __name__ == '__main__':
    pipeline = create_pipeline()

    # Connect to device and start pipeline
    with dai.Device(pipeline) as device:
        print("Pipeline started. Running combined stereo & preview pipeline...")
        # Optionally, you could read from XLinkOut queues, but here we simply sleep.
        while not device.isClosed():
            time.sleep(1)
