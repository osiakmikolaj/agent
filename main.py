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



# Main loop
i = 0
while i < 20:
    i += 1
    try:
        # Response from the model
        model_response = client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=messages,
            config=config
        )

        # If content exists, append it to the messages
        if model_response.candidates is not None and model_response.candidates:
            for candidate in model_response.candidates:
                if candidate.content is not None:
                    messages.append(candidate.content)

        if model_response.candidates is not None and model_response.candidates and model_response.candidates[0].content is not None and model_response.candidates[0].content.parts is not None:
            parts = model_response.candidates[0].content.parts
        else:
            parts = None

        if parts and getattr(parts[0], "function_call", None) is not None:
            # Get function response as types.Content
            function_call_response = call_function(parts[0].function_call, if_verbose)

            messages.append(function_call_response)

            if function_call_response.parts is not None and function_call_response.parts[0].function_response is not None:
                call_output = function_call_response.parts[0].function_response.response
            else:
                call_output = None

            if call_output is None:
                raise Exception("Fatal error occurred!")

            if if_verbose:
                print(f"-> {call_output}")

        else:
            if hasattr(model_response, "text") and model_response.text:
                print(model_response.text)
                break

            if model_response.candidates:
                content = model_response.candidates[0].content
                if content and getattr(content, 'parts', None) and content.parts:
                    for part in content.parts:
                        text = getattr(part, "text", None)
                        if text:
                            print(text)
                            break

        # only print if --verbose flag is included
        if if_verbose:
            usage = model_response.usage_metadata
            prompt_tokens = getattr(usage, 'prompt_token_count', 0) if usage else 0
            completion_tokens = getattr(usage, 'completion_token_count', 0) if usage else 0
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {completion_tokens}")
    except Exception as e:
        print(f"Error occurred: {e}")
