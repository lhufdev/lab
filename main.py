import os
from typing import Final

from dotenv import load_dotenv
from google import genai

from constants import ERR_API_KEY_IS_NONE, MODEL_FLASH_25, TEST_PROMPT

ENV_GEMINI_API_KEY: Final = "GEMINI_API_KEY"


def get_api_key() -> str:
    """Load and validate GEMINI_API_KEY from .env"""
    load_dotenv()
    api_key = os.getenv(ENV_GEMINI_API_KEY)
    if not api_key:
        raise RuntimeError(ERR_API_KEY_IS_NONE)
    return api_key


def create_client(api_key: str) -> genai.Client:
    """Create Gemini client"""
    return genai.Client(api_key=api_key)


def gen_content_test(client: genai.Client):
    """Generate test response from Gemini"""
    response = client.models.generate_content(
        model=MODEL_FLASH_25, contents=TEST_PROMPT
    )
    return response.text


def main() -> None:
    api_key = get_api_key()
    client = create_client(api_key)
    print(gen_content_test(client))


if __name__ == "__main__":
    main()
