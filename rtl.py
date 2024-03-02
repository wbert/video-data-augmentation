import os
from moviepy.editor import VideoFileClip, ImageSequenceClip
import numpy as np

def flip_video_lr(video_path):
    # Load video clip
    video_clip = VideoFileClip(video_path)
    
    # List to store processed frames
    processed_frames = []
    
    # Iterate over each frame
    for frame in video_clip.iter_frames():
        # Flip frame horizontally
        processed_frame = np.fliplr(frame)
        processed_frames.append(processed_frame)
    
    # Close the original clip
    video_clip.close()
    
    # Convert processed frames to a new video clip
    processed_clip = ImageSequenceClip(processed_frames, fps=video_clip.fps)
    
    return processed_clip

if __name__ == "__main__":
    input_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\shooting"  # Specify the input directory containing videos
    output_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\shooting0"  # Specify the output directory for processed videos

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".mov"):  # Adjust this condition based on your file types
            input_video_path = os.path.join(input_dir, filename)
            output_video_path = os.path.join(output_dir, filename)
            
            # Flip the video
            processed_clip = flip_video_lr(input_video_path)
            
            # Save the processed video
            processed_clip.write_videofile(output_video_path, codec="libx264")

    print("All videos processed successfully.")

