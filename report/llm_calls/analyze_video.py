import os
import base64
from anthropic import Anthropic
from utils.get_alfred_ai_response import get_alfred_ai_response
import concurrent.futures
# Initialize Anthropic API Client
anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def encode_image_to_base64(image_path):
    """Convert an image file to a base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def analyze_frame_group(frames, prompt=''):
    """Send a group of frames for analysis to Claude AI."""
    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": frame
                        }
                    } for frame in frames
                ]
            }
        ]

        response = anthropic.messages.create(
                        model="claude-3-5-sonnet-20240620",
                        max_tokens=8192,
                        temperature=1,
                        system=prompt + '\n\n Rispondi solo ed esclusivamente in italiano.',
                        messages=messages,
                        # headers={'anthropic-beta': 'max-tokens-3-5-sonnet-2024-07-15'}
                    )

        print("FRAMES analysis result:", response.content[0].text)
        return response.content[0].text
    except Exception as error:
        print("Error calling Anthropic API:", error)
        raise error


# def analyze_video(frames_folder, user_prompt=''):
#     """Analyzes a video using frames stored in a folder."""
#     # try:
#     frame_files = sorted(os.listdir(frames_folder))
#     frames = [encode_image_to_base64(os.path.join(frames_folder, frame)) for frame in frame_files if frame.endswith(('.jpg', '.jpeg', '.png'))]

#     frame_groups = [frames[i:i+100] for i in range(0, len(frames), 100)]
#     analyses = []

#     total_length_video = len(frames) // 30
#     print(f'Total video length: {total_length_video} secondi')

#     analyses.append(f'Total video length: {total_length_video} secondi. \n\n')

#     prompt_frames = (f'Data questa serie di frame appartenenti a un video più ampio e la richiesta dell\'utente: "{user_prompt}", '
#                         f'generare un prompt dettagliato per analizzare questo gruppo di frame. Il prompt deve guidare l\'analisi in modo da soddisfare '
#                         f'la richiesta dell\'utente. Rispondi semplicemente con il prompt in italiano senza aggiungere commenti o considerazioni.')

#     group_prompt = get_alfred_ai_response(prompt_frames)

#     for i, group in enumerate(frame_groups):
#         start_second = round(i * 100 / 30, 2)
#         end_second = min(round((i + 1) * 100 / 30, 2), total_length_video)
#         print(f"Analyzing video segment from {start_second}s to {end_second}s")

#         analysis = (f"Risultati dell'analisi dei segmenti del video dal secondo {start_second}s al {end_second}s: \n\n"
#                     f"{analyze_frame_group(group, group_prompt)}")

#         analyses.append(analysis)

#     # Final Analysis
#     complete_analysis_prompt = (f"Effettua un'analisi completa e dettagliata basandoti sui risultati delle analisi parziali dei seguenti frame. "
#                                 f"Nella tua analisi finale, tieni sempre in considerazione la richiesta iniziale dell'utente: \"{user_prompt}\". "
#                                 f"Ecco le analisi parziali dei frame: \n\n {chr(10).join(analyses)}. "
#                                 f"Rispondi semplicemente con l'analisi finale senza aggiungere commenti o considerazioni.")

#     print("completeAnalysisPrompt:", complete_analysis_prompt)
#     final_analysis = get_alfred_ai_response(complete_analysis_prompt)

#     print("Final Analysis:", final_analysis)
#     return final_analysis

    # except Exception as error:
    #     print("Analyze Video error:", error)
    #     return ""

def analyze_video(frames_folder, user_prompt=''):
    """Analyzes a video using frames stored in a folder using multithreading."""
    
    # Read and encode frames
    frame_files = sorted(os.listdir(frames_folder))
    frames = [encode_image_to_base64(os.path.join(frames_folder, frame)) for frame in frame_files if frame.endswith(('.jpg', '.jpeg', '.png'))]

    # Divide frames into batches of 100
    frame_groups = [frames[i:i+100] for i in range(0, len(frames), 100)]
    total_length_video = len(frames) // 30
    print(f'Total video length: {total_length_video} secondi')

    analyses = [f'Total video length: {total_length_video} secondi. \n\n']
    
    # Generate prompt for AI analysis
    prompt_frames = (f'Data questa serie di frame appartenenti a un video più ampio e la richiesta dell\'utente: "{user_prompt}", '
                     f'generare un prompt dettagliato per analizzare questo gruppo di frame. Il prompt deve guidare l\'analisi in modo da soddisfare '
                     f'la richiesta dell\'utente. Rispondi semplicemente con il prompt in italiano senza aggiungere commenti o considerazioni.')
    
    group_prompt = get_alfred_ai_response(prompt_frames)

    # Function to analyze a single group
    def analyze_segment(i, group):
        start_second = round(i * 100 / 30, 2)
        end_second = min(round((i + 1) * 100 / 30, 2), total_length_video)
        print(f"Analyzing video segment from {start_second}s to {end_second}s")
        
        analysis_result = analyze_frame_group(group, group_prompt)
        return i, (f"Risultati dell'analisi dei segmenti del video dal secondo {start_second}s al {end_second}s: \n\n{analysis_result}")

    # Use ThreadPoolExecutor for parallel execution
    results = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(analyze_segment, i, group): i for i, group in enumerate(frame_groups)}

        for future in concurrent.futures.as_completed(futures):
            i, analysis = future.result()
            results[i] = analysis  # Store results by index

    # Append results in the correct order
    for i in sorted(results.keys()):
        analyses.append(results[i])

    # Final AI-Based Analysis
    complete_analysis_prompt = (f"Effettua un'analisi completa e dettagliata basandoti sui risultati delle analisi parziali dei seguenti frame. "
                                f"Nella tua analisi finale, tieni sempre in considerazione la richiesta iniziale dell'utente: \"{user_prompt}\". "
                                f"Ecco le analisi parziali dei frame: \n\n {chr(10).join(analyses)}. "
                                f"Rispondi semplicemente con l'analisi finale senza aggiungere commenti o considerazioni.")

    print("completeAnalysisPrompt:", complete_analysis_prompt)
    final_analysis = get_alfred_ai_response(complete_analysis_prompt)

    print("Final Analysis:", final_analysis)
    return final_analysis