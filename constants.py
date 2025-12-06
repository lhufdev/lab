from enum import StrEnum


class Model(StrEnum):
    FLASH_25 = "gemini-2.5-flash"


class ErrorMessage:
    NO_API_KEY = "No API_KEY found... Is GEMINI_API_KEY set in .env?"
    API_REQUEST_FAILED = "Something went wrong... API request failed."
