import os
import cv2
import numpy as np

def apply_superpixel(video_path, output_path, num_frames=None):
    # Open video file
    cap = cv2.VideoCapture(video_path)
    
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

    # Calculate number of superpixels based on frame dimensions
    num_superpixels = int((width * height) ** 0.5 / 4)

    # Iterate over frames
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Apply Superpixel Segmentation
        slic = cv2.ximgproc.createSuperpixelSLIC(frame, cv2.ximgproc.SLICO, num_superpixels)
        slic.iterate()
        mask = slic.getLabelContourMask()
        superpixel_frame = cv2.bitwise_and(frame, frame, mask=mask)

        # Write the transformed frame to the output video
        out.write(superpixel_frame)

        # Print progress
        print(f"Processed frame {i + 1}/{num_frames_total} for video {video_path}")

    # Release video capture and writer
    cap.release()
    out.release()

def process_videos_in_directory(input_dir, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith((".mp4",".mov")):  # Adjust this condition based on your file types
            input_video_path = os.path.join(input_dir, filename)
            output_video_path = os.path.join(output_dir, filename)
            
            # Apply Superpixel Transform to the video
            apply_superpixel(input_video_path, output_video_path)
            print(f"Superpixel Transform applied to {filename}.")

if __name__ == "__main__":
    input_dir = "C:\\Users\\Wilbert\\Desktop\\data\\cleaned\\assault"
    output_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\assaultpix"

    # Process all videos in the input directory
    process_videos_in_directory(input_dir, output_dir)

    print("All videos processed successfully.")

