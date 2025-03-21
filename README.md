Python version of runnethons_program

1) Concurrency in api calls

2) Intelligent filtering

3) The difficult part till video anaylsucs and preliminrayr report generation is done,  now research modele is remaining in python

4) The last step of work of Asynchronous Processing Pipeline since python is good at modular level concurrency
   Concurrency has been added for the videoanalysics via frame grouping


Creating the virtual environment and installing dependencies

python3.11.5 -m venv runethons

source runethons/bin/activate

pip install -r requirements.txt

20-21 March updates

1) Research module updated takes makes the preplexity api calls to generate results with promptSearchScinetificResults.py from prompts and get the summarized results along with the bibliography in json

2) For each bibliogpagy object make the benchmark results and put in list based on promptBenchMarkResults.py with the openai call

3) Updated the simple report_generator class report_generator

4) Updated 4 agents crew at report level generations using crewai and langchain library,  each agents coarch,  doctor, researches and report compiler work in parallel,  they also communcuiated based on memory report_generator_crew

5) Requirements.txt updated

6) Find a bug at angle velocity creation

7) waiting for athlete data to run system in one go