import requests
import json

def build_prompt(user_input):
    system_prompt = """
    You are FunFit AI, a fitness assistant.

    Your job is to answer user questions related to:
    - fitness
    - workouts
    - diet
    - calories
    - daily health habits

    Rules:
    - use the revievent emojis
    - Keep answers short and practical
    - don't make the tables and
    - Give actionable advice
    - Use simple language
    - Prefer Indian context when suggesting food
    - Avoid unsafe or extreme advice
    """

    final_prompt = system_prompt + "\n\nUser: " + user_input + "\nAI:"

    return final_prompt

from flask import Response

def stream_response(user_input):
    full_prompt = build_prompt(user_input)

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": "Bearer Opwnrouter_API",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-oss-120b:free",
        "messages": [
            {"role": "user", "content": full_prompt}
        ],
        "stream": True   # 🔥 IMPORTANT
    }

    def generate():
        with requests.post(url, headers=headers, json=data, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    decoded = line.decode("utf-8")

                    if decoded.startswith("data: "):
                        chunk = decoded.replace("data: ", "")

                        if chunk == "[DONE]":
                            break

                        try:
                            json_data = json.loads(chunk)
                            content = json_data['choices'][0]['delta'].get('content', '')
                            if content:
                                yield content
                        except:
                            continue

    return Response(generate(), mimetype='text/plain')