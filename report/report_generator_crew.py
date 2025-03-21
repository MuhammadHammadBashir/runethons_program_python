import json
from crewai import Agent, Task, Crew
from langchain.llms import Gemini
from prompt.promptPaperGenerator import prompt_paper_generator
class ScientificPaperCrew:
    def __init__(self, athleteData, videoAnalysis, researchResults):
        self.athleteData = athleteData
        self.videoAnalysis = videoAnalysis
        self.researchResults = researchResults
        self.llm = Gemini(model_name="gemini-1.5-pro-002")

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

        # ✅ Define Task-Specific Prompts
        biomechanical_analysis = Task(
            description=f"Analyze the athlete’s video performance based on keypoints, angles, and velocities.\n\n**Video Analysis:** {json.dumps(self.videoAnalysis)}",
            agent=coach_agent
        )

        physiological_evaluation = Task(
            description=f"Assess the athlete’s physiological and metabolic performance.\n\n**Data:** {json.dumps(self.athleteData)}",
            agent=physiologist_agent
        )

        scientific_review = Task(
            description=f"Compare results with scientific benchmarks.\n\n**Research Papers:** {json.dumps(self.researchResults['papers_summary'])}",
            agent=researcher_agent
        )

        final_report = Task(
            description=f"Compile findings into a structured paper.\n\n**Benchmark Results:** {json.dumps(self.researchResults['benchmark_results'])}",
            agent=report_compiler
        )

        # ✅ Create Crew
        crew = Crew(
            agents=[coach_agent, physiologist_agent, researcher_agent, report_compiler],
            tasks=[biomechanical_analysis, physiological_evaluation, scientific_review, final_report]
        )

        return crew.kickoff()

    def _generate_prompt(self):
        """Builds the complete structured prompt from template placeholders."""
        # Replacing placeholders with JSON data
        prompt_paper = prompt_paper_generator() 
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