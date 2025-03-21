def prompt_search_scientific_results(athlete_data, video_analysis, frame_analysis):
    prompt = f'''
    You are an advanced research assistant specializing in retrieving and summarizing the latest scientific evidence from peer-reviewed research papers.
    Your task is to identify and analyze the top 5-7 most recent and relevant research papers in the field of video analysis of athletes, particularly focusing on:
    
    1. Athlete's profile: {athlete_data}
    2. Pose estimation techniques used in video analysis: {video_analysis}
    3. Detailed results of the framework analysis for each video frame: {frame_analysis}

    Research report will be in summarized report of all paper you found.  At last provide the bibliography as usually present in the research papers.
    

    
    Ensure the extracted information is concise, factual, and supported by proper citations. Provide a structured bibliography in JSON format, including:
    - Title
    - Authors
    - Year
    - Source
    - DOI/URL
    
    Return the response in a structured format for easy analysis.
    '''
    
    return prompt