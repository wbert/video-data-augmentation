import os
import cv2
import numpy as np
from skimage.transform import PiecewiseAffineTransform, warp

def apply_piecewise_affine(video_path, output_path, num_frames=None):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    num_frames_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if num_frames is None:
        num_frames = num_frames_total

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    src_points = np.array([[0, 0], [0, height - 1], [width - 1, 0], [width - 1, height - 1]])
    dst_points = np.array([[0, 0], [0, height - 1], [width - 1, 100], [width - 1, height - 101]])

    for i in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break

        transformer = PiecewiseAffineTransform()
        transformer.estimate(src_points, dst_points)
        warped_frame = warp(frame, transformer)
        warped_frame = (warped_frame * 255).astype(np.uint8)

        out.write(warped_frame)

        print(f"Processed frame {i + 1}/{num_frames_total} for video {video_path}")

    cap.release()
    out.release()

def process_video(video_path, output_path):
    apply_piecewise_affine(video_path, output_path)
    print(f"Piecewise Affine Transform applied to {video_path}.")

def process_videos_in_directory(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for filename in os.listdir(input_dir):
        if filename.endswith((".mp4", ".avi", ".mov")):
            input_video_path = os.path.join(input_dir, filename)
            output_video_path = os.path.join(output_dir, filename)
            process_video(input_video_path, output_video_path)

if __name__ == "__main__":
    input_dir = "C:\\Users\\Wilbert\\Desktop\\data\\cleaned\\re"
    output_dir = "C:\\Users\\Wilbert\\Desktop\\data\\augmented\\ree"
    process_videos_in_directory(input_dir, output_dir)
    print("All videos processed successfully.")

