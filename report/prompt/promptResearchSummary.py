import json
def prompt_research_summary(ai_result,athleteData,videoAnalysisTemp,descriptionVideoAnalysis):
    return f"""
    I am leading scientific research based on the video analysis of an athlete.I am looking for scientific papers that can support my work.I will provide you with the context and I would like you to summarize the research file, considering in particular:

    1. The athlete's profile
    2. The video analysis made through Pose estimation
    3. The detailed results of the framework analysis for frame

    The goal is to find scientific evidence that can corroborate my video analysis.Could you help me identify the most relevant papers, connecting them to the specific data of the athlete and the results of the video analysis?
            ## Here the athlete's data: 
    {json.dumps(athleteData['athlete'])}

    # Here the evaluation carried out with measurements through pose estimation of the video:
    {json.dumps(videoAnalysisTemp)}

    # Here the results of the Full Video Frame Analysis with more in-depth assessments of the video:
    {descriptionVideoAnalysis}

    # Here is the research paper for which I want you to provide me above analysics. {ai_result}
    """