import logging
from flask import Flask, jsonify, request
from utils import response_format
from models import session, Biodata

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = Flask(__name__)

@app.route("/api/health/")
def deployment_status():
    logging.info("Health route was accessed")
    return jsonify(message="deployment is SUCCESSFUL"), 200

@app.route("/api/biodata/")
def get_all_data():
    all_data = session.query(Biodata).all()
    serialized_data = [item.serialize for item in all_data]
    logging.info("fetched all biodata records (count=%s)", len(serialized_data))
    return response_format(
        message="Fetched all biodata successfully",
        data=serialized_data
    )

@app.route("/api/biodata/post/", methods=["POST"])
def add_data():
    data = request.get_json()
    required_fields = ["first_name", 'last_name', "age", "state_of_origin"]
    for item in required_fields:
        if item not in data:
            logging.warning("Missing required field %s", item)
            return response_format(
                status="error",
                message=f"Missing required field: {item}",
                status_code=400
            )
    
    new_biodata = Biodata(
        first_name = data["first_name"],
        last_name = data["last_name"],
        age = data["age"],
        state_of_origin = data["state_of_origin"]
    )
    session.add(new_biodata)
    session.commit()
    logging.info("Added new biodata record (id=%s)", new_biodata.id)
    return response_format(
        message="Your data has been added to the RECORDS",
        data=new_biodata.serialize
    )

@app.route("/api/biodata/<int:id>/delete/", methods=["DELETE"])
def del_biodata(id):
    biodata_row = session.query(Biodata).filter(Biodata.id==id).one()
    if not biodata_row:
        logging.warning("Attempted to delete non-existent record (id=%s)", id)
        response_format(
            status="error",
            message=f"No biodata found with id {id}",
            status_code=404
        )

    session.delete(biodata_row)
    session.commit()
    logging.info("Deleted biodata (id=%s)", id)
    return response_format(
        message=f"Biodata with id {id} deleted successfully",
    )

if __name__ == "__main__":
    logging.info("[INFO] Starting Flask server...")
    app.run(host="0.0.0.0", port=5000)
