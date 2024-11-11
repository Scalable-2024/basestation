from flask import Blueprint
import json

from config.constants import SATELLITE_FUNCTION_DISASTER_IMAGING
from controllers.create_header import create_header
from middleware.header import check_headers
import base64

router = Blueprint('main', __name__)

def read_satellites_from_json():
    with open('satellites.json', 'r') as json_file:
        data = json.load(json_file)
        return data['satellites']

@router.route('/v1/create-header', methods=['POST'])
def create_custom_headers():
    return create_header()

@router.route('/v1/satellites', methods=['GET'])
def get_satellites():
    middleware = check_headers()
    if middleware is not True:
        return middleware

    satellites = read_satellites_from_json()
    return {"satellites": satellites}

@router.route('/v1/satellites/<string:ip>/images', methods=['POST'])
def capture_image(ip):
    # middleware = check_headers()
    # if middleware is not True:
    #     return middleware

    satellites = read_satellites_from_json()

    if ip not in [sat["ip"] for sat in satellites]:
        return {"error": "Satellite not found"}, 404

    satellite = next((sat for sat in satellites if sat["ip"] == ip), None)
    if satellite["function"] != SATELLITE_FUNCTION_DISASTER_IMAGING:
        return {
            "error": "Satellite can not take images",
            "status": "failure",
            "status_code": 400
        }, 400

    with open("development/mar-menor.jpg", "rb") as image_file:
        base64_bytes = base64.b64encode(image_file.read())
        encoded_string = base64_bytes.decode()

    return {"status":"success","image": encoded_string, "status_code": 200}