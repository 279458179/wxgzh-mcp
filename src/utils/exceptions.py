class WeChatAPIError(Exception):
    def __init__(self, errcode: int, errmsg: str):
        self.errcode = errcode
        self.errmsg = errmsg
        super().__init__(f"Error {errcode}: {errmsg}")


class AuthenticationError(WeChatAPIError):
    pass


class TokenExpiredError(AuthenticationError):
    pass


class RateLimitError(WeChatAPIError):
    pass


class InvalidParameterError(WeChatAPIError):
    pass


class NetworkError(Exception):
    pass


class FileNotFoundError(Exception):
    pass
