import os
import shutil

def copy_videos(source_path, destination_path):
    # Recursively scan all directories and files in the source path
    for root, _, files in os.walk(source_path):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mkv', '.mov')):
                source_file_path = os.path.join(root, file)
                destination_file_path = os.path.join(destination_path, file)

                try:
                    # Copy the file to the destination
                    shutil.copy2(source_file_path, destination_file_path)
                    print(f"Copied: {file}")
                except PermissionError as e:
                    print(f"Permission error for {file}: {e}")

if __name__ == "__main__":
    # Define source and destination paths
    FILEPATH = r'F:\DATASETS\UCF\Anomaly-Videos-Part-3\Anomaly-Videos-Part-3\Shooting'
    FILEDESTINATION = r'F:\data\shooting'

    # Copy videos from source to destination
    copy_videos(FILEPATH, FILEDESTINATION)


