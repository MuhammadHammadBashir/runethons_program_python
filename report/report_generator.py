from prompt.promptPaperGenerator import prompt_paper_generator
import json
import utils.get_alfred_ai_response import  get_alfred_ai_response
class ReportGenerator:
    def __init__(self, athleteData, videoAnalysis, researchResults):
        self.athleteData = athleteData
        self.videoAnalysis = videoAnalysis
        self.researchResults = researchResults

    def generate_prompt_paper(self):
        prompt_paper = prompt_paper_generator()  # Assuming this function returns the template string

        # Replacing placeholders with JSON data
        prompt_paper = prompt_paper.replace("[ATHLETE_DATA]", json.dumps(self.athleteData))
        # prompt_paper = prompt_paper.replace("[ATHLETE_CONVERSATIONS]", json.dumps(self.athleteData.get("athleteConversations", {})))
        # prompt_paper = prompt_paper.replace("[EXPERT_CONVERSATIONS]", json.dumps(self.athleteData.get("expertConversations", {})))

        # Structuring the video analysis data
        video_analysis_data = {
            "keypoints": self.videoAnalysis.get("keypoints"),
            "angles": self.videoAnalysis.get("angles"),
            "velocities": self.videoAnalysis.get("velocities"),
            "videoAnalysis": self.videoAnalysis.get("videoAnalysis", ""),
            "videoFrames": self.videoAnalysis.get("videoFrames", {})
        }
        prompt_paper = prompt_paper.replace("[VIDEO_ANALYSIS]", json.dumps(video_analysis_data))

        print("Final prompt searches:", self.researchResults)

        prompt_paper = prompt_paper.replace("[DESCRIPTION_VIDEO_ANALYSIS]", self.videoAnalysis.get("videoAnalysis", ""))
        prompt_paper = prompt_paper.replace("[VIDEO_FRAMES]", json.dumps(self.videoAnalysis.get("videoFrames", {})))

        # Handling research results properly
        research_results_data = {
            "papers_summary": self.researchResults.get("papers_summary", ""),
            "benchmark_results": self.researchResults.get("benchmark_results", [])
        }
        prompt_paper = prompt_paper.replace("[SCIENTIFIC_PAPERS]", json.dumps(research_results_data["papers_summary"]))
        prompt_paper = prompt_paper.replace("[BENCHMARKS]", json.dumps(research_results_data["benchmark_results"]))

        return prompt_paper
    
    def generateReport(self,reportId):
        report_prompt  =  self.generate_prompt_paper()

        final_response = get_alfred_ai_response(report_prompt, 'gemini')

        print(final_response)

