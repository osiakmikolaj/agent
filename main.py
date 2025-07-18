import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.get_file_content import schema_get_file_content
from functions.call_function import call_function

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
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_file,
        schema_run_python_file,
        schema_get_file_content
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

# Helper functions
def get_function_call(response):
    try:
        return response.candidates[0].content.parts[0].function_call
    except (IndexError, AttributeError):
        return None

def get_function_response(function_call_result):
    if not function_call_result:
        return None

    parts = getattr(function_call_result, 'parts', None)
    if not parts or len(parts) == 0:
        return None

    function_response_obj = getattr(parts[0], 'function_response', None)
    if not function_response_obj:
        return None

    return getattr(function_response_obj, 'response', None)

# Check for a function call
function_call_part = get_function_call(response)
if function_call_part:
    # Call the function
    function_call_result = call_function(function_call_part)

    function_response = get_function_response(function_call_result)

    if function_response is None:
        raise RuntimeError("call_function did not return expected types.Content structure")

    if if_verbose:
        print(f"-> {function_response}")
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
