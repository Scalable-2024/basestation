from flask import request
from utils.headers import BobbHeaders
from utils.optional_headers import BobbOptionalHeaders

def capture_image():
    body_data = request.get_json()

