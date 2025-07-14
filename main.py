import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python_file, run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
verbose = False
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
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

def call_function(function_call_part, verbose=False):
    
   
    function_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    if function_call_part.name in function_dict:
        args = dict(function_call_part.args)
        args["working_directory"] = "calculator"
        function_result = function_dict[function_call_part.name](**args)
        if verbose == True:
            print(f"Calling function: {function_call_part.name}({args})")
        else:
            print(f" - Calling function: {function_call_part.name}")
        #print(function_result)
    else:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )

def main():
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
    verbose = "--verbose" in sys.argv
    if not args:
        sys.exit("prompt must be provided")

    user_prompt = " ".join(args)
    if verbose:
        print(f"User prompt:", user_prompt)
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    loop = 0
    while True:
        loop += 1
        if loop > 20:
            print("Loop 20 exit.")
            sys.exit(1)
            
        try:
            final = generate_content(client, messages, verbose)
            if final:
                print("Final response:")
                print(final)
                break
            
        except Exception as e:
            print(f"ERROR: {e} on loop {loop}")

        

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=system_prompt
                    ),
                )
    if verbose:
        print(f"Prompt tokens:", response.usage_metadata.prompt_token_count)
        print(f"Response tokens:", response.usage_metadata.candidates_token_count)
    if response.candidates:
        for candidate in response.candidates:
            content = candidate.content
            messages.append(content)
    
    if not response.function_calls:
        return response.text
    
    response_functions = []
    r_funcs = response.function_calls
    for function in r_funcs:
        if verbose:
            print(f"Calling function: {function.name}({function.args})")    
        result = call_function(function, verbose)   
        if not result.parts or not result.parts[0].function_response:
            raise Exception("empty function call result")
        if verbose:
            print(f"->: {result.parts[0].function_response.response}")
        response_functions.append(result.parts[0])
    messages.append(types.Content(role="tool", parts=response_functions))

if __name__ == "__main__":
    main()