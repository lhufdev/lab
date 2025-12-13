import argparse
from typing import TypedDict

from google import genai
from google.genai import types

from config import MODEL, WORKING_DIR, ErrorMessage
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from llm_client import config, create_client, get_api_key, load_env


class GenerationResult(TypedDict):
    # Normalised shape of model response
    user_prompt: str
    prompt_token_count: int | None
    response_token_count: int | None
    response_text: str


def get_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", nargs="+", help="user prompt")
    parser.add_argument("--verbose", action="store_true", help="enable verbose output")
    return parser.parse_args()


def call_function(function_call_part, verbose: bool = False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call_part.name
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    function_result = function_map[function_name](**args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name, response={"result": function_result}
            )
        ],
    )


def gen_content_with_usage(
    gen_ai_client: genai.Client,
    prompt: str,
    model: str,
    verbose: bool = False,
) -> GenerationResult:
    """Generate response from Gemini"""

    # Wrap user prompt in required Gemini content format
    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    response = gen_ai_client.models.generate_content(
        model=model, contents=messages, config=config
    )

    # usage_metadata requrired for token accounting
    if response.usage_metadata is None:
        raise RuntimeError(ErrorMessage.API_REQUEST_FAILED)

    # If present prefer function calls, otherwise fallback to text
    # Ensure response_text is always string
    function_call_parts: list[types.Part] = []
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=verbose)

            if (
                not function_call_result.parts
                or function_call_result.parts[0].function_response is None
                or function_call_result.parts[0].function_response.response is None
            ):
                raise RuntimeError(
                    "Fatal: tool response is missing function_response.response"
                )

            function_call_parts.append(function_call_result.parts[0])

            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        response_text = ""

    elif response.text is not None:
        response_text = response.text
    else:
        response_text = ""

    return {
        "user_prompt": prompt,
        "prompt_token_count": response.usage_metadata.prompt_token_count,
        "response_token_count": response.usage_metadata.candidates_token_count,
        "response_text": response_text,
    }


def print_gen_result(result: GenerationResult, verbose_mode: bool) -> None:
    """Prints formatted result"""
    if verbose_mode:
        print(f"User prompt: {result['user_prompt']}")
        print(f"Prompt tokens: {result['prompt_token_count']}")
        print(f"Response tokens: {result['response_token_count']}")

    if result["response_text"]:
        print(f"Response: {result['response_text']}")


def main() -> None:
    load_env()
    cli_args = get_cli_args()

    try:
        gen_ai_client = create_client(get_api_key())
        initial_prompt = " ".join(cli_args.prompt)
        result = gen_content_with_usage(
            gen_ai_client, prompt=initial_prompt, model=MODEL, verbose=cli_args.verbose
        )
        print_gen_result(result, cli_args.verbose)

    except Exception as ex:
        print(f"Error: {ex}")


if __name__ == "__main__":
    main()
