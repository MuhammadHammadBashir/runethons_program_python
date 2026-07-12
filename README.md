# 🏃 RunTheOns – AI-Powered Virtual Sports Health Coach & Biomechanics Analysis

**Website:** https://www.runtheons.com/

---

# Overview

RunTheOns is an AI-powered virtual sports coaching platform that combines **computer vision, biomechanics, sports science, and generative AI** to analyze athlete performance from smartphone videos.

The platform processes short training or gameplay videos, extracts biomechanical measurements, evaluates movement quality, estimates injury risk, and generates personalized coaching reports supported by scientific literature.

Rather than simply tracking body landmarks, the system compares an athlete's movement against ideal biomechanical patterns from sports science research and provides actionable recommendations for improving performance.

---

# Features

- AI-powered biomechanics analysis
- Automatic pose estimation
- Joint angle calculation
- Velocity and acceleration estimation
- Injury risk assessment
- Movement quality evaluation
- Personalized coaching reports
- Nutrition recommendations
- Multi-agent AI coaching
- Research-backed recommendations using RAG
- Video understanding with multimodal LLMs

---

# System Architecture

```
Video Upload
      │
      ▼
Video Processing
(OpenCV + FFmpeg)
      │
      ▼
Frame Extraction (6 FPS)
      │
      ▼
Pose Detection
(MediaPipe / Ultralytics)
      │
      ▼
Biomechanics Engine
│
├── Joint Angles
├── Velocity
├── Acceleration
├── Symmetry
├── Contact Time
├── Flight Time
└── Risk Assessment
      │
      ▼
Vision LLM Analysis
│
├── Claude Vision
├── GPT-4o Vision
└── Gemini 2.5
      │
      ▼
Multi-Agent AI System
│
├── Fitness Coach
├── Nutrition Coach
└── Game Coach
      │
      ▼
RAG Knowledge Engine
│
├── arXiv
├── Semantic Scholar
├── YouTube
└── Sports Science Papers
      │
      ▼
Final Athlete Report
```

---

# Computer Vision Pipeline

## Video Processing

- Video preprocessing using FFmpeg
- Frame extraction
- Image normalization
- Frame synchronization
- Motion segmentation

---

## Pose Estimation

The system extracts body landmarks using:

- MediaPipe Pose
- Ultralytics Pose Models

Keypoints are tracked across frames to analyze athlete movement with high temporal consistency.

---

## Biomechanical Analysis

The platform computes:

- Joint angles
- Angular velocity
- Limb symmetry
- Landing mechanics
- Jump height
- Contact time
- Flight time
- Reactive Strength Index (RSI)
- Sprint acceleration
- Deceleration
- Body alignment
- Balance and stability

---

# Vision AI Pipeline

To improve reliability, multiple Vision-Language Models are combined.

### Claude Sonnet 3.7

Used for block-based understanding of athlete posture and overall movement.

---

### GPT-4o Vision

Processes videos frame-by-frame to extract detailed movement information.

---

### Gemini 2.5

Gemini combines outputs from all vision models using its large context window to generate a unified biomechanics analysis.

This multi-model approach produces significantly more stable and accurate reports than relying on a single model.

---

# AI Coaching System

Instead of generating simple metrics, the platform simulates multiple expert coaches.

## Fitness Coach

Provides:

- Exercise recommendations
- Technique improvements
- Performance optimization

---

## Nutrition Advisor

Generates:

- Nutrition plans
- Recovery guidance
- Hydration recommendations

---

## Game Coach

Provides:

- Tactical suggestions
- Sport-specific coaching
- Technical corrections

---

# Retrieval-Augmented Generation (RAG)

Recommendations are backed by scientific literature instead of relying only on LLM knowledge.

The RAG system retrieves information from:

- arXiv
- Semantic Scholar
- YouTube educational content
- Sports science publications
- Perplexity Search

This allows every recommendation to include evidence-based explanations and citations.

---

# Athlete Report

The final report contains:

- Performance summary
- Biomechanics analysis
- Joint angle visualization
- Injury risk assessment
- Technique comparison
- Personalized training plan
- Nutrition recommendations
- Recovery guidance
- Scientific references

---

# Technologies Used

## Computer Vision

- OpenCV
- MediaPipe
- Ultralytics YOLO
- FFmpeg
- Pillow (PIL)

## Large Language Models

- Gemini 2.5
- Claude Sonnet
- GPT-4o
- LLaVA

## AI Frameworks

- LangChain
- CrewAI
- Hugging Face Transformers

## Retrieval & Knowledge

- Pinecone
- Embedding Models
- Semantic Scholar
- arXiv
- Perplexity API

## Backend

- Python
- FastAPI

---

# Applications

- Sports performance analysis
- Athlete biomechanics
- Injury prevention
- Virtual coaching
- Personalized fitness
- Sports science research
- Rehabilitation monitoring

---

# Future Roadmap

- Real-time live coaching
- Mobile application
- Multi-camera biomechanics
- Wearable sensor integration
- Team dashboards
- Long-term athlete progress tracking
- AI rehabilitation assistant

---

# Project Highlights

- AI-powered virtual sports coach
- Multi-modal computer vision pipeline
- Vision-Language Model integration
- Multi-agent coaching architecture
- Research-backed recommendations using RAG
- Personalized athlete reports
- Production-ready FastAPI backend
- End-to-end video understanding pipeline
