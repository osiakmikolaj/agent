from functions.get_absolute_path import get_absolute_path
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types

FUNCTIONS = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content,
    'get_absolute_path': get_absolute_path,
    'run_python_file': run_python_file,
    'write_file': write_file
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    # Call the function
    function_name = function_call_part.name
    if function_name in FUNCTIONS:
        function_to_call = FUNCTIONS[function_name]

        # Manually add working_directory to the args dictionary
        function_args = dict(function_call_part.args)
        function_args['working_directory'] = './calculator'

        function_result = function_to_call(**function_args)

        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
