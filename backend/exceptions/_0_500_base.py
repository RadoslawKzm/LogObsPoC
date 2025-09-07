import fastapi


class BaseCustomError(Exception):
    """Every custom exception is following <CustomName>Error :> rule N818
    Every custom exception class has to have implemented unique mes

    Internal Message is *<Probable Cause of the Error>*
    Internal Code is debug code displayed for User to create bug report.
    HTTP_Code is return code for User.
    External Message is Message displayed for User. **No Tracebacks there!**

    :param int http_code: HTTP code aimed to be shown to customers.
                           Hardcoded up in exception class.
    :param str external_message: HTTP response message provided dynamically.
                                 Aimed at customer so exclude any internal info
    :param int internal_code: Internal code hardcoded in exception class.
                              Sent to client for easier bug fixing.
    :param str internal_message: Put here *PROBABLE CAUSE* of the error.
                                 Logged in our internal logger.
                        How to? :>> raise ApiCustom(internal_message="Problem")
                                 Aimed at developers so be helpful to ourselves

    """

    http_code: int = fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR
    internal_code: int = 500
    external_message: str = (
        "Internal server error. Our team has been notified."
    )
    internal_message: str
    _tree: dict = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._add_to_tree(cls)

    @classmethod
    def _add_to_tree(cls, new_cls):
        parent = new_cls.__base__

        if not issubclass(new_cls, BaseCustomError) or parent is object:
            return

        # If direct child of BaseCustomError, add at root
        if parent is BaseCustomError:
            if new_cls.__name__ not in cls._tree:
                cls._tree[new_cls.__name__] = {"object": new_cls}
            return

        # Otherwise, recursively insert under the correct parent
        def insert_recursive(tree: dict):
            for key, val in tree.items():
                if key == parent.__name__:
                    # Parent found, add child
                    if new_cls.__name__ not in val:
                        val[new_cls.__name__] = {"object": new_cls}
                    return True
                # Recurse into nested dictionaries
                for nested_key, nested_val in val.items():
                    if isinstance(nested_val, dict):
                        if insert_recursive({nested_key: nested_val}):
                            return True
            return False

        inserted = insert_recursive(cls._tree)
        if not inserted:
            # Parent not found yet, add placeholder for parent then insert
            cls._tree[parent.__name__] = {
                "object": parent,
                new_cls.__name__: {"object": new_cls},
            }

    def __init__(self, internal_message: str = "", external_message: str = ""):
        super().__init__()
        self.internal_message = internal_message or self.internal_message
        self.external_message = external_message or self.external_message

    @classmethod
    def openapi(cls):
        return {
            "summary": f"{cls.http_code}: {cls.__name__}",
            "description": cls.internal_message,
            "value": {"message": cls.external_message},
        }
