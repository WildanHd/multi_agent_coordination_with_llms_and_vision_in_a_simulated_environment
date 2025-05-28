# agents/processing_agent.py
import openai
import json
from pathlib import Path

# Set OpenRouter.ai API config
openai.api_key = "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"  
openai.api_base = "https://openrouter.ai/api/v1"

def plan_route_with_llm(vision_output_path, output_path="output/llm_route_output.json"):
    # Load vision agent output
    with open(vision_output_path, 'r') as f:
        vision_data = json.load(f)

    prompt = f"""
    You are a helpful AI agent. Your task is to find the shortest path from the start to the finish position in a 5x5 grid with index start from 0 to 4 and both 0 indexes are in the most top left.
    You have to avoid all objects.
    Here you can use input data with coordinate x, y:
    Input:
    {json.dumps(vision_data, indent=2)}
    Now:
    1. Write the positions of all objects, start, and finish
    2. Generate the shortest path from start to finish avoiding all objects with format [move two step to the right, move one step up, etc] only
    """

    response = openai.ChatCompletion.create(
        model="mistralai/mistral-7b-instruct",  # You can try other models too
        messages=[
            {"role": "system", "content": "You are a pathfinding assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    actions = response['choices'][0]['message']['content']

    # Save result to file
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump({"route": actions}, f, indent=2)

    print(f"Saved route output to: {output_path}")
    return actions


