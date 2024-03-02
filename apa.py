import os
import cv2
import numpy as np
from skimage.transform import PiecewiseAffineTransform, warp

def apply_piecewise_affine(video_path, output_path, num_frames=None):
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

    # Iterate over frames
    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break

        # Define control points for the transformation
        src_points = np.array([[0, 0], [0, height - 1], [width - 1, 0], [width - 1, height - 1]])
        dst_points = np.array([[0, 0], [0, height - 1], [width - 1, 100], [width - 1, height - 101]])

        # Apply Piecewise Affine Transform
        transformer = PiecewiseAffineTransform()
        transformer.estimate(src_points, dst_points)
        warped_frame = warp(frame, transformer)

        # Convert frame to uint8 for writing
        warped_frame = (warped_frame * 255).astype(np.uint8)

        # Write the transformed frame to the output video
        out.write(warped_frame)

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
        if filename.endswith(".mp4"):  # Adjust this condition based on your file types
            input_video_path = os.path.join(input_dir, filename)
            output_video_path = os.path.join(output_dir, filename)
            
            # Apply Piecewise Affine Transform to the video
            apply_piecewise_affine(input_video_path, output_video_path)
            print(f"Piecewise Affine Transform applied to {filename}.")

if __name__ == "__main__":
    input_dir = "C:\\Users\\Wilbert\\Desktop\\data\\cleaned\\theft"
    output_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\theft"

    # Process all videos in the input directory
    process_videos_in_directory(input_dir, output_dir)

    print("All videos processed successfully.")

