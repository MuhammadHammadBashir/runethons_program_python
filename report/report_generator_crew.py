import json
from crewai import Agent, Task, Crew
# from langchain_google_genai import ChatGoogleGenerativeAI
from prompt.promptPaperGenerator import prompt_paper_generator
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, LLM
import os
from dotenv import load_dotenv
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
class ScientificPaperCrew:
    def __init__(self, athleteData, videoAnalysis, researchResults):
        self.athleteData = athleteData
        self.videoAnalysis = videoAnalysis
        self.researchResults = researchResults
        self.llm = LLM(api_key=os.getenv('GEMINI_API_KEY'),
                       model='gemini/gemini-1.5-pro-002'
                       )
        
    def generate_paper(self):
        # ✅ Dynamically Construct the Prompt
        prompt_paper = self._generate_prompt()

        # ✅ Define CrewAI Agents with Task-Specific Context
        coach_agent = Agent(
            name="Coach Agent",
            role="Sports Biomechanics Analyst",
            goal="Analyze joint angles, movement efficiency, and performance benchmarks.",
            backstory="A professional sports coach specializing in biomechanics. You evaluate an athlete’s movement efficiency.",
            llm=self.llm
        )

        physiologist_agent = Agent(
            name="Physiologist Agent",
            role="Endurance & Metabolic Expert",
            goal="Assess physiological performance, including oxygen efficiency, energy use, and fatigue metrics.",
            backstory="You are a physiologist specializing in metabolic and endurance assessments.",
            llm=self.llm
        )

        researcher_agent = Agent(
            name="Researcher Agent",
            role="Scientific Literature Analyst",
            goal="Compare findings with recent scientific literature and provide evidence-based insights.",
            backstory="A researcher with expertise in biomechanics and sports science, summarizing relevant studies.",
            llm=self.llm
        )

        report_compiler = Agent(
            name="Report Compiler",
            role="Scientific Paper Writer",
            goal="Integrate all findings into a structured, formatted scientific paper in Italian.",
            backstory="An expert in academic writing, structuring the final research paper with proper citations.",
            llm=self.llm
        )

       
        biomechanical_analysis = Task(
            description=f"Analyze the athlete’s video performance based on keypoints, angles, and velocities.\n\n**Video Analysis:** {json.dumps(self.videoAnalysis)}",
            agent=coach_agent,
            expected_output="A detailed biomechanical analysis report describing the efficiency, balance, and potential improvements in the athlete's movements."
        )

        physiological_evaluation = Task(
            description=f"Assess the athlete’s physiological and metabolic performance.\n\n**Data:** {json.dumps(self.athleteData)}",
            agent=physiologist_agent,
            expected_output="An evaluation of the athlete's physiological and metabolic performance, highlighting strengths, weaknesses, and areas for improvement."
        )

        scientific_review = Task(
            description=f"Compare results with scientific benchmarks.\n\n**Research Papers:** {json.dumps(self.researchResults['papers_summary'])}",
            agent=researcher_agent,
            expected_output="A comparative analysis of the athlete’s performance against scientific benchmarks, citing relevant research findings."
        )

        final_report = Task(
            description=f"Compile findings into a structured paper.\n\n**Benchmark Results:** {json.dumps(self.researchResults['benchmark_results'])}",
            agent=report_compiler,
            expected_output="A well-structured scientific report summarizing all findings, analyses, and comparisons, formatted for academic or professional review."
        )

        
        crew = Crew(
            agents=[coach_agent, physiologist_agent, researcher_agent, report_compiler],
            tasks=[biomechanical_analysis, physiological_evaluation, scientific_review, final_report]
        )

       
        results = crew.kickoff()  # Get outputs from all tasks
        print(type(results))  # Check the type
        print(dir(results))   # List available attributes and methods
        print(results)  
        # ✅ Convert task results into a JSON format
        results_json = {
            "Biomechanical Analysis": results.get(biomechanical_analysis, "Not Found"),
            "Physiological Evaluation": results.get(physiological_evaluation, "Not Found"),
            "Scientific Review": results.get(scientific_review, "Not Found"),
            "Final Report": results.get(final_report, "Not Found"),
        }

        # ✅ Save JSON File
        json_filename = "crew_results.json"
        with open(json_filename, "w", encoding="utf-8") as json_file:
            json.dump(results_json, json_file, indent=4, ensure_ascii=False)

        print(f"\n✅ Results saved to {json_filename}")

        # ✅ Print all task results (Optional)
        print("\n--- Task Results ---\n", json.dumps(results_json, indent=4))

        return results_json["Final Report"]

    def _generate_prompt(self):
        """Builds the complete structured prompt from template placeholders."""
        # Replacing placeholders with JSON data
        prompt_paper = prompt_paper_generator() 
        prompt_paper = prompt_paper.replace("[ATHLETE_DATA]", json.dumps(self.athleteData["athlete"]))
        prompt_paper = prompt_paper.replace("[ATHLETE_CONVERSATIONS]", json.dumps(self.athleteData["athleteConversations"]))
        prompt_paper = prompt_paper.replace("[EXPERT_CONVERSATIONS]", json.dumps(self.athleteData["expertConversations"]))

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