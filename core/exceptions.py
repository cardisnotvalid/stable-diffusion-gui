class NoApiKey(Exception):
    "Raised when the API key is missing in the file"
    pass


class NoFileWithApiKey(Exception):
    "Raised when the file with API key is not exists"
    pass


class NoModels(Exception):
    "Raised when the models is missing in the file"
    pass


class NoFileWithModels(Exception):
    "Raised when the file with models is not exists"
    pass


class ResponseErrorCode(Exception):
    "Raised when there is an error in the response"

    def __init__(self, error_code: str) -> None:
        self.error_code = "Error code: %s" % error_code
        super().__init__(self.error_code)
