import json
def prompt_benchmark_results(athlete, video_analysis, frame_analysis,scientific_paper_json):
    prompt = f"""
    I am leading scientific research based on the video analysis of an athlete. I am looking for pertinent benchmarks to support my work. I will provide you with the necessary context, and I would like you to analyze and summarize the content of these videos, relating it to:

    1. The athlete's profile
    2. The video analysis made through Pose Estimation
    3. The detailed results of the framework analysis for each frame
    4. The scientific papers to support the analysis

    The goal is to find scientific evidence that can corroborate my video analysis. Could you help me identify the benchmarks of these scientific papers that I will provide, connecting them to the specific data of the athlete and the results of the video analysis?

    To facilitate this process, I will provide you with the following information:

    - Athlete data: {json.dumps(athlete, indent=2)}
    - Evaluation carried out with measurements through Pose Estimation of the video: {json.dumps(video_analysis, indent=2)}
    - Results of the Full Video Frame analysis with more in-depth assessments: {json.dumps(frame_analysis, indent=2)}
    - Scientific paper connected to my research from which to try to pick up benchmarks: {scientific_paper_json}

    Using this information, could you analyze the relevant files and provide a complete analysis that integrates all these elements, obtaining concrete and measurable data to be compared between the results of the paper and the video analysis?
        """
    return prompt