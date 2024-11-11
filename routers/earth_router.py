from flask import Blueprint

from config.constants import SATELLITE_FUNCTION_DISASTER_IMAGING
from controllers.create_header import create_header
from middleware.header import check_headers
import base64

router = Blueprint('main', __name__)

@router.route('/v1/create-header', methods=['POST'])
def create_custom_headers():
    return create_header()

@router.route('/v1/satellites', methods=['GET'])
def get_satellites():
    middleware = check_headers()
    if middleware is not True:
        return middleware

    return {"satellites": [{"location": "Valencia", "ip": "2001:0000:130F:0000:0000:09C0:876A:130B", "function": "disaster-imaging"}, {"location": "Madrid", "ip": "2001:0000:130F:0000:0000:09C0:876A:130C", "function": "disaster-imaging"}, {"location": "Barcelona", "ip": "2001:0000:130F:0000:0000:09C0:876A:130D", "function": "disaster-imaging"}, {"location": "Sevilla", "ip": "2001:0000:130F:0000:0000:09C0:876A:130E", "function": "disaster-imaging"}, {"location": "Zaragoza", "ip": "2001:0000:130F:0000:0000:09C0:876A:130F", "function": "disaster-imaging"}, {"location": "Málaga", "ip": "2001:0000:130F:0000:0000:09C0:876A:1310", "function": "disaster-imaging"}, {"location": "Murcia", "ip": "2001:0000:130F:0000:0000:09C0:876A:1311", "function": "disaster-imaging"}, {"location": "Palma de Mallorca", "ip": "2001:0000:130F:0000:0000:09C0:876A:1312", "function": "disaster-imaging"}, {"location": "Las Palmas de Gran Canaria", "ip": "2001:0000:130F:0000:0000:09C0:876A:1313", "function": "disaster-imaging"}, {"location": "Bilbao", "ip": "2001:0000:130F:0000:0000:09C0:876A:1314", "function": "disaster-imaging"}]}

@router.route('/v1/satellites/<string:ip>/images', methods=['POST'])
def capture_image(ip):
    # middleware = check_headers()
    # if middleware is not True:
    #     return middleware

    satellites = {
        "satellites": [
        {"location": "Valencia", "ip": "2001:0000:130F:0000:0000:09C0:876A:130B", "function": "disaster-imaging"},
        {"location": "Madrid", "ip": "2001:0000:130F:0000:0000:09C0:876A:130C", "function": "disaster-imaging"},
        {"location": "Barcelona", "ip": "2001:0000:130F:0000:0000:09C0:876A:130D", "function": "disaster-imaging"},
        {"location": "Sevilla", "ip": "2001:0000:130F:0000:0000:09C0:876A:130E", "function": "disaster-imaging"},
        {"location": "Zaragoza", "ip": "2001:0000:130F:0000:0000:09C0:876A:130F", "function": "disaster-imaging"},
        {"location": "Málaga", "ip": "2001:0000:130F:0000:0000:09C0:876A:1310", "function": "disaster-imaging"},
        {"location": "Murcia", "ip": "2001:0000:130F:0000:0000:09C0:876A:1311", "function": "disaster-imaging"},
        {"location": "Palma de Mallorca", "ip": "2001:0000:130F:0000:0000:09C0:876A:1312", "function": "disaster-imaging"},
        {"location": "Las Palmas de Gran Canaria", "ip": "2001:0000:130F:0000:0000:09C0:876A:1313", "function": "disaster-imaging"},
        {"location": "Bilbao", "ip": "2001:0000:130F:0000:0000:09C0:876A:1314", "function": "whale-tracking"}
        ]
    }

    if ip not in [satellite["ip"] for satellite in satellites["satellites"]]:
        return {"error": "Satellite not found"}, 404

    satellite = [satellite for satellite in satellites["satellites"] if satellite["ip"] == ip][0]
    if satellite["function"] != SATELLITE_FUNCTION_DISASTER_IMAGING:
        return {"error": "Satellite can not take images", "status": "failure", "status_code": 400}, 400


    with open("development/mar-menor.jpg", "rb") as image_file:
        base64_bytes = base64.b64encode(image_file.read())
        encoded_string = base64_bytes.decode()

    return {"status":"success","image": encoded_string, "status_code": 200}