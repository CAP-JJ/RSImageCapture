import cv2
import numpy as np
import pyrealsense2 as rs
from datetime import datetime
import time

# Set the desired options.
image_directory = "C:/CapturedImages/"
image_file_extension = ".jpg"
timestamp_format = "%H_%M_%S_%f"
feed_horizontal_dimension = 1280
feed_vertical_dimension = 720
feed_color_format = rs.format.bgr8
feed_depth_format = rs.format.z16
frame_rate = 30
wait_time = 1


# Function returning a path name to store each image. Every frame is timestamped.
def get_name():
    path_name = image_directory + datetime.now().strftime(timestamp_format) + image_file_extension
    return path_name


# Initialize RealSense camera
pipeline = rs.pipeline()

# Set the feed configuration
config = rs.config()
# config.enable_stream(rs.stream.depth, feed_horizontal_dimension, feed_vertical_dimension, feed_depth_format, frame_rate)
config.enable_stream(rs.stream.color, feed_horizontal_dimension, feed_vertical_dimension, feed_color_format, frame_rate)
# align = rs.align(rs.stream.depth)

# Start the pipeline
print("[INFO] Starting streaming...")
pipeline.start(config)
print("[INFO] Camera ready.")

# Main loop to pull a frame and store on the specified directory.
while True:
    frames = pipeline.wait_for_frames()
    # aligned_frames = align.process(frames)
    # depth_frame = aligned_frames.get_depth_frame()
    # color_frame = aligned_frames.get_color_frame()

    # Extract a color frame from the incoming frame set.
    color_frame = frames.get_color_frame()
    if not color_frame:
        continue

    # Extract the rgb data from the color frame. This is stored as a NumPy array.
    color_image = np.asanyarray(color_frame.get_data())

    # Generate a path name for the image.
    name = get_name()

    # Write the image to the specified path.
    status = cv2.imwrite(name, color_image)

    # Report the final status of the writing process.
    print(name, status)

    # Wait for a specified duration. This can also be expressed in the shape of frame rates.
    time.sleep(wait_time)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close the feed and report the end of streaming.
# This currently is unreachable due to the infinite loop above.
# But in case of a timed implementation, this would be needed.
print("[INFO] stop streaming ...")
pipeline.stop()
