import copy

class ResearchModule:
    def conduct_research(self,athleteData, videoAnalysis):
        # Create a shallow copy (similar to spread operator `{...videoAnalysis}`)
        videoAnalysisTemp = videoAnalysis.copy()

        # Extract videoAnalysis from the copied dictionary
        descriptionVideoAnalysis = videoAnalysisTemp.get("videoAnalysis")

        # Delete the specified keys
        videoAnalysisTemp.pop("videoAnalysis", None)
        videoAnalysisTemp.pop("videoFrames", None)

        print(descriptionVideoAnalysis)
