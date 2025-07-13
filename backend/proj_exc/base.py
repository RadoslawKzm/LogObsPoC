import fastapi


class BaseCustomError(Exception):
    """Every custom exception is following ...Error rule N818
    Every custom exception class has to have implemented unique message.
    While using it as baseclass code yourself: http_code, internal_code, external_msg.
    Internal_msg and internal_exception will be dynamic from inside of code.

    :param int http_code: HTTP code aimed to be shown to customers.
                           Hardcoded up in exception class.
    :param str external_message: HTTP response message provided dynamically.
                                 Aimed at customer so exclude any internal info
    :param int internal_code: Internal code hardcoded in exception class.
                                Aimed for us.
    :param str internal_message: Message to internal logger provided in code.
                                 raise ApiCustom(internal_message="Problem")
                                 Aimed at developers so be helpful to ourselves.
    """

    http_code: int = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code: int = 500
    external_message: str = (
        "Internal server error occurred. We are sorry, try again in some time."
    )
    internal_message: str

    def __init__(self, internal_message: str = ""):
        super().__init__()
        if internal_message:
            self.internal_message = internal_message
