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

# Client will be initialized in setup_client()

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

def setup_client():
    """Initialize the Gemini client and configuration"""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

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

    return client, config

def has_function_call(response):
    """Check if the response contains a function call in any part"""
    try:
        if not (response.candidates and response.candidates[0].content and response.candidates[0].content.parts):
            return False

        # Check all parts for function calls
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call') and part.function_call is not None:
                return True
        return False
    except (IndexError, AttributeError):
        return False

def get_text_content(response):
    """Extract text content from response"""
    try:
        if hasattr(response, "text") and response.text:
            return response.text

        if response.candidates and response.candidates[0].content:
            content = response.candidates[0].content
            if content.parts:
                for part in content.parts:
                    if hasattr(part, "text") and part.text:
                        return part.text
    except (IndexError, AttributeError):
        pass
    return None

def handle_function_call(response, messages, verbose):
    """Handle function call in response"""
    try:
        # Find the part with the function call
        function_call_part = None
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call') and part.function_call is not None:
                function_call_part = part.function_call
                break

        if not function_call_part:
            return False

        function_call_response = call_function(function_call_part, verbose)

        # Add function response to messages
        messages.append(function_call_response)

        # Extract and validate the result
        if (function_call_response.parts and
            function_call_response.parts[0].function_response and
            function_call_response.parts[0].function_response.response):

            call_output = function_call_response.parts[0].function_response.response
            if verbose:
                print(f"-> {call_output}")
            return True  # Continue conversation
        else:
            raise Exception("Fatal error: Function call returned invalid response")

    except Exception as e:
        print(f"Error in function call: {e}")
        return False

def print_usage_stats(response, user_prompt, verbose):
    """Print usage statistics if verbose mode is enabled"""
    if verbose:
        usage = response.usage_metadata
        prompt_tokens = getattr(usage, 'prompt_token_count', 0) if usage else 0
        completion_tokens = getattr(usage, 'completion_token_count', 0) if usage else 0
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {completion_tokens}")

def main_conversation_loop(client, config, user_prompt, verbose):
    """Main conversation loop with the AI"""
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    max_iterations = 20
    for i in range(max_iterations):
        try:
            # Get response from model
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=config
            )

            # Add response to conversation history
            if response.candidates:
                for candidate in response.candidates:
                    if candidate.content:
                        messages.append(candidate.content)

            # Check for both text and function calls
            text_content = get_text_content(response)
            has_func_call = has_function_call(response)

            # Print any text content first
            if text_content:
                print(text_content)

            # Handle function calls if present
            if has_func_call:
                should_continue = handle_function_call(response, messages, verbose)
                if not should_continue:
                    break
            else:
                # No function call and we have text - this likely ends the conversation
                if text_content:
                    print_usage_stats(response, user_prompt, verbose)
                    break
                else:
                    print("No response content found")
                    break

            # Print usage stats for this iteration if verbose (for function call iterations)
            if verbose and has_func_call:
                print_usage_stats(response, user_prompt, verbose)

        except Exception as e:
            print(f"Error occurred: {e}")
            break

# Initialize and run
client, config = setup_client()
main_conversation_loop(client, config, user_prompt, if_verbose)
