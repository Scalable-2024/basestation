# Basestation for scalable computing group 1, 13 and 8

## Features
Send request to satellite
Receive data from satellite

## Request/Routes

#### Create Custom Headers
- **Endpoint**: `/v1/create-header`
- **Method**: `POST`
- **Description**: Creates custom headers based on the request body.
- **Request Body**:
    ```json
    {
        "necessary_header": {
            "version_major": 1,
            "version_minor": 0,
            "message_type": 2,
            "dest_ipv6": "::1",
            "dest_port": 12345,
            "source_ipv6": "::1",
            "source_port": 12345,
            "sequence_number": 456,
            "timestamp": 1633072800
        },
        "optional_header": {
            "hop_count": 10,
            "priority": 1,
            "encryption_algo": "AES256"
        }
    }
    ```
- **Response**:
    ```json
    {
        "status": "success",
        "data": {
            "X-Bobb-Header": "<hex-encoded-header>",
            "X-Bobb-Optional-Header": "<hex-encoded-optional-header>"
        },
        "status_code": 200
    }
    ```

#### Get Satellites
- **Endpoint**: `/v1/satellites`
- **Method**: `GET`
- **Description**: Returns a list of available satellites.
- **Response**:
    ```json
    {
        "satellites": [
            {"location": "Valencia", "ip": "2001:0000:130F:0000:0000:09C0:876A:130B", "function": "disaster-imaging"},
            {"location": "Madrid", "ip": "2001:0000:130F:0000:0000:09C0:876A:130C", "function": "disaster-imaging"},
            ...
        ]
    }
    ```

#### Capture Image
- **Endpoint**: `/v1/satellites/<string:ip>/images`
- **Method**: `POST`
- **Description**: Captures an image from a specified satellite.
- **Response**:
    ```json
    {
        "status": "success",
        "image": "<base64-encoded-image>",
        "status_code": 200
    }
    ```