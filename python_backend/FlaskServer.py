import numpy as np
from flask import Flask, jsonify, send_file
from flask_cors import CORS, cross_origin
from RoofData import get_roof_data
from PIL import Image

app = Flask(__name__)
CORS(app, support_credentials=True)

curr_id = 0

received_ids = []

def get_segmented_img_name(id):
    return "./segmented/" + str(id) + ".png"


@app.route("/address/<address>")
@cross_origin(supports_credentials=True)
def get_info(address):
    m_area, segmented_img = get_roof_data(address)

    global curr_id
    img = Image.fromarray(segmented_img)
    img.save(get_segmented_img_name(curr_id))

    my_json = {
        "area": m_area,
        "id": curr_id
    }
    return jsonify(my_json)


@app.route("/get-by-id/<id>")
@cross_origin(supports_credentials=True)
def load_segmentation_img(id):
    # global received_ids
    # received_ids.append(id)
    return send_file(get_segmented_img_name(id), 'image/png')
