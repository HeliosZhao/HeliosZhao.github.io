import cv2
from PIL import Image

def video_to_gif(video_path, gif_path, frame_skip=3):
    # Open video file
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)  # Frames per second
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Total frame count
    video_duration = total_frames / fps  # Duration in seconds (should be ~10s)
    
    # Calculate how many frames will be used in the GIF
    frames_to_use = total_frames // frame_skip
    
    # Calculate duration per frame in milliseconds to match original video duration
    gif_duration_per_frame = int((video_duration * 1000) / frames_to_use)

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
            # Convert to PIL Image and append to frames list
            frames.append(Image.fromarray(rgb_frame))
        
        frame_count += 1

    # Release the video capture object
    video.release()
    
    # Save frames as GIF
    if frames:
        frames[0].save(gif_path, save_all=True, append_images=frames[1:len(frames)//2], duration=gif_duration_per_frame, loop=0)
        print(f"GIF saved at {gif_path}, with each frame displayed for {gif_duration_per_frame} ms.")
    else:
        print("No frames were extracted.")


# Example usage
video_to_gif("/Users/yyzhao/Desktop/Paper/ICLR-2025/figures/gif-teaser-homepage.mp4", "/Users/yyzhao/Desktop/Paper/ICLR-2025/figures/gif-teaser-homepage.gif", frame_skip=2)
