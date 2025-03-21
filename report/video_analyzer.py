import os
from pathlib import Path
import cv2
import mediapipe as mp
import numpy as np
import math
import shutil

from ultralytics import YOLO
import base64
import os
import json
import threading
import concurrent.futures
from prompt.promptExtractAndDescriptFrames import prompt_extract_and_describe_frames
from llm_calls.analyze_photo import analyze_photo
from llm_calls.analyze_video import analyze_video
class VideoAnalyzer:
    def __init__(self, video_path, athlete_data=None):
        self.video_path = video_path
        self.athlete_data = athlete_data

        # Get video name without extension
        video_name = os.path.splitext(os.path.basename(video_path))[0]

        # Define frames directory path
        self.frames_dir = os.path.join(os.getcwd(), f"asset/video-frames/{video_name}/")
        self.filter_frames_dir = os.path.join(os.getcwd(), f"asset/filtered-video-frames/{video_name}/")
        
        # Initialize attributes
        self.keypoints = []
        self.angles = []
        self.velocities = []
        self.video_frames = []
        self.video_analysis = ''

        self.yolo_model = YOLO("yolov8s.pt")
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=True, model_complexity=2)

    def analyze(self):
        """Runs the full video analysis process sequentially."""
        self.extract_frames(self.video_path, 30)
        self.intelligent_filter_frames()

        self.detect_keypoints()
        angles = self.calculate_angles()
        
        # print("athleteData:", self.athlete_data)
        # print("angles:", angles)

        # Get athlete height in meters (default to 1.7m if not provided)
        person_height_in_meters = int(self.athlete_data.get("height", 170)) / 100 if self.athlete_data else 1.7

        self.calculate_velocities(30, person_height_in_meters)

        self.descript_frames()
        self.generate_video_analysis()
        
        return self.generate_analysis_report()
    def extract_frames(self,video_path, fps=None):
        # Create output directory
        print(f'extractFrames > frames_dir: {self.frames_dir}')
        os.makedirs(self.frames_dir, exist_ok=True)
        

        
        # Check if directory was created
        if not os.path.exists(self.frames_dir):
            print('extractFrames > directory was not created')
            return []
        
        # Get video file name without extension
        base_name = Path(video_path).stem
        
        # Open the video
        video = cv2.VideoCapture(video_path)
        if not video.isOpened():
            print(f"Could not open video: {video_path}")
            return []
        
        # Get video properties
        video_fps = video.get(cv2.CAP_PROP_FPS)
        frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Calculate frame interval based on desired fps
        if fps is not None:
            frame_interval = int(video_fps / fps)
            if frame_interval < 1:
                frame_interval = 1
        else:
            frame_interval = 1  # Extract every frame
        
        frame_number = 0
        count = 1
        extracted_frames = []
        
        while True:
            success, frame = video.read()
            if not success:
                break
                
            if frame_number % frame_interval == 0:
                output_path = f"{self.frames_dir}/{base_name}_frame{count}.jpg"
                cv2.imwrite(output_path, frame)
                extracted_frames.append(output_path)
                count += 1
                
            frame_number += 1
        
        video.release()
    def intelligent_filter_frames(self):
        """Filters frames that contain a person and saves them in a separate folder."""
        
        os.makedirs(self.filter_frames_dir, exist_ok=True)
        
        # Check if directory was created
        if not os.path.exists(self.filter_frames_dir):
            print('extractFrames > directory was not created')
            return []
        for filename in os.listdir(self.frames_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):  # Process only images
                image_path = os.path.join(self.frames_dir, filename)
                image = cv2.imread(image_path)

                # Run YOLO inference without unnecessary logs
                results = self.yolo_model(image, verbose=False)

                # Track highest confidence for each class
                class_confidences = {}

                # Check if a person (class ID 0) is detected
                person_detected = False

                for result in results:
                    for box in result.boxes:
                        class_id = int(box.cls[0])  # Class ID
                        confidence = float(box.conf[0])  # Confidence score

                        # Store the highest confidence for each detected class
                        if class_id not in class_confidences or confidence > class_confidences[class_id]:
                            class_confidences[class_id] = confidence

                        # Check if the detected class is "person" (Class ID 0)
                        if class_id == 0 and confidence > 0.8:  # Confidence threshold (adjustable)
                            person_detected = True

                # Print confidence scores
                # print(f"📌 {filename}:")
                # for class_id, confidence in class_confidences.items():
                #     print(f"   - Class {class_id}: {confidence:.2f}")

                # If a person is detected, copy the image to the filtered frames directory
                if person_detected:
                    shutil.copy(image_path, os.path.join(self.filter_frames_dir, filename))
                    print(f"✅ Copied: {filename}")

        print(f"🎯 Filtering complete! All images with persons are saved in: {self.filter_frames_dir}")
    def descript_frames(self):
        if not os.path.exists(self.filter_frames_dir):
            raise FileNotFoundError(f"Frame directory {self.filter_frames_dir} not found.")

        frame_files = sorted(
            [f for f in os.listdir(self.filter_frames_dir) if f.endswith(".jpg")],
            key=lambda x: int(x.split("frame")[1].split(".jpg")[0])
        )
        results = []
        # Using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_frame = {}

            frame_number = 1  # Initialize frame number
            for file in frame_files:
                frame_path = os.path.join(self.frames_dir, file)

                # Load image as Base64
                with open(frame_path, "rb") as image_file:
                    base64_image = base64.b64encode(image_file.read()).decode("utf-8")

                prompt = prompt_extract_and_describe_frames(frame_number)

                # Submit task to thread pool
                future = executor.submit(analyze_photo, base64_image, frame_number, prompt)
                future_to_frame[future] = frame_number

                frame_number += 1  # Increment frame number

            # Retrieve results
            for future in concurrent.futures.as_completed(future_to_frame):
                frame_number, description = future.result()
                self.video_frames.append({"frameNumber": frame_number, "description": description})
    def detect_keypoints(self):
        """ Detects keypoints from extracted frames using MediaPipe Pose. """
        if not os.path.exists(self.frames_dir):
            raise FileNotFoundError(f"Frame directory {self.frames_dir} not found.")

        frame_files = sorted(
            [f for f in os.listdir(self.frames_dir) if f.endswith(".jpg")],
            key=lambda x: int(x.split("frame")[1].split(".jpg")[0])
        )

        frame_number = 1
        for file in frame_files:
            frame_path = os.path.join(self.frames_dir, file)


            # Load image
            image = cv2.imread(frame_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Run pose detection
            results = self.pose.process(image_rgb)

            if results.pose_landmarks:
                keypoints = [
                    {
                        "frameNumber": frame_number,
                        "x": lm.x * image.shape[1],  # Convert normalized to pixels
                        "y": lm.y * image.shape[0],
                        "part": self.mp_pose.PoseLandmark(i).name,
                        "confidence": lm.visibility
                    }
                    for i, lm in enumerate(results.pose_landmarks.landmark)
                ]
                self.keypoints.append(keypoints)

            print(f"Processed {file}")
            frame_number += 1

        print("Detected keypoints:", self.keypoints)

    def calculate_angles(self):
        """ Calculate joint angles based on detected keypoints. """
        self.angles = []
        for points in self.keypoints:
            # Convert keypoints list into a dictionary for easy access
            body_points = {point["part"]: point for point in points}

            self.angles.append({
                "rightElbow": self.calculate_angle(
                    body_points.get("RIGHT_SHOULDER"),
                    body_points.get("RIGHT_ELBOW"),
                    body_points.get("RIGHT_WRIST")
                ),
                "leftElbow": self.calculate_angle(
                    body_points.get("LEFT_SHOULDER"),
                    body_points.get("LEFT_ELBOW"),
                    body_points.get("LEFT_WRIST")
                ),
                "rightKnee": self.calculate_angle(
                    body_points.get("RIGHT_HIP"),
                    body_points.get("RIGHT_KNEE"),
                    body_points.get("RIGHT_ANKLE")
                ),
                "leftKnee": self.calculate_angle(
                    body_points.get("LEFT_HIP"),
                    body_points.get("LEFT_KNEE"),
                    body_points.get("LEFT_ANKLE")
                ),
                "rightHip": self.calculate_angle(
                    body_points.get("RIGHT_SHOULDER"),
                    body_points.get("RIGHT_HIP"),
                    body_points.get("RIGHT_KNEE")
                ),
                "leftHip": self.calculate_angle(
                    body_points.get("LEFT_SHOULDER"),
                    body_points.get("LEFT_HIP"),
                    body_points.get("LEFT_KNEE")
                )
            })
        print("Calculated Angles:", self.angles)
        return self.angles
        
    def calculate_angle(self, pointA, pointB, pointC):
        """ Calculate the angle at pointB formed by (pointA - pointB - pointC). """
        if not pointA or not pointB or not pointC:
            return None  # Return None if any keypoint is missing

        # Vector BA
        vectorBA_x = pointA["x"] - pointB["x"]
        vectorBA_y = pointA["y"] - pointB["y"]

        # Vector BC
        vectorBC_x = pointC["x"] - pointB["x"]
        vectorBC_y = pointC["y"] - pointB["y"]

        # Dot product
        dot_product = vectorBA_x * vectorBC_x + vectorBA_y * vectorBC_y

        # Magnitudes
        magnitudeBA = math.sqrt(vectorBA_x**2 + vectorBA_y**2)
        magnitudeBC = math.sqrt(vectorBC_x**2 + vectorBC_y**2)

        if magnitudeBA == 0 or magnitudeBC == 0:
            return None  # Prevent division by zero

        # Compute angle in radians and convert to degrees
        angle_rad = math.acos(dot_product / (magnitudeBA * magnitudeBC))
        angle_deg = math.degrees(angle_rad)

        return angle_deg
    def calculate_velocities(self, fps=30, person_height_in_meters=1.7):
        """Calculate the velocity of key body points in km/h based on keypoints from frames."""
        time_interval = 1 / fps  # Time interval between frames
        self.velocities = []

        for i in range(1, len(self.keypoints)):
            prev_points = self.keypoints[i - 1]
            current_points = self.keypoints[i]

            # Estimate pixels per meter using a reference height
            pixels_per_meter = self.estimate_pixels_per_meter(prev_points, person_height_in_meters)

            frame_velocities = {
                "rightWrist": self.calculate_point_velocity_kmh(self.get_point(prev_points, "right_wrist"),
                                                                self.get_point(current_points, "right_wrist"),
                                                                time_interval, pixels_per_meter),
                "leftWrist": self.calculate_point_velocity_kmh(self.get_point(prev_points, "left_wrist"),
                                                               self.get_point(current_points, "left_wrist"),
                                                               time_interval, pixels_per_meter),
                "rightElbow": self.calculate_point_velocity_kmh(self.get_point(prev_points, "right_elbow"),
                                                                self.get_point(current_points, "right_elbow"),
                                                                time_interval, pixels_per_meter),
                "leftElbow": self.calculate_point_velocity_kmh(self.get_point(prev_points, "left_elbow"),
                                                               self.get_point(current_points, "left_elbow"),
                                                               time_interval, pixels_per_meter),
                "rightShoulder": self.calculate_point_velocity_kmh(self.get_point(prev_points, "right_shoulder"),
                                                                   self.get_point(current_points, "right_shoulder"),
                                                                   time_interval, pixels_per_meter),
                "leftShoulder": self.calculate_point_velocity_kmh(self.get_point(prev_points, "left_shoulder"),
                                                                  self.get_point(current_points, "left_shoulder"),
                                                                  time_interval, pixels_per_meter),
                "rightHip": self.calculate_point_velocity_kmh(self.get_point(prev_points, "right_hip"),
                                                              self.get_point(current_points, "right_hip"),
                                                              time_interval, pixels_per_meter),
                "leftHip": self.calculate_point_velocity_kmh(self.get_point(prev_points, "left_hip"),
                                                             self.get_point(current_points, "left_hip"),
                                                             time_interval, pixels_per_meter),
                "rightKnee": self.calculate_point_velocity_kmh(self.get_point(prev_points, "right_knee"),
                                                               self.get_point(current_points, "right_knee"),
                                                               time_interval, pixels_per_meter),
                "leftKnee": self.calculate_point_velocity_kmh(self.get_point(prev_points, "left_knee"),
                                                              self.get_point(current_points, "left_knee"),
                                                              time_interval, pixels_per_meter),
                "rightAnkle": self.calculate_point_velocity_kmh(self.get_point(prev_points, "right_ankle"),
                                                                self.get_point(current_points, "right_ankle"),
                                                                time_interval, pixels_per_meter),
                "leftAnkle": self.calculate_point_velocity_kmh(self.get_point(prev_points, "left_ankle"),
                                                               self.get_point(current_points, "left_ankle"),
                                                               time_interval, pixels_per_meter),
                "nose": self.calculate_point_velocity_kmh(self.get_point(prev_points, "nose"),
                                                          self.get_point(current_points, "nose"),
                                                          time_interval, pixels_per_meter)
            }

            self.velocities.append(frame_velocities)

        print("Calculated Velocities:", self.velocities)
        print("velocities_printed_above")

    def estimate_pixels_per_meter(self, points, person_height_in_meters):
        """Estimate the scale of the image in pixels per meter based on the athlete's height."""
        nose = self.get_point(points, "nose")
        left_ankle = self.get_point(points, "left_ankle")
        right_ankle = self.get_point(points, "right_ankle")

        if not nose or not left_ankle or not right_ankle:
            return 100  # Default value if estimation is not possible

        # Average the Y-coordinates of both ankles
        ankle_y = (left_ankle["y"] + right_ankle["y"]) / 2
        pixel_height = ankle_y - nose["y"]

        return pixel_height / person_height_in_meters

    def calculate_point_velocity_kmh(self, prev_point, current_point, time_interval, pixels_per_meter):
        """Calculate the velocity of a single keypoint in km/h."""
        if not prev_point or not current_point:
            return None

        # Calculate Euclidean distance in pixels
        distance_pixels = math.sqrt((current_point["x"] - prev_point["x"]) ** 2 +
                                    (current_point["y"] - prev_point["y"]) ** 2)

        # Convert distance from pixels to meters
        distance_meters = distance_pixels / pixels_per_meter

        # Compute velocity in m/s and convert to km/h
        velocity_mps = distance_meters / time_interval
        velocity_kmh = velocity_mps * 3.6  # Convert m/s to km/h

        return round(velocity_kmh, 2)  # Round to two decimal places

    def get_point(self, points, part):
        """Helper function to retrieve a specific keypoint."""
        return next((p for p in points if p["part"] == part), None)
    
    def identify_potential_issues(self):
        """
        Identify potential movement issues based on angles and velocities.
        """
        issues = []

        for frame_index, frame_angles in enumerate(self.angles):
            frame_velocities = self.velocities[frame_index] if frame_index < len(self.velocities) else None

            # Knee issues
            if frame_angles["leftKnee"] < 45 or frame_angles["leftKnee"] > 135:
                issues.append(f"Frame {frame_index}: Potential left knee issue. Angle: {frame_angles['leftKnee']:.2f}°")
            if frame_angles["rightKnee"] < 45 or frame_angles["rightKnee"] > 135:
                issues.append(f"Frame {frame_index}: Potential right knee issue. Angle: {frame_angles['rightKnee']:.2f}°")

            # Elbow hyperextension issues
            if frame_angles["leftElbow"] < 15 or frame_angles["leftElbow"] > 165:
                issues.append(f"Frame {frame_index}: Potential left elbow hyperextension. Angle: {frame_angles['leftElbow']:.2f}°")
            if frame_angles["rightElbow"] < 15 or frame_angles["rightElbow"] > 165:
                issues.append(f"Frame {frame_index}: Potential right elbow hyperextension. Angle: {frame_angles['rightElbow']:.2f}°")

            # Hip asymmetry
            hip_asymmetry = abs(frame_angles["leftHip"] - frame_angles["rightHip"])
            if hip_asymmetry > 20:
                issues.append(f"Frame {frame_index}: Significant hip asymmetry detected. Difference: {hip_asymmetry:.2f}°")

            # High velocity detection
            velocity_threshold = 50  # km/h
            if frame_velocities:
                for part, velocity in frame_velocities.items():
                    if velocity > velocity_threshold:
                        issues.append(f"Frame {frame_index}: High velocity detected in {part}. Speed: {velocity:.2f} km/h")

        return issues

    def assess_injury_risk(self):
        """
        Assess injury risk based on movement patterns over time.
        """
        risk_factors = {
            "suddenChangeKnee": 0,
            "suddenChangeElbow": 0,
            "sustainedBadPosture": 0,
            "repetitiveHighVelocity": 0,
            "oscillatingAsymmetry": 0
        }

        sequence_length = 10  # Analyze sequences of 10 frames
        frame_counts = len(self.angles)

        for i in range(sequence_length, frame_counts):
            sequence_angles = self.angles[i - sequence_length:i]
            sequence_velocities = self.velocities[i - sequence_length:i]

            # Sudden knee angle change
            knee_angle_change = abs(sequence_angles[-1]["leftKnee"] - sequence_angles[0]["leftKnee"])
            if knee_angle_change > 45:
                risk_factors["suddenChangeKnee"] += 1

            # Sudden elbow angle change
            elbow_angle_change = abs(sequence_angles[-1]["leftElbow"] - sequence_angles[0]["leftElbow"])
            if elbow_angle_change > 45:
                risk_factors["suddenChangeElbow"] += 1

            # Repetitive high velocity movements
            high_velocity_count = sum(
                1 for frame in sequence_velocities if any(velocity > 50 for velocity in frame.values())
            )
            if high_velocity_count > sequence_length * 0.5:
                risk_factors["repetitiveHighVelocity"] += 1

            # Oscillating hip asymmetry
            hip_asymmetry_sequence = [abs(frame["leftHip"] - frame["rightHip"]) for frame in sequence_angles]
            asymmetry_oscillation = max(hip_asymmetry_sequence) - min(hip_asymmetry_sequence)
            if asymmetry_oscillation > 30:
                risk_factors["oscillatingAsymmetry"] += 1

        # Normalize risk factors
        sequence_counts = frame_counts - sequence_length + 1
        for factor in risk_factors:
            risk_factors[factor] = (risk_factors[factor] / sequence_counts) * 100 if sequence_counts > 0 else 0

        # Compute final risk score
        risk_score = sum(risk_factors.values()) / len(risk_factors)

        # Determine risk level
        if risk_score > 50:
            risk_level = "High"
        elif risk_score > 15:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return {
            "score": round(risk_score, 2),
            "level": risk_level,
            "factors": risk_factors
        }
    def generate_video_analysis(self):
        video_analysis_report = {
            "keypoints": self.keypoints,
            "angles": self.angles,
            "velocities": self.velocities,
            # "potentialIssues": self.identify_potential_issues(),
            # "injuryRiskAssessment": self.assess_injury_risk(),
        }

        prompt = f"""
        Analyzes this video in detail and produce an in-depth scientific paper, focusing on the following aspects:

        1. Biomechanics
        2. Benchmark with precise data
        3. Detailed assessment of the risks of accident

        Include a frame-by-frame analysis, specifying the number of each examined frame. For each frame, evaluate:

        1. The technique used
        2. The potential risk of accident
        3. The possible areas of improvement

        The target audience of this paper will be made up of experts who will have to make decisions and understand how to improve the highlighted aspects. Be exhaustive in your analysis.

        In your evaluation, also consider the following results obtained by a measurement made through Pose estimation on the video in question:
        {json.dumps(video_analysis_report, indent=4)}

        Use these data to enrich and support your overall analysis.
        """
        analysis = analyze_video(self.frames_dir, prompt)
        # print("generate_video_analysis > prompt:", prompt)
        self.video_analysis = analysis
        return analysis
    def generate_analysis_report(self):
        """Generate a dictionary containing the full analysis report."""
        return {
            "keypoints": self.keypoints,
            "angles": self.angles,
            "velocities": self.velocities,
            # "potentialIssues": self.identify_potential_issues(),
            # "injuryRiskAssessment": self.assess_injury_risk(),
            "videoAnalysis": self.video_analysis,
            "videoFrames": self.video_frames
        }       

        
        