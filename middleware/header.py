from flask import request, g
from config.constants import (
    X_BOBB_HEADER,
    X_BOBB_OPTIONAL_HEADER,
    ERROR_INVALID_BOBB_HEADER,
    ERROR_INVALID_OPTIONAL_HEADER
)
from helpers.response_helper import create_response
from utils.headers import BobbHeaders
from utils.optional_headers import BobbOptionalHeaders


def check_headers():
    """
    Middleware to parse BobbHeaders and BobbOptionalHeaders from the request.
    Returns True if valid, otherwise returns a Flask response.
    """
    custom_header = request.headers.get(X_BOBB_HEADER)
    if custom_header:
        try:
            bobb = BobbHeaders()
            g.bobb_header = bobb.parse_header(bytes.fromhex(custom_header))
        except Exception as e:
            return create_response({"error": ERROR_INVALID_BOBB_HEADER, "details": str(e)}, 400)
    else:
        return create_response({"error": ERROR_INVALID_BOBB_HEADER}, 400)

    optional_header = request.headers.get(X_BOBB_OPTIONAL_HEADER)
    if optional_header:
        try:
            leo = BobbOptionalHeaders()
            g.bobb_optional_header = leo.parse_optional_header(
                bytes.fromhex(optional_header))
        except Exception as e:
            return create_response({"error": ERROR_INVALID_OPTIONAL_HEADER, "details": str(e)}, 400)
    else:
        return create_response({"error": ERROR_INVALID_OPTIONAL_HEADER}, 400)

    return True