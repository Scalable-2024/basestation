import time
from flask import Flask, request, g

from config.config import load_from_config_file
from helpers.name_generator import generate_name
from routers.earth_router import router as main_router
from config.constants import X_BOBB_HEADER, ERROR_INVALID_BOBB_HEADER, X_BOBB_OPTIONAL_HEADER
from helpers.response_helper import create_response
from utils.crypto_utils import generate_keys
from utils.headers import BobbHeaders
from utils.optional_headers import BobbOptionalHeaders

app = Flask(__name__)

app.register_blueprint(main_router)


@app.before_request
def add_custom_headers_to_request():
    # Parse BobbHeaders
    custom_header = request.headers.get(X_BOBB_HEADER)
    if custom_header:
        try:
            bobb = BobbHeaders()
            g.bobb_header = bobb.parse_header(bytes.fromhex(custom_header))
        except Exception as e:
            return create_response({"error": ERROR_INVALID_BOBB_HEADER, "details": str(e)}, 400)
    else:
        g.bobb_header = None  # No Bobb header present

    # Parse LEOOptionalHeaders
    optional_header = request.headers.get(X_BOBB_OPTIONAL_HEADER)
    if optional_header:
        try:
            leo = BobbOptionalHeaders()
            g.bobb_optional_header = leo.parse_optional_header(
                bytes.fromhex(optional_header))
        except Exception as e:
            return create_response({"error": X_BOBB_OPTIONAL_HEADER, "details": str(e)}, 400)
    else:
        g.bobb_optional_header = None


@app.after_request
def add_custom_headers_to_response(response):
    """
    Middleware to inject the BobbHeaders and LEOOptionalHeaders into the response.
    """
    bobb_response = BobbHeaders(
        version_major=1,
        version_minor=0,
        message_type=2,
        sequence_number=456,
        timestamp=int(time.time())
    )
    response.headers[X_BOBB_HEADER] = bobb_response.build_header().hex()

    leo_response = BobbOptionalHeaders(
        timestamp=int(time.time()),
        hop_count=10,
        priority=1,
        encryption_algo="AES256"
    )
    response.headers[X_BOBB_OPTIONAL_HEADER] = leo_response.build_optional_header(
    ).hex()

    return response


if __name__ == "__main__":
    name = load_from_config_file()["name"]

    generate_keys(name)
    app.run(debug=True, port=30001)