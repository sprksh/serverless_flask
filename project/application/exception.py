# coding=utf-8
"""
Exceptions
"""
import logging

from application.api.api_response import ApiResponse


class ValidationError(Exception):
    pass


class ProjectException(Exception):
    error_code = "0001"
    message = "Something went wrong"

    def __init__(self, description=None, extra_payload=None):
        self.description = description
        self.extra_payload = extra_payload

    def __str__(self):
        return "exception: error_code=%s message=%s description=%s" % (
            self.error_code,
            self.message,
            self.description,
        )

    def with_description(self, description):
        self.description = description
        return self

    @property
    def code(self):
        return "0401" + self.error_code


class ValidationException(ProjectException):
    error_code = "0002"
    message = "Request Invalid"


class ProjectValidationException(ProjectException):
    error_code = "0006"
    message = "Request Invalid"


def get_http_status_code_from_exception(exception):
    # status_code_map = {RandomError: 409}
    status_code_map = {}
    return status_code_map.get(type(exception), 400)


def exception_handler(error):
    logger = logging.getLogger("api_exception")
    logger.exception("Exception in api: %s", error, exc_info=True)

    if isinstance(error, ProjectException):
        status_code = get_http_status_code_from_exception(error)
        error = dict(
            code=error.code,
            message=error.message,
            developer_message=error.description,
            extra_payload=error.extra_payload,
        )
        return ApiResponse.build(errors=[error], status_code=status_code)

    status_code = 500
    if getattr(error, "status_code", None):
        status_code = error.status_code
    if getattr(error, "code", None):
        status_code = error.code

    if isinstance(error, ValidationError):
        status_code = 400
    import re

    if not re.search(r"^[1-5]\d{2}$", str(status_code)):
        status_code = 500

    error_dict = dict(code=status_code)
    error_dict["message"] = (
        error.message if hasattr(error, "message") else "Unknown Exception occurred."
    )
    error_dict["developer_message"] = (
        error.description if hasattr(error, "description") else str(error)
    )

    response = ApiResponse.build(errors=[error_dict], status_code=status_code)
    return response


def api_validation_exception_handler(exception):
    error = dict(
        code=exception.code,
        message=exception.message,
        developer_message=exception.description,
        extra_payload=exception.extra_payload,
    )
    return ApiResponse.build(errors=[error], status_code=400)
