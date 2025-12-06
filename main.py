import argparse
import os
from typing import Final, TypedDict

from dotenv import load_dotenv
from google import genai

from constants import ErrorMessage, Model

ENV_GEMINI_API_KEY: Final = "GEMINI_API_KEY"


class GenerationResult(TypedDict):
    user_prompt: str
    prompt_token_count: int | None
    response_token_count: int | None
    response_text: str | None


def load_env() -> None:
    load_dotenv()


def get_user_prompt() -> str:
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", nargs="+", help="User prompt")
    args = parser.parse_args()
    return " ".join(args.prompt)


def get_api_key() -> str:
    """Load and validate GEMINI_API_KEY from .env"""
    api_key = os.getenv(ENV_GEMINI_API_KEY)
    if not api_key:
        raise RuntimeError(ErrorMessage.NO_API_KEY)
    return api_key


def create_client(api_key: str) -> genai.Client:
    """Create Gemini client"""
    return genai.Client(api_key=api_key)


def gen_content_with_usage(
    gen_ai_client: genai.Client,
    prompt: str,
    model: Model = Model.FLASH_25,
) -> GenerationResult:
    """Generate test response from Gemini"""

    response = gen_ai_client.models.generate_content(model=model, contents=prompt)

    if response.usage_metadata is None:
        raise RuntimeError(ErrorMessage.API_REQUEST_FAILED)

    return {
        "user_prompt": prompt,
        "prompt_token_count": response.usage_metadata.prompt_token_count,
        "response_token_count": response.usage_metadata.candidates_token_count,
        "response_text": response.text,
    }


def print_gen_result(result: GenerationResult) -> None:
    """Prints formatted result"""

    print(f"User prompt: {result['user_prompt']}")
    print(f"Prompt tokens: {result['prompt_token_count']}")
    print(f"Response tokens: {result['response_token_count']}")
    print(f"Response: {result['response_text']}")


def main() -> None:
    load_env()

    try:
        gen_ai_client = create_client(get_api_key())
        user_prompt = get_user_prompt()
        result = gen_content_with_usage(gen_ai_client, prompt=user_prompt)
        print_gen_result(result)

    except Exception as ex:
        print(f"Error: {ex}")


if __name__ == "__main__":
    main()
