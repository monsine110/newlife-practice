from flask import jsonify

def response_format(status="success", message="success", data=None, status_code=200):
    response = {
        "status": status,
        "message": message,
        "data": data
    }

    if isinstance(data, list):
        response["count"] = len(data)

    return jsonify(response), status_code