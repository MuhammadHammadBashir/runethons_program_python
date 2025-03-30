import json
import re
from utils.get_alfred_ai_response import  get_alfred_ai_response
from web_expert import WebExpert
from prompt.promptWebSearch import prompt_web_search
from prompt.promptResearchSummary import prompt_research_summary
from prompt.promptBenchMarkResults import prompt_benchmark_results
from llm_calls.scientific_search import scientific_search
class ResearchModule:
    def conduct_research(self, athleteData, videoAnalysis):
        # Create a shallow copy (similar to spread operator `{...videoAnalysis}`)
        videoAnalysisTemp = videoAnalysis.copy()

        # Extract videoAnalysis from the copied dictionary
        descriptionVideoAnalysis = videoAnalysisTemp.get("videoAnalysis")

        # Delete the specified keys
        videoAnalysisTemp.pop("videoAnalysis", None)
        videoAnalysisTemp.pop("videoFrames", None)

        prompt = f"""
        You are a researcher who studies a specific athlete. You have available:

        1. The personal data of the athlete
        2. A video analysis of its performance

        Your goal is to find a scientific article on Google Scholar who:

        1. Best interprets your video analysis
        2. Contextualizes the athlete's data
        3. Provides useful information to complete your research

        The article should fill the gaps in your understanding and offer ideas for insights.

        ## Here the athlete's data: 
        {json.dumps(athleteData['athlete'])}

        # Here the evaluation carried out with measurements through pose estimation of the video:
        {json.dumps(videoAnalysisTemp)}

        # Here the results of the Full Video Frame Analysis with more in-depth assessments of the video:
        {descriptionVideoAnalysis}

        On the basis of this, suggest some research queries to be used on Google Scholar to find relevant articles.
        Provide only the query in JSON format: ["Query1", "Query2"].
        Do not add any explanation, comment, or explanation, answer only with the query in JSON format.
        """
        
        print("conduct_research > prompt:", prompt)
        
        queries = get_alfred_ai_response(prompt, 'gemini', False, '', 1)
        queries = self.extract_json_from_text(queries)
        html_ai_results= self.search_scientific_papers(queries, max_results=10)
        research_summary_list = []
        research_bibliography_list = []
        bench_mark_result_list  = []
        for ai_result in html_ai_results:
            prompt_for_research_summary =prompt_research_summary(ai_result,athleteData,videoAnalysisTemp,descriptionVideoAnalysis)
            search_results = scientific_search(prompt_for_research_summary)
            search_results = search_results.model_dump()
            papers_summary, bibliography = search_results["research_summary"], search_results["bibliography"]
            benchmark_prompt = prompt_benchmark_results(athleteData, videoAnalysisTemp, descriptionVideoAnalysis, papers_summary)
            bench_mark_result = get_alfred_ai_response(benchmark_prompt,'gemini')
            bench_mark_result_list.append(bench_mark_result)
            research_summary_list.append(papers_summary)
            research_bibliography_list.append(bibliography)


        return research_bibliography_list

    def extract_json_from_text(self,testo):
        # Look for a sequence that starts with [ and ends with ]
        match = re.search(r'\[[\s\S]*\]', testo)
        
        if match:
            try:
                # Try to parse the found JSON
                return json.loads(match.group(0))
            except json.JSONDecodeError as error:
                print("JSON parsing error:", error)
                return None
        else:
            print("No JSON array found in the text")
            return None
         
    def search_scientific_papers(self,queries, max_results=2):

        # Look for a sequence that starts with [ and ends with ]
        # Create instance
        web_expert = WebExpert()

        # Get PDF links
        pdf_links = web_expert.get_pdf_links(queries,max_results)

        html_results = []
        html_ai_results = []
        summary_pdf_urls = []
        for query, links in pdf_links.items():
            for link in links:
                html_result = web_expert.get_page_html(link)
                html_results.append(html_result)
                search_prompt =prompt_web_search(html_result)
                ai_result = get_alfred_ai_response(search_prompt, 'gemini')
                
                html_ai_results.append(ai_result)

                # print(f" - {link}")

        # Close the driver after all operations
        web_expert.close()

        return html_ai_results
        


