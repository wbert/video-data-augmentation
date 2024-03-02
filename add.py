import os
import cv2
import numpy as np
import random

def apply_add_effect(frame, value=50):
    """
    Apply an "Add" effect to the frame by adding a constant value to each pixel.
    
    Parameters:
        frame (numpy.ndarray): The input frame.
        value (int): The value to add to each pixel. Default is 50.
    
    Returns:
        numpy.ndarray: The frame with the "Add" effect applied.
    """
    # Add the constant value to each pixel
    frame_with_add = cv2.add(frame, np.array([value]))

    return frame_with_add

def apply_add_effect_to_video(video_path, output_path, value=50, num_frames=None):
    """
    Apply an "Add" effect to each frame of the input video and save the result to a new video.
    
    Parameters:
        video_path (str): The path to the input video file.
        output_path (str): The path to save the output video file.
        value (int): The value to add to each pixel. Default is 50.
        num_frames (int): The number of frames to process. If None, process all frames. Default is None.
    """
    # Open video file
    cap = cv2.VideoCapture(video_path)
    
    # Check if the video file was successfully opened
    if not cap.isOpened():
        print(f"Error: Could not open video file '{video_path}'")
        return
    
    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    num_frames_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Determine the number of frames to process
    if num_frames is None:
        num_frames = num_frames_total

    # Create output video
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    # Check if the output video file was successfully created
    if not out.isOpened():
        print(f"Error: Could not create output video file '{output_path}'")
        return

    # Iterate over frames
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: End of video '{video_path}' reached at frame {i + 1}.")
            break

        # Apply "Add" effect to the frame
        frame_with_add = apply_add_effect(frame, value=value)

        # Write the transformed frame to the output video
        out.write(frame_with_add)

        # Print progress
        print(f"Processed frame {i + 1}/{num_frames_total} for video {video_path}")

    # Release video capture and writer
    cap.release()
    out.release()

def process_videos_in_directory(input_dir, output_dir, value=50):
    """
    Apply an "Add" effect to all videos in the input directory and save the results to the output directory.
    
    Parameters:
        input_dir (str): The path to the input directory containing video files.
        output_dir (str): The path to the output directory to save processed videos.
        value (int): The value to add to each pixel. Default is 50.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith((".mp4",".mov")):  # Adjust this condition based on your file types
            input_video_path = os.path.join(input_dir, filename)
            output_video_path = os.path.join(output_dir, filename)
            
            # Apply "Add" effect to the video
            apply_add_effect_to_video(input_video_path, output_video_path, value=value)
            print(f"Add effect applied to {filename}.")

if __name__ == "__main__":
    input_dir = "C:\\Users\\Wilbert\\Desktop\\data\\cleaned\\shooting"
    output_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\shootingadd"

    # Value parameter determines the intensity of the effect
    value = 50  # Adjust as needed, higher values will result in brighter frames
    
    # Process all videos in the input directory
    process_videos_in_directory(input_dir, output_dir, value=value)

    print("All videos processed successfully.")
