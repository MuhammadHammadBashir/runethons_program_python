import copy
import re
import json
from prompt.promptSearchScientificResults import prompt_search_scientific_results
from prompt.promptBenchMarkResults import prompt_benchmark_results
from llm_calls.scientific_search import scientific_search
from llm_calls.benchmark_result import benchmark_result
class ResearchModule:
    def conduct_research(self,athleteData, videoAnalysis):
        # Create a shallow copy (similar to spread operator `{...videoAnalysis}`)
        videoAnalysisTemp = videoAnalysis.copy()

        # Extract videoAnalysis from the copied dictionary
        descriptionVideoAnalysis = videoAnalysisTemp.get("videoAnalysis")

        # Delete the specified keys
        videoAnalysisTemp.pop("videoAnalysis", None)
        videoAnalysisTemp.pop("videoFrames", None)

        benchmark_result_list = []

        search_prompt = prompt_search_scientific_results(athleteData,videoAnalysisTemp,descriptionVideoAnalysis)

        search_results = scientific_search(search_prompt)
        papers_summary, bibliography_data =  self.seperating_bibliography(search_results)
        
        for paper in bibliography_data:
            scientific_paper_json = json.dumps(paper, indent=2)
            benchmark_prompt = prompt_benchmark_results(athleteData,videoAnalysisTemp,descriptionVideoAnalysis,scientific_paper_json)
            result  = benchmark_result(benchmark_prompt)
            benchmark_result_list.append(result)
        
        return {
                "papers_summary": papers_summary,
                "benchmark_results": benchmark_result_list
            }

    
    def seperating_bibliography(self,search_results):
        
        bibliography_pattern = re.search(r"```json\n(\[.*?\])\n```", search_results, re.DOTALL)

        if bibliography_pattern:
            bibliography_json = bibliography_pattern.group(1)  # Extract JSON content
            bibliography_data = json.loads(bibliography_json)  # Convert to Python object

            # Remove the bibliography section from the main text
            analysis_text = re.sub(r"```json\n\[.*?\]\n```", "", search_results, flags=re.DOTALL).strip()

            # print("### Analysis Text ###\n", analysis_text)

            return analysis_text, bibliography_data
            # print("\n### Bibliography (JSON Format) ###")
            # print(json.dumps(bibliography_data, indent=4))
        else:
            print("No bibliography section found.")
            return "not found", "not found"
