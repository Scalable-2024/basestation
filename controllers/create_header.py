from flask import jsonify, request
from utils.headers import BobbHeaders
from utils.optional_headers import BobbOptionalHeaders


def create_header():
    body_data = request.get_json()

    try:
        # Extract necessary header fields
        necessary_header = body_data["necessary_header"]
        version_major = necessary_header["version_major"]
        version_minor = necessary_header["version_minor"]
        message_type = necessary_header["message_type"]
        dest_ipv6 = necessary_header["dest_ipv6"]
        dest_port = necessary_header["dest_port"]
        source_ipv6 = necessary_header["source_ipv6"]
        source_port = necessary_header["source_port"]
        sequence_number = necessary_header["sequence_number"]
        timestamp = necessary_header["timestamp"]

        bobb_header = BobbHeaders(
            version_major=version_major,
            version_minor=version_minor,
            message_type=message_type,
            dest_ipv6=dest_ipv6,
            dest_port=dest_port,
            source_ipv6=source_ipv6,
            source_port=source_port,
            sequence_number=sequence_number,
            timestamp=timestamp
        )
        x_bobb_header = bobb_header.build_header().hex()

        optional_header = body_data["optional_header"]
        hop_count = optional_header["hop_count"]
        priority = optional_header["priority"]
        encryption_algo = optional_header["encryption_algo"]

        optional_header_obj = BobbOptionalHeaders(
            timestamp=timestamp,
            hop_count=hop_count,
            priority=priority,
            encryption_algo=encryption_algo
        )
        x_bobb_optional_header = optional_header_obj.build_optional_header().hex()

    except KeyError as e:
        return jsonify({
            "status": "error",
            "message": f"Missing required field: {e.args[0]}"
        }), 400

    return jsonify({
        "status": "success",
        "data": {
            "X-Bobb-Header": x_bobb_header,
            "X-Bobb-Optional-Header": x_bobb_optional_header
        },
        "status_code": 200
    }), 200