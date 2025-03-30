import logging
from data_retriever import DataRetriever
from input_manager import InputManager
# from json_formatter import JSONFormatter
# from llm_integrator import LLMIntegrator
from report_generator import ReportGenerator
# from research_module import ResearchModule
from research_module_1 import ResearchModule
from video_analyzer import VideoAnalyzer
from report_generator_crew import ScientificPaperCrew
import json
class PerformanceAnalysisSystem:
    def __init__(self):
        # self.input_manager = InputManager()
        self.data_retriever = DataRetriever()
        self.video_analyzer = None  # Initialized after video processing
        # self.llm_integrator = LLMIntegrator()
        # self.research_module = ResearchModule()
        self.research_module = ResearchModule()
        self.report_generator = None  # Initialized later
        self.json_formatter = None  # Initialized later

    def analyze_performance(self, video_file: str, athlete_email: str = None, report_id: str = None):
        try:
            # Step 1: Video processing
            # video_path = self.input_manager.process_video(video_file)
            # logging.info(f"Video processed. Path: {video_path}")

            # Step 2: Retrieve athlete's data
            athlete_data = self.data_retriever.get_all_data(athlete_email)
            logging.info(f"Athlete data retrieved: {athlete_data}")




            video_path = video_file

            # # Step 3: Video analysis
            # self.video_analyzer = VideoAnalyzer(video_path)
            # video_analysis = self.video_analyzer.analyze()
            # logging.info(f"Video analysis completed: {video_analysis}")

            # Reading temp from the file to speed up the process
            file_path = "video_analysics_report.json"


            with open(file_path, "r", encoding="utf-8") as f:
                video_analysis = json.load(f)

            # # Step 4: Conduct research
            research_results = self.research_module.conduct_research(athlete_data, video_analysis)
            logging.info(f"Research completed: {research_results}")





            # data_to_save = {
            #     "athlete_data": athlete_data,
            #     "video_analysis": video_analysis,
            #     "research_results": research_results
            # }

            # # # Save to a JSON file
            # file_path = "saved_final_temp_analysis.json"
            # with open(file_path, "w") as f:
            #     json.dump(data_to_save, f, indent=4)

            # print(f"Data successfully saved to {file_path}")

            # with open("saved_final_temp_analysis.json", "r") as f:
            #     loaded_data = json.load(f)

            # athlete_data = loaded_data["athlete_data"]
            # video_analysis = loaded_data["video_analysis"]
            # research_results = loaded_data["research_results"]


            # self.report_generator = ReportGenerator(athlete_data, video_analysis, research_results)
            # final_report = self.report_generator.generate_report(report_id)
            # logging.info(f"Report generated: {final_report}")
            # # crew_system = ScientificPaperCrew(athlete_data, video_analysis, research_results)
            # # final_report = crew_system.generate_paper()

            # # return report
            # with open("final_report.html", "w", encoding="utf-8") as file:
            #     file.write(final_report)

            # return final_report

            return "yes"
        
        
        except Exception as e:
            logging.error(f"Error in performance analysis: {str(e)}", exc_info=True)
            raise

