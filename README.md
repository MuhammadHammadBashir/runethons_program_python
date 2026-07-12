RunTheOns – AI-Powered Virtual Sports Health Coach & Biomechanics Analysis

🌐 Website: https://www.runtheons.com/

Overview

RunTheOns is an AI-powered virtual sports coach designed to analyze athlete movements from smartphone videos and provide personalized biomechanics, health, and performance feedback. The platform combines computer vision, biomechanics, sports science, and large language models to transform short gameplay or training videos into comprehensive coaching reports.

Instead of simply tracking body joints, the system evaluates movement quality, identifies biomechanical inefficiencies, estimates injury risk, and delivers evidence-based recommendations generated from scientific literature.

Key Features
AI-Based Biomechanics Analysis
Automatic pose estimation
Joint angle calculation
Motion tracking
Velocity and acceleration estimation
Movement symmetry analysis
Injury risk assessment
Performance evaluation
Pose Estimation

The system extracts athlete landmarks using modern pose estimation models, including:

MediaPipe Pose
Ultralytics Pose
Vision-Language Models for posture understanding

Body landmarks are used to calculate:

Knee angles
Hip angles
Elbow angles
Shoulder rotation
Ankle movement
Spine alignment
Head posture
Movement Analysis

The platform measures:

Jump height
Contact time
Flight time
Reactive Strength Index (RSI)
Landing mechanics
Sprint phases
Acceleration
Deceleration
Balance
Stability
Movement symmetry

These metrics are compared against sports science references to identify areas for improvement.

AI Coaching Reports

One of the main goals of RunTheOns is to provide athletes with personalized coaching instead of raw measurements.

The system compares:

Actual athlete movement
Ideal movement patterns
Published biomechanics research

It then generates detailed coaching reports explaining:

What the athlete performed correctly
Technical mistakes
Injury risks
Performance limitations
Recommended improvements
Vision AI Pipeline

The platform combines multiple Vision AI models to improve analysis accuracy.

Claude Sonnet 3.7

Used for block-based image understanding and posture evaluation.

GPT-4o Vision

Processes frame-by-frame athlete movements for detailed motion analysis.

Gemini 2.5

Combines outputs from different vision models using its large context window to generate consistent and accurate biomechanics reports.

The system samples videos at approximately 6 FPS, allowing efficient processing while preserving sufficient temporal information for movement analysis.

Multi-Agent AI System

RunTheOns uses multiple AI agents that collaborate to generate personalized recommendations.

Fitness Coach

Analyzes movement quality and creates individualized training plans.

Nutrition Advisor

Generates nutrition recommendations based on athlete goals and performance.

Game Coach

Provides sport-specific technical feedback and tactical suggestions.

Each agent contributes to the final report using structured prompt engineering workflows.

RAG-Based Knowledge System

To ensure recommendations are grounded in scientific evidence, the platform integrates Retrieval-Augmented Generation (RAG).

The system retrieves relevant information from:

arXiv
Semantic Scholar
YouTube educational content
Research publications
Sports science literature

Rather than relying solely on LLM knowledge, recommendations are supported by external evidence and citations.

Athlete Reports

Each analysis generates a detailed report containing:

Biomechanics assessment
Performance summary
Joint angle visualizations
Movement quality evaluation
Injury risk analysis
Personalized training recommendations
Nutrition guidance
Recovery suggestions
Scientific references
Progress tracking

Reports are designed for athletes, coaches, and sports professionals.

Computer Vision Components
Pose estimation
Human keypoint detection
Joint tracking
Motion analysis
Frame extraction
Video preprocessing
Athlete segmentation
Landmark smoothing
Threshold-based event detection
Temporal movement analysis
AI Components
Vision-Language Models
Prompt Engineering
Multi-Agent Systems
Retrieval-Augmented Generation (RAG)
Embedding Search
Semantic Retrieval
Scientific Literature Analysis
Personalized Recommendation Generation
Backend Architecture

The platform exposes REST APIs through FastAPI for:

Video upload
Video processing
Pose extraction
AI report generation
Research retrieval
Athlete profile management
Technologies Used
Computer Vision
OpenCV
MediaPipe
Ultralytics YOLO
FFmpeg
Pillow (PIL)
Large Language Models
Gemini 2.5
Claude Sonnet
GPT-4o
LLaVA
AI Frameworks
LangChain
CrewAI
Hugging Face Transformers
Retrieval & Knowledge
Pinecone
Embedding Models
Semantic Scholar
arXiv
Perplexity API
YouTube Knowledge Retrieval
Backend
Python
FastAPI
Applications
Sports biomechanics
Athlete performance analysis
Virtual coaching
Injury prevention
Sports science research
Fitness assessment
Personalized training
AI-powered health coaching
Future Enhancements
Real-time live coaching during training
Mobile application support
Multi-camera biomechanical analysis
Wearable sensor integration
Team performance dashboards
Coach collaboration portal
Longitudinal athlete progress tracking
AI-powered rehabilitation programs
