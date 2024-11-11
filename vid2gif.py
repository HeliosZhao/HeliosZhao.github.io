import cv2
from PIL import Image
import sys
import argparse

def video_to_gif(args):
    video_path = args.video_path
    gif_path = args.gif_path if args.gif_path else video_path.replace(".mp4", ".gif")
    frame_skip = args.frame_skip
    save_ratio = args.save_ratio
    resize = args.resize
    # Open video file
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)  # Frames per second


    frames = []
    frame_count = 0

    # Loop through the video frames
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        # Process every nth frame based on frame_skip
        if frame_count % frame_skip == 0:
            # Convert the frame from BGR (OpenCV format) to RGB (Pillow format)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if resize is not None:
                # resize the shorter side to the specified size
                h, w = rgb_frame.shape[:2]
                if h < w:
                    new_h = resize
                    new_w = int(w * resize / h)
                else:
                    new_w = resize
                    new_h = int(h * resize / w)
                rgb_frame = cv2.resize(rgb_frame, (new_w, new_h))
            # Convert to PIL Image and append to frames list
            frames.append(Image.fromarray(rgb_frame))
        
        frame_count += 1

    # Release the video capture object
    video.release()
    save_num = int(len(frames) * save_ratio)
    frames = frames[:save_num]
    
    total_frames = len(frames)  # Total frame count
    video_duration = total_frames / fps  # Duration in seconds (should be ~10s)
    
    # Calculate how many frames will be used in the GIF
    frames_to_use = total_frames // frame_skip
    
    # Calculate duration per frame in milliseconds to match original video duration
    gif_duration_per_frame = int((video_duration * 1000) / frames_to_use)
    
    # Save frames as GIF
    if frames:
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=gif_duration_per_frame, loop=0)
        print(f"GIF saved at {gif_path}, with each frame displayed for {gif_duration_per_frame} ms.")
    else:
        print("No frames were extracted.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert video to GIF")
    parser.add_argument("-v", "--video_path", help="Path to the video file")
    parser.add_argument("-fs", "--frame_skip", type=int, default=3, help="Number of frames to skip between each frame")
    parser.add_argument("-sr", "--save_ratio", type=float, default=1.0, help="Ratio of frames to save")
    parser.add_argument("-g", "--gif_path", help="Path to save the GIF file", type=str, default=None)
    parser.add_argument("--resize", help="Resize the video to a specific width and height", type=int, default=None)
    args = parser.parse_args()
    # Example usage

    video_to_gif(args)
