# import copy
# import re
# import json
# from prompt.promptSearchScientificResults import prompt_search_scientific_results
# from prompt.promptBenchMarkResults import prompt_benchmark_results
# from llm_calls.scientific_search import scientific_search
# from llm_calls.benchmark_result import benchmark_result
# from utils.get_alfred_ai_response import get_alfred_ai_response
# class ResearchModule:
#     def conduct_research(self,athleteData, videoAnalysis):
#         # Create a shallow copy (similar to spread operator `{...videoAnalysis}`)
#         videoAnalysisTemp = videoAnalysis.copy()

#         # Extract videoAnalysis from the copied dictionary
#         descriptionVideoAnalysis = videoAnalysisTemp.get("videoAnalysis")

#         # Delete the specified keys
#         videoAnalysisTemp.pop("videoAnalysis", None)
#         videoAnalysisTemp.pop("videoFrames", None)

#         benchmark_result_list = []

#         search_prompt = prompt_search_scientific_results(athleteData,videoAnalysisTemp,descriptionVideoAnalysis)

#         search_results = scientific_search(search_prompt)
#         papers_summary, bibliography_data =  self.seperating_bibliography(search_results)
        
#         for paper in bibliography_data:
#             scientific_paper_json = json.dumps(paper, indent=2)
#             benchmark_prompt = prompt_benchmark_results(athleteData,videoAnalysisTemp,descriptionVideoAnalysis,scientific_paper_json)
#             result  = get_alfred_ai_response(benchmark_prompt)
#             benchmark_result_list.append(result)
        
#         return {
#                 "papers_summary": papers_summary,
#                 "benchmark_results": benchmark_result_list
#             }

    
#     def seperating_bibliography(self,search_results):
        
#         bibliography_pattern = re.search(r"```json\n(\[.*?\])\n```", search_results, re.DOTALL)

#         if bibliography_pattern:
#             bibliography_json = bibliography_pattern.group(1)  # Extract JSON content
#             bibliography_data = json.loads(bibliography_json)  # Convert to Python object

#             # Remove the bibliography section from the main text
#             analysis_text = re.sub(r"```json\n\[.*?\]\n```", "", search_results, flags=re.DOTALL).strip()

#             # print("### Analysis Text ###\n", analysis_text)

#             return analysis_text, bibliography_data
#             # print("\n### Bibliography (JSON Format) ###")
#             # print(json.dumps(bibliography_data, indent=4))
#         else:
#             print("No bibliography section found.")
#             return "not found", "not found"


import concurrent.futures
import copy
import re
import json
from prompt.promptSearchScientificResults import prompt_search_scientific_results
from prompt.promptBenchMarkResults import prompt_benchmark_results
from llm_calls.scientific_search import scientific_search
from llm_calls.benchmark_result import benchmark_result
from utils.get_alfred_ai_response import get_alfred_ai_response
from pydantic import BaseModel, HttpUrl
from typing import List, Optional
import json

class BibliographyEntry(BaseModel):
    title: str
    authors: List[str]
    year: int
    source: str
    doi: Optional[HttpUrl]  # Can be None if unavailable

class ResearchOutput(BaseModel):
    research_summary: str
    bibliography: List[BibliographyEntry]

class ResearchModule:
    def conduct_research(self, athleteData, videoAnalysis):
        # Create a shallow copy (similar to spread operator `{...videoAnalysis}`)
        videoAnalysisTemp = videoAnalysis.copy()

        # Extract videoAnalysis from the copied dictionary
        descriptionVideoAnalysis = videoAnalysisTemp.get("videoAnalysis")

        # Delete the specified keys
        videoAnalysisTemp.pop("videoAnalysis", None)
        videoAnalysisTemp.pop("videoFrames", None)

        benchmark_result_list = []

        # Generate the search prompt
        search_prompt = prompt_search_scientific_results(athleteData, videoAnalysisTemp, descriptionVideoAnalysis)

        # Fetch search results

        try:
            search_results = scientific_search(search_prompt)
            # search_results = get_alfred_ai_response(search_prompt,'gemini')
            print("Validated Research Results:", search_results.model_dump_json(indent=2))

        except ValueError as e:
            print(e)

        # try:
        #     json_text = scientific_search(search_prompt)
        #     structured_output = json.loads(json_text)
            
        #     # Validate using Pydantic
        #     search_results = ResearchOutput(**structured_output)
        # except Exception as e:
        #     print(f"Error parsing LLM response: {e}")
            
        search_results = search_results.model_dump()
        data = {"content": search_results}  # Store the text inside a dictionary

        with open("sonar_output.json", "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)  # Save JSON with formatting
        # papers_summary, bibliography_data = self.seperating_bibliography(search_results)
        papers_summary, bibliography = search_results["research_summary"], search_results["bibliography"]
        research_output = {
                "research_summary": papers_summary,
                "bibliography": bibliography
            }

            # Save to JSON file
        with open('research_bib.json', "w", encoding="utf-8") as f:
                json.dump(research_output, f, indent=4, ensure_ascii=False)

        
        # ✅ Add multithreading for concurrent execution
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(self.process_paper, athleteData, videoAnalysisTemp, descriptionVideoAnalysis, paper): paper
                for paper in bibliography
            }

            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    benchmark_result_list.append(result)
                except Exception as e:
                    print(f"Error processing paper: {e}")

        return {
            "papers_summary": papers_summary,
            "benchmark_results": benchmark_result_list
        }

    def process_paper(self, athleteData, videoAnalysisTemp, descriptionVideoAnalysis, paper):
        """
        Helper function to process a single paper.
        """
        scientific_paper_json = json.dumps(paper, indent=2)
        benchmark_prompt = prompt_benchmark_results(athleteData, videoAnalysisTemp, descriptionVideoAnalysis, scientific_paper_json)
        return get_alfred_ai_response(benchmark_prompt,'gemini')

    def seperating_bibliography(self, search_results, save_path="research_summary_bibliography.json"):
        bibliography_pattern = re.search(r"```json\n(\[.*?\])\n```", search_results, re.DOTALL)

        if bibliography_pattern:
            bibliography_json = bibliography_pattern.group(1)  # Extract JSON content
            bibliography_data = json.loads(bibliography_json)  # Convert to Python object

            # Remove the bibliography section from the main text
            analysis_text = re.sub(r"```json\n\[.*?\]\n```", "", search_results, flags=re.DOTALL).strip()
                    # Create structured dictionary
            research_output = {
                "research_summary": analysis_text,
                "bibliography": bibliography_data
            }

            # Save to JSON file
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(research_output, f, indent=4, ensure_ascii=False)
            return analysis_text, bibliography_data
        else:
            print("No bibliography section found.")
            return "not found", "not found"
