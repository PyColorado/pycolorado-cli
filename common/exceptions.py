class ConfigurationError(Exception):
    pass


class APIException(Exception):
    def __init__(self, msg, api_response=None):
        super().__init__(msg)
        self.api_response = api_response

    def __str__(self):
        if self.api_response:
            return f"[{self.api_response.status_code}]: {super().__str__()}"
        else:
            return super().__str__()
