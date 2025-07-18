import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

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

# Hardcoded system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info
    ]
)

config = types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

# response from the model
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=config
)

# Helper function
def get_function_call(response):
    try:
        return response.candidates[0].content.parts[0].function_call
    except (IndexError, AttributeError):
        return None

# Check for a function call
function_call_part = get_function_call(response)
if function_call_part:
    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print("No function call found in the response.")
    print(response.text)

# only print if --verbose flag is included
if if_verbose:
    usage = response.usage_metadata
    prompt_tokens = getattr(usage, 'prompt_token_count', 0) if usage else 0
    completion_tokens = getattr(usage, 'completion_token_count', 0) if usage else 0
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")
