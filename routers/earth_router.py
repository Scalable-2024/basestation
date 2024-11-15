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
    middleware = check_headers()
    if middleware is not True:
        return middleware

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
    
    @router.route('/v1/update_location', methods=['POST'])
def update_location():
    """
    Receives location updates from satellites.
    Example request body:
    {
        "satellite_id": "satellite-group-13",
        "location": {
            "latitude": 40.712776,
            "longitude": -74.005974
        }
    }
    """
    data = request.get_json()
    satellite_id = data.get("satellite_id")
    location = data.get("location")

    if not satellite_id or not location:
        return {"error": "Missing required fields"}, 400

    if "satellite_locations" not in g:
        g.satellite_locations = {}

    g.satellite_locations[satellite_id] = location
    print(f"Received location update from satellite {satellite_id}: {location}")
    
    return {"status": "Location updated successfully"}, 200
