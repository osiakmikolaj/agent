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

# System prompt
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

# Check if response is a function call
if isinstance(response, types.FunctionCall):
    # Get function response as types.Content
    result = call_function(response)

    try:
        function_response = result.parts[0].function_response.response # type: ignore
    except Exception as e:
        raise Exception(f"Error: {str(e)}")

    if function_response is None:
        raise Exception("Fatal error occurred!")

    if if_verbose:
        print(f"-> {function_response}")

else:
    print("No function call found in the response.")
    # Check if response has text attribute
    if hasattr(response, "text"):
        print(response.text)
    else:
        print(response)



# only print if --verbose flag is included
if if_verbose:
    usage = response.usage_metadata
    prompt_tokens = getattr(usage, 'prompt_token_count', 0) if usage else 0
    completion_tokens = getattr(usage, 'completion_token_count', 0) if usage else 0
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {completion_tokens}")
