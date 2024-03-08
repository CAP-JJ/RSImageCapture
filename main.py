import cv2
import numpy as np
import pyrealsense2 as rs
from datetime import datetime
import time


def get_name():
    path_name = "C:/CapturedImages/" + datetime.now().strftime("%H_%M_%S_%f") + ".jpg"
    return path_name


# Initialize RealSense camera
wait_time = 1
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
# align = rs.align(rs.stream.depth)

print("[INFO] Starting streaming...")
pipeline.start(config)
print("[INFO] Camera ready.")

while True:
    frames = pipeline.wait_for_frames()
    # aligned_frames = align.process(frames)
    # depth_frame = aligned_frames.get_depth_frame()
    # color_frame = aligned_frames.get_color_frame()
    color_frame = frames.get_color_frame()
    if not color_frame:
        continue

    color_image = np.asanyarray(color_frame.get_data())

    name = get_name()
    status = cv2.imwrite(name, color_image)
    print(name, status)
    time.sleep(wait_time)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


print("[INFO] stop streaming ...")
pipeline.stop()
