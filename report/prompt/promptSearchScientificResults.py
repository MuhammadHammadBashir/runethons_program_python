# def prompt_search_scientific_results(athlete_data, video_analysis, frame_analysis):
#     prompt = f"""
#     You are an advanced research assistant specializing in retrieving and summarizing the latest scientific evidence from peer-reviewed research papers.
    
#     Your task is to identify and analyze the top 5-7 most recent and relevant research papers in the field of video analysis of athletes, particularly focusing on:

#     - Athlete's profile: {athlete_data}
#     - Pose estimation techniques used in video analysis: {video_analysis}
#     - Detailed results of the framework analysis for each video frame: {frame_analysis}

#     ### Expected Output:
#     You **must return** the response in JSON format with the following structure:

#     ```json
#     {{
#       "research_summary": "Summary of findings...",
#       "bibliography": [
#         {{
#           "title": "Paper Title 1",
#           "authors": ["Author 1", "Author 2"],
#           "year": 2024,
#           "source": "Journal Name",
#           "doi": "https://doi.org/xxxx"
#         }},
#         {{
#           "title": "Paper Title 2",
#           "authors": ["Author A", "Author B"],
#           "year": 2023,
#           "source": "Conference Name",
#           "doi": "https://doi.org/yyyy"
#         }}
#       ]
#     }}
#     ```

#     Ensure:
#     - The extracted information is **structured JSON**.
#     - The bibliography section contains valid sources.
#     - If a DOI is unavailable, set `"doi": null`.
#     """
    
#     return prompt




def prompt_search_scientific_results(athlete_data, video_analysis, frame_analysis):
    prompt = f"""
    You are an advanced AI research assistant. Your task is to search for and summarize the latest **high-impact** scientific research in athlete video analysis.

    ## **Instructions:**
    - **Only return valid JSON** (no markdown, no explanations, no extra text).
    - The JSON **must contain exactly two objects**: `"research_summary"` and `"bibliography"`.
    - The `"bibliography"` must be a list of at most **7** research papers.
    - **Only include papers from high-impact journals and top-tier conferences** in biomechanics, sports science, and AI.  
      **(Examples: Nature, Science, IEEE Transactions, Journal of Sports Science, Journal of Biomechanics, CVPR, NeurIPS, ICCV, ICLR)**
    - Each entry in the `"bibliography"` must include:
      - `"title"`: Paper title
      - `"authors"`: List of authors
      - `"year"`: Year of publication
      - `"source"`: Journal or conference name
      - `"doi"`: **MUST be a valid DOI URL** (or `null` if unavailable)

    ## **Required JSON Format:**
    {{
      "research_summary": "Summary of the latest findings from high-impact research...",
      "bibliography": [
        {{
          "title": "Advanced AI Techniques in Athlete Pose Analysis",
          "authors": ["John Doe", "Alice Smith"],
          "year": 2024,
          "source": "IEEE Transactions on Neural Networks",
          "doi": "https://doi.org/10.1109/TNN.2024.1234567"
        }},
        {{
          "title": "Deep Learning for Biomechanical Motion Analysis",
          "authors": ["Jane Doe", "Bob Johnson"],
          "year": 2023,
          "source": "Journal of Biomechanics",
          "doi": "https://doi.org/10.1016/j.jbiomech.2023.001234"
        }}
      ]
    }}

    ## **Context:**
    - **Athlete Profile**: {athlete_data}
    - **Pose Estimation Techniques**: {video_analysis}
    - **Frame-by-Frame Analysis Results**: {frame_analysis}

    **Return only valid JSON.** Do not include any text outside the JSON response.
    """

    return prompt
