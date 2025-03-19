import os
import json
import logging
import ffmpeg
from PIL import Image

class InputManager:
    def __init__(self):
        self.max_duration = 600  # 10 minutes
        self.min_resolution = {"width": 640, "height": 480}
        self.target_resolution = {"width": 1280, "height": 720}

    def get_image_resolution(self, image_path):
        """ Retrieves the resolution of an image file. """
        try:
            with Image.open(image_path) as img:
                return {"width": img.width, "height": img.height}
        except Exception as e:
            logging.error(f"Error reading image: {e}")
            return None

    def get_video_metadata(self, file_path):
        """ Extracts video metadata (duration, resolution, fps) using FFmpeg. """
        try:
            probe = ffmpeg.probe(file_path)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

            if not video_stream:
                raise ValueError("No video stream found")

            duration = float(probe['format']['duration'])
            width = int(video_stream['width'])
            height = int(video_stream['height'])
            fps = eval(video_stream['r_frame_rate'])  # Convert "30000/1001" to float

            self.target_resolution["width"] = width
            self.target_resolution["height"] = height

            return {
                "duration": duration,
                "resolution": f"{width}x{height}",
                "fps": round(fps, 2)
            }
        except Exception as e:
            logging.error(f"Error getting video metadata: {e}")
            raise

    def validate_video(self, metadata):
        """ Validates if the video meets the required specifications. """
        if metadata["duration"] > self.max_duration:
            raise ValueError(f"Video duration exceeds {self.max_duration} seconds")

        width, height = map(int, metadata["resolution"].split("x"))
        if width < self.min_resolution["width"] or height < self.min_resolution["height"]:
            raise ValueError(f"Video resolution is below minimum required ({self.min_resolution['width']}x{self.min_resolution['height']})")

        if metadata["fps"] < 24:
            raise ValueError("Video frame rate is too low (minimum 24 fps required)")

        return {"result": True, "message": "Video is valid"}

    def prepare_video(self, file_path):
        """ Compresses and resizes the video using FFmpeg. """
        output_dir = os.path.join(os.getcwd(), "temp_videos")
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, os.path.basename(file_path))

        command = (
            ffmpeg
            .input(file_path)
            .output(output_path, vcodec="libx264", crf=23, preset="medium", acodec="copy")
        )

        try:
            command.run()  # Removed asyncio.to_thread, now runs synchronously
            return output_path
        except Exception as e:
            logging.error(f"Error compressing video: {e}")
            raise

    def process_video(self, file_path):
        """ Handles video processing (metadata extraction, validation, compression). """
        if not file_path:
            raise ValueError("File path is required")

        try:
            metadata = self.get_video_metadata(file_path)  # Now synchronous
            self.validate_video(metadata)  # Now synchronous
            prepared_file = self.prepare_video(file_path)  # Now synchronous
            return prepared_file
        except Exception as e:
            logging.error(f"Error processing video: {e}")
            raise
