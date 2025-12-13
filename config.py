MODEL = "gemini-2.5-flash"  # model to use
MSG_LIMIT = 10000  # max characters in single request
PYTHON_RUN_TIMEOUT = 30  # python code run timeout in seconds
WORKING_DIR = "./calculator"


class ErrorMessage:
    NO_API_KEY = "No API_KEY found... Is GEMINI_API_KEY set in .env?"
    API_REQUEST_FAILED = "Something went wrong... API request failed."
