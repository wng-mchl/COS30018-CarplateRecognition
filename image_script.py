import cv2
import os
from concurrent.futures import ThreadPoolExecutor

# Configuration
INPUT_VIDEOS_DIR = "Test"     
OUTPUT_FRAMES_DIR = "all_frames"     
SECONDS_INTERVAL = 10                
MAX_WORKERS = 2                    

def process_video(video_file):
    video_path = os.path.join(INPUT_VIDEOS_DIR, video_file)
    video_name = os.path.splitext(video_file)[0]
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"vid bad ")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:  

        fps = 30
    
    frames_to_skip = int(fps * SECONDS_INTERVAL)



    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frames_to_skip == 0:

            frame_filename = os.path.join(

                OUTPUT_FRAMES_DIR, 



                f"{video_name}_frame_{frame_count:04d}.jpg"
            )


            cv2.imwrite(frame_filename, frame)  # Full quality save

        frame_count += 1


    cap.release()
    print(f"Finished: {video_file} (extracted {frame_count // frames_to_skip} frames)")

def main():
    os.makedirs(OUTPUT_FRAMES_DIR, exist_ok=True)
    
    video_files = [
        f for f in os.listdir(INPUT_VIDEOS_DIR) 
        if f.lower().endswith((".mp4", ".ts"))
    ]

    if not video_files:
        print(f"no videos in {INPUT_VIDEOS_DIR}!")
        return

    # Process videos in parallel
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(process_video, video_files)

    print(f"\nsaved to: {os.path.abspath(OUTPUT_FRAMES_DIR)}")

if __name__ == "__main__":
    main()
