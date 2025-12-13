import argparse

from google import genai
from google.genai import types

from config import MODEL, WORKING_DIR, ErrorMessage
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from llm_client import config, create_client, get_api_key, load_env


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


def generate_content(
    gen_ai_client: genai.Client,
    messages: list[types.Content],
    model: str,
    verbose: bool,
) -> types.GenerateContentResponse:
    response = gen_ai_client.models.generate_content(
        model=model, contents=messages, config=config
    )

    if response.usage_metadata is None:
        raise RuntimeError(ErrorMessage.API_REQUEST_FAILED)

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # add each candidates content to the message list
    if response.candidates:
        for candidate in response.candidates:
            if candidate.content:
                messages.append(candidate.content)

    # if no tools called, return
    if not response.function_calls:
        return response

    # call tools and collect parts
    function_responses: list[types.Part] = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)

        if (
            not function_call_result.parts
            or function_call_result.parts[0].function_response is None
            or function_call_result.parts[0].function_response.response is None
        ):
            raise RuntimeError("empty function call result")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")

        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise RuntimeError("no function responses generated. exiting...")

    messages.append(types.Content(role="user", parts=function_responses))
    return response


def main() -> None:
    load_env()
    cli_args = get_cli_args()

    try:
        gen_ai_client = create_client(get_api_key())
        initial_prompt = " ".join(cli_args.prompt)

        messages: list[types.Content] = [
            types.Content(role="user", parts=[types.Part(text=initial_prompt)])
        ]

        last_response_text: str | None = None
        last_had_function_calls: bool = False

        for i in range(20):
            response = generate_content(
                gen_ai_client, messages=messages, model=MODEL, verbose=cli_args.verbose
            )

            last_had_function_calls = bool(response.function_calls)

            if not last_had_function_calls:
                last_response_text = response.text

            finished = (not response.function_calls) and bool(
                response.text and response.text.strip()
            )
            if finished:
                print("Final response:")
                print(response.text)
                break

        else:
            details = []
            details.append(f"last_had_function_calls={last_had_function_calls}")
            details.append(
                f"last_response_text_present={bool(last_response_text and last_response_text.strip())}"
            )
            raise RuntimeError(
                "Reached max iterations (20) without finishing. " + ", ".join(details)
            )

    except Exception as ex:
        print(f"Error: {ex}")


if __name__ == "__main__":
    main()
