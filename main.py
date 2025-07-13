import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# get gemini key from env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

if_verbose = False

# get user promt and optional argument from sys.argv
if len(sys.argv) > 1:
    user_prompt = sys.argv[1]
    if len(sys.argv) > 2:
        if sys.argv[2] == "--verbose":
            if_verbose = True
        else:
            print("Error! Invalid argument!")
            print("Aavailable arguments: --verbose")
            sys.exit(1)
else:
    print("Error! No prompt provided")
    print("Usage: uv run main.py <prompt> <optional argument>")
    sys.exit(1)

# list of all user prompts
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]

# response from the model
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)

# printing out the response and meta data
print(response.text)

# only print if --verbose flag is included
if if_verbose:
    usage = response.usage_metadata
    prompt_tokens = getattr(usage, 'prompt_token_count', 0) if usage else 0
    completion_tokens = getattr(usage, 'completion_token_count', 0) if usage else 0
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")
